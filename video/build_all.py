"""
一键构建所有 5 个视频：
1. manim 渲染动画 → 无声 MP4
2. edge-tts 生成解说 → MP3
3. ffmpeg 合并视频和音频 → 最终 MP4

使用方法:
  cd "D:\Code x Demo\Yz-Demo"
  venv\Scripts\activate
  python video/build_all.py           # 构建全部
  python video/build_all.py 1         # 只构建第1个
"""
import subprocess
import os
import sys
import asyncio
import glob

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR  = os.path.join(PROJECT_ROOT, "video_output")
VIDEO_DIR   = os.path.join(PROJECT_ROOT, "video")

# manim 配置
MANIM_QUALITY = "-ql"  # 低质量快速 (-qh 高质量, -ql 低质量)

VOICE = "zh-CN-XiaoxiaoNeural"

GAMES = [
    {"num": "01", "class": "Game01HotSearch", "name": "车厢热搜榜"},
    {"num": "02", "class": "Game02Undercover", "name": "大巴卧底旅行团"},
    {"num": "03", "class": "Game03Dubbing",     "name": "即兴配音巴士"},
    {"num": "04", "class": "Game04BlindBox",    "name": "车厢任务盲盒"},
    {"num": "05", "class": "Game05Hunter",      "name": "沿途情报猎人"},
]

NARRATIONS = {
    "01_车厢热搜榜": "欢迎收看大巴团建互动游戏方案。第一个游戏：车厢热搜榜。核心玩法是匿名投票加现场揭晓加轻量回应。把全车员工变成热搜制造机。主持人抛出一个轻松话题，比如最像徒步领队的人，全员用微信群匿名投票，30秒内完成。主持人现场公布前三名，被点名者完成一句获奖感言或出征姿势。规则要点：不能投自己，回应任务保持轻量不强迫表演，话题只做友好调侃，避开外貌收入隐私等敏感内容。这个游戏适合开场快速破冰，能在不强迫表演的情况下让全车进入团建气氛。",

    "02_大巴卧底旅行团": "第二个游戏：大巴卧底旅行团。核心玩法是隐藏身份加一句话发言加轻推理。大多数人拿到同一个旅行关键词，少数卧底拿到相近但不同的关键词。35人设置5名卧底旅行者。每轮给一个话题，所有人依次说一句话描述，不能直接说出关键词。发言后全车投票淘汰1至2人。关键词组合例如：徒步对逛商场，爬山对泡温泉，团建对年会，背包对行李箱。规则很简单：每人每轮只说一句话，不能直接说关键词。卧底坚持到最后3人以内则卧底获胜。比传统谁是卧底更贴合出行场景，推理轻节奏快，适合中段把气氛再次拉起来。",

    "03_即兴配音巴士": "第三个游戏：即兴配音巴士。核心玩法是场景题加情绪题加1分钟短剧。把窗外路景、车内人物和徒步想象变成即兴配音短剧。6到8人一组，每组抽取一个场景题和一种风格题，在座位上快速分配台词，准备1分钟，表演1分钟。表演结束后全车投票评出最佳配音组、最佳戏精和最佳反差感。场景题示例：精英徒步队只带了零食没带水、山顶突然出现神秘任务。风格可选悬疑片、新闻联播、霸总剧、动物世界解说、武侠片。这是综艺效果最强的游戏，适合后段提神。",

    "04_车厢任务盲盒": "第四个游戏：车厢任务盲盒。核心玩法是隐藏任务加自然触发加阶段结算。每个人随机获得一张隐藏任务卡，在车程中自然完成。上车后每人抽取任务卡，不能展示给别人。玩家在聊天和互动中自然完成任务，完成后向主持人认证得分。被别人猜中任务则本任务失败。任务卡示例：让3个人主动跟你击掌，让5个人说出今天一定能登顶，让一个人唱一句歌，找到同月生日的人。这个游戏最适合穿插在全程，互动不会集中爆发，让不爱表演的人也能悄悄参与进来。积分最高者获得最佳隐藏任务王。",

    "05_沿途情报猎人": "第五个游戏：沿途情报猎人。核心玩法是窗外观察加小组共创加抵达前颁奖。它不是找物品，而是找画面、故事和团队角色。全车分成5到7组，每组发放沿途情报清单。小组在车程中观察窗外风景和团队状态，完成打卡任务。各组派代表做30秒分享展示队名、口号和创意故事。情报清单示例：找到最像徒步电影开场的窗外画面、给本车起队名、设计徒步口号、用窗外三个元素编30秒故事。临近目的地时使用效果最好，能把车上情绪自然转到下车后的徒步队伍。总分最高者获得最佳情报小队。",
}


