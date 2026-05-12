"""
音画同步构建脚本 - 可靠方案
1. 生成 TTS 语音 + 测算时长 → 写入 JSON
2. manim 读取 JSON 按语音时长控制动画节奏（无声渲染）
3. 拼接所有语音段 → ffmpeg 合成最终视频
"""
import subprocess
import os
import sys
import json
import glob as g
import mutagen.mp3

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT  = os.path.join(PROJECT, "video_output")
AUDIO   = os.path.join(OUTPUT, "sync_audio")
VOICE   = "zh-CN-XiaoxiaoNeural"

os.makedirs(AUDIO, exist_ok=True)
os.makedirs(OUTPUT, exist_ok=True)

GAMES = []

def add_game(num, name, tagline, steps, rules_text, end_text):
    GAMES.append({
        "num": num, "name": name, "tagline": tagline,
        "steps": steps,        # list of (title, desc)
        "rules": rules_text,
        "end": end_text,
    })

# ═══════════════════════════════════════════════════
#  5个游戏数据
# ═══════════════════════════════════════════════════

add_game("01", "车厢热搜榜", "匿名投票 + 现场揭晓 + 轻量回应",
    [("主持人抛出热搜话题", "例如「最像徒步领队的人」"),
     ("全员匿名投票", "微信群/小程序，30秒内完成"),
     ("现场揭晓前三名", "被点名者完成获奖感言或出征姿势")],
    "规则要点：不能投自己 / 回应任务保持轻量 / 话题只做友好调侃，避开外貌收入隐私等敏感内容",
    "适合开场快速破冰，让全车在不强迫表演的情况下进入团建气氛。")

add_game("02", "大巴卧底旅行团", "隐藏身份 + 一句话发言 + 轻推理",
    [("主持人私发身份", "多数人拿同一个关键词，5名卧底拿到相近但不同的词"),
     ("每轮一句话描述", "不能直接说出关键词，根据发言找卧底"),
     ("全车投票淘汰", "每轮淘汰1-2人，卧底坚持到最后3人则获胜")],
    "关键词组合：徒步对逛商场 / 爬山对泡温泉 / 团建对年会 / 背包对行李箱 / 山顶对餐厅",
    "比传统「谁是卧底」更贴合出行场景，推理轻、节奏快，适合中段把气氛再次拉起来。")

add_game("03", "即兴配音巴士", "场景题 + 情绪题 + 1分钟短剧",
    [("分组抽题", "6-8人一组，抽「场景题」+「情绪题」"),
     ("准备1分钟表演1分钟", "在座位上分配台词，即兴演绎"),
     ("全车投票评奖", "最佳配音组、最佳戏精、最佳反差感")],
    "场景示例：精英徒步队只带了零食没带水 / 山顶神秘任务 / 大巴变冠军领奖台。风格：悬疑片、新闻联播、霸总剧、动物世界、武侠片、选秀导师",
    "综艺效果最强的游戏，适合后段提神。注意控制音量和动作，确保不影响行车安全。")

add_game("04", "车厢任务盲盒", "隐藏任务 + 自然触发 + 阶段结算",
    [("每人抽取隐藏任务卡", "只有自己知道，不能展示给别人"),
     ("自然互动中完成", "聊天时悄悄完成任务，向主持人认证得分"),
     ("阶段结算积分", "被猜中任务则失败，每15-20分钟结算一次")],
    "任务示例：让3个人主动跟你击掌 / 让5个人说出「今天一定能登顶」/ 让一个人唱一句歌 / 找到同月生日的人 / 让同事夸你的装备",
    "最适合全程穿插，互动不会集中爆发，让不爱表演的人也能悄悄参与进来。")

add_game("05", "沿途情报猎人", "窗外观察 + 小组共创 + 抵达前颁奖",
    [("分组发放情报清单", "5-7组，观察窗外、车内、团队状态"),
     ("小组共创打卡", "记录画面、故事、团队角色，完成清单任务"),
     ("30秒分享+颁奖", "展示队名、口号、创意故事，总分最高获奖")],
    "清单示例：找到最像徒步电影开场的窗外画面 / 发现绿色元素招牌 / 给本车起队名 / 设计徒步口号 / 用窗外三个元素编30秒故事",
    "临近目的地使用效果最好，能把车上情绪自然转到下车后的徒步队伍。")


def gen_tts(text, filename):
    """生成一段 TTS，返回 (路径, 秒数)"""
    path = os.path.join(AUDIO, filename)
    if os.path.exists(path):
        return path, mutagen.mp3.MP3(path).info.length
    clean = text.replace('"', '').replace("'", '').replace('\n', ' ')
    subprocess.run([
        sys.executable, "-m", "edge_tts",
        "--voice", VOICE, "--text", clean, "--write-media", path,
    ], capture_output=True)
    return path, mutagen.mp3.MP3(path).info.length


def gen_all_tts():
    """为所有游戏生成 TTS 并记录时长 → 写入 timing.json"""
    timing = {}
    for game in GAMES:
        num = game["num"]
        timing[num] = {"name": game["name"], "tagline": game["tagline"],
                       "steps": [], "rules": {}, "end": {}}

        # 标题
        intro_text = f"第{int(num)}个游戏：{game['name']}。{game['tagline']}。"
        path, dur = gen_tts(intro_text, f"{num}_00_intro.mp3")
        timing[num]["intro"] = {"file": path, "dur": round(dur, 2), "text": intro_text}
        print(f"  [{num}] intro: {dur:.1f}s")

        # 步骤
        for i, (title, desc) in enumerate(game["steps"]):
            text = f"第{i+1}步，{title}。{desc}"
            path, dur = gen_tts(text, f"{num}_0{i+1}_step{i+1}.mp3")
            timing[num]["steps"].append({"file": path, "dur": round(dur, 2), "text": text})
            print(f"  [{num}] step{i+1}: {dur:.1f}s")

        # 规则
        rules_text = game["rules"]
        path, dur = gen_tts(rules_text, f"{num}_04_rules.mp3")
        timing[num]["rules"] = {"file": path, "dur": round(dur, 2), "text": rules_text}
        print(f"  [{num}] rules: {dur:.1f}s")

        # 结尾
        end_text = game["end"]
        path, dur = gen_tts(end_text, f"{num}_05_end.mp3")
        timing[num]["end"] = {"file": path, "dur": round(dur, 2), "text": end_text}
        print(f"  [{num}] end: {dur:.1f}s")

    # 写 JSON
    json_path = os.path.join(AUDIO, "timing.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(timing, f, ensure_ascii=False, indent=2)
    print(f"\nTiming data saved to {json_path}")
    return timing


def concat_audio(game_num):
    """拼接某个游戏的所有音频段"""
    timing = json.load(open(os.path.join(AUDIO, "timing.json"), encoding="utf-8"))
    t = timing[game_num]
    files = [t["intro"]["file"]]
    for s in t["steps"]:
        files.append(s["file"])
    files.append(t["rules"]["file"])
    files.append(t["end"]["file"])

    list_file = os.path.join(AUDIO, f"{game_num}_list.txt")
    with open(list_file, "w") as f:
        for af in files:
            f.write(f"file '{af}'\n")

    output_path = os.path.join(AUDIO, f"{game_num}_full.mp3")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", list_file, "-c", "copy", output_path,
    ], capture_output=True)
    return output_path


def render_manim(game_num):
    """渲染 manim 无声视频"""
    script = os.path.join(os.path.dirname(__file__), "sync_scenes.py")
    subprocess.run([
        sys.executable, "-m", "manim", "-ql",
        script, f"Game{game_num}Synced",
    ], cwd=PROJECT, capture_output=True, text=True)

    # 找视频文件 - manim 0.20 输出到 media/videos/<script_name>/480p15/
    script_base = os.path.splitext(os.path.basename(script))[0]
    video_dir = os.path.join(PROJECT, "media", "videos", script_base, "480p15")
    video_file = os.path.join(video_dir, f"Game{game_num}Synced.mp4")
    if os.path.exists(video_file):
        return video_file
    # fallback: recursive search
    files = g.glob(os.path.join(PROJECT, "media", "videos", "**", "*.mp4"), recursive=True)
    matches = [f for f in files if f"Game{game_num}Synced" in f]
    if matches:
        return max(matches, key=os.path.getmtime)
    print(f"  manim ERROR: no video found (looked in {video_dir})")
    return None


def build_game(game_num):
    """构建一个完整游戏视频"""
    print(f"\n{'='*60}")
    name = [g["name"] for g in GAMES if g["num"] == game_num][0]
    print(f"Building Game {game_num}: {name}")
    print(f"{'='*60}")

    # 1. 渲染 manim（读取 timing.json 控制动画时长）
    print("  [1/3] Rendering animation...")
    video = render_manim(game_num)
    if not video:
        print("  FAILED: manim rendering")
        return None
    print(f"  Video rendered: {os.path.basename(video)}")

    # 2. 拼接音频
    print("  [2/3] Concatenating audio...")
    audio = concat_audio(game_num)
    print(f"  Audio: {os.path.basename(audio)}")

    # 3. 合成
    print("  [3/3] Merging...")
    final = os.path.join(OUTPUT, f"{game_num}_{name}.mp4")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", video,
        "-i", audio,
        "-c:v", "libx264", "-c:a", "aac",
        "-shortest",
        "-map", "0:v:0", "-map", "1:a:0",
        final,
    ], capture_output=True)

    size = os.path.getsize(final) / 1024
    print(f"  DONE: {os.path.basename(final)} ({size:.0f} KB)")
    return final


def main():
    # 1. 生成所有 TTS
    print("=" * 60)
    print("Step 1: Generating TTS audio segments...")
    print("=" * 60)
    gen_all_tts()

    # 2. 逐个构建
    target = int(sys.argv[1]) if len(sys.argv) > 1 else None
    for game in GAMES:
        num = game["num"]
        if target and int(num) != target:
            continue
        build_game(num)

    # 结果
    finals = g.glob(os.path.join(OUTPUT, "0?_*.mp4"))
    if finals:
        print(f"\n{'='*60}")
        print(f"FINISHED! {len(finals)} videos:")
        for f in sorted(finals):
            print(f"  {os.path.basename(f)}")


if __name__ == "__main__":
    main()