def run_cmd(cmd, cwd=None):
    """运行命令并打印输出"""
    print(f"  → {' '.join(cmd[:4])}...")
    result = subprocess.run(cmd, cwd=cwd or PROJECT_ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ✗ 错误: {result.stderr[-300:]}")
    else:
        # 取最后一行有意义输出
        lines = [l for l in result.stdout.splitlines() if l.strip()]
        if lines:
            print(f"  ✓ {lines[-1][:120]}")
    return result.returncode == 0


def find_manim_video(scene_class):
    """在 media 目录中找 manim 渲染出的视频"""
    pattern = os.path.join(PROJECT_ROOT, "media", "videos", "*", f"{scene_class}.*.mp4")
    # manim 会在 media/videos/<quality>/ 下生成
    alt_pattern = os.path.join(PROJECT_ROOT, "media", "videos", "**", f"{scene_class}.*.mp4")
    files = glob.glob(pattern, recursive=False) or glob.glob(alt_pattern, recursive=True)
    if files:
        # 取最新的
        return max(files, key=os.path.getmtime)
    return None


def render_manim(game):
    """用 manim 渲染一个游戏的视频"""
    class_name = game["class"]
    print(f"\n{'='*60}")
    print(f"  🎬 渲染动画: {game['num']} - {game['name']} ({class_name})")
    print(f"{'='*60}")

    cmd = [
        sys.executable, "-m", "manim",
        MANIM_QUALITY,
        os.path.join(VIDEO_DIR, "generate_videos.py"),
        class_name,
    ]
    return run_cmd(cmd)


async def generate_tts(name, text):
    """用 edge-tts 生成语音"""
    mp3_path = os.path.join(OUTPUT_DIR, f"{name}.mp3")
    if os.path.exists(mp3_path):
        print(f"  ✓ 语音已存在: {name}.mp3")
        return mp3_path

    print(f"  🔊 生成语音: {name}")
    # 清理文本中的引号
    clean_text = text.replace('"', '').replace("'", '').replace('\n', ' ')
    cmd = f'edge-tts --voice "{VOICE}" --text "{clean_text}" --write-media "{mp3_path}"'
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode == 0:
        print(f"  ✓ 完成: {name}.mp3")
        return mp3_path
    else:
        print(f"  ✗ TTS 失败: {stderr.decode()[:200]}")
        return None


def combine_video_audio(video_path, audio_path, output_name):
    """用 ffmpeg 合并视频和音频"""
    output_path = os.path.join(OUTPUT_DIR, output_name)
    if os.path.exists(output_path):
        print(f"  ✓ 最终视频已存在: {output_name}")
        return output_path

    print(f"  🎬 合成: {output_name}")
    # 获取音频时长，调整视频速度以匹配
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        "-map", "0:v:0",
        "-map", "1:a:0",
        output_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  ✓ 合成完成: {output_name}")
        return output_path
    else:
        print(f"  ✗ 合成失败: {result.stderr[-300:]}")
        return None


async def build_one(game):
    """构建单个游戏的完整视频"""
    key = f"{game['num']}_{game['name']}"
    text = NARRATIONS.get(key, "")
    final_name = f"{game['num']}_{game['name']}_final.mp4"

    # 1. 渲染 manim
    if not render_manim(game):
        print(f"  ✗ manim 渲染失败，跳过")
        return False

    # 2. 找 manim 生成的视频
    manim_video = find_manim_video(game["class"])
    if not manim_video:
        print(f"  ✗ 找不到 manim 输出视频")
        return False
    print(f"  📁 找到视频: {os.path.basename(manim_video)}")

    # 3. 生成 TTS
    mp3_path = await generate_tts(key, text)
    if not mp3_path:
        return False

    # 4. 合成
    result = combine_video_audio(manim_video, mp3_path, final_name)
    return result is not None


async def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 检查依赖
    print("检查依赖...")
    for dep in ["ffmpeg"]:
        r = subprocess.run([dep, "-version"], capture_output=True)
        if r.returncode != 0:
            print(f"  ✗ {dep} 不可用，请安装 ffmpeg")
            print("    winget install ffmpeg")
            return
    print("  ✓ ffmpeg 可用")

    # 检查 edge-tts
    r = subprocess.run([sys.executable, "-m", "edge_tts", "--version"], capture_output=True, text=True)
    if r.returncode != 0:
        print("  ✗ edge-tts 未安装，运行: pip install edge-tts")
        return
    print("  ✓ edge-tts 可用")

    # 选择构建范围
    if len(sys.argv) > 1:
        idx = int(sys.argv[1]) - 1
        games_to_build = [GAMES[idx]]
    else:
        games_to_build = GAMES

    print(f"\n开始构建 {len(games_to_build)} 个视频...\n")

    for game in games_to_build:
        success = await build_one(game)
        if success:
            print(f"  ✅ {game['num']} {game['name']} 完成!")
        else:
            print(f"  ❌ {game['num']} {game['name']} 失败!")

    print(f"\n📁 输出目录: {OUTPUT_DIR}")
    # 列出最终文件
    finals = glob.glob(os.path.join(OUTPUT_DIR, "*_final.mp4"))
    if finals:
        print(f"✅ 共生成 {len(finals)} 个最终视频:")
        for f in sorted(finals):
            size_mb = os.path.getsize(f) / 1024 / 1024
            print(f"   📹 {os.path.basename(f)} ({size_mb:.1f} MB)")
    else:
        print("⚠️ 暂无最终视频生成")


if __name__ == "__main__":
    asyncio.run(main())
