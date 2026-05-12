"""
大巴团建互动游戏 - 5个音画同步介绍视频
每个画面切换时，对应语音同步播放
"""
from manim import *
import os
import asyncio
import subprocess
import sys

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "video_output")
AUDIO_DIR  = os.path.join(OUTPUT_DIR, "audio_segments")

BG      = "#1a1a2e"
ACCENT  = "#e94560"
GOLD    = "#f5c518"
WHITE   = "#ffffff"
LIGHT   = "#c8d6e5"
CARD_BG = "#16213e"

VOICE = "zh-CN-XiaoxiaoNeural"


def tts(text, filename):
    """生成单段语音"""
    path = os.path.join(AUDIO_DIR, filename)
    if os.path.exists(path):
        return path
    os.makedirs(AUDIO_DIR, exist_ok=True)
    clean = text.replace('"', '').replace("'", '').replace('\n', ' ')
    subprocess.run([
        sys.executable, "-m", "edge_tts",
        "--voice", VOICE,
        "--text", clean,
        "--write-media", path,
    ], capture_output=True)
    return path


def pre_generate_all_audio():
    """预生成所有语音片段"""
    print("Pre-generating audio segments...")
    os.makedirs(AUDIO_DIR, exist_ok=True)

    all_segments = {}

    # ── Game 01: 车厢热搜榜 ──
    all_segments["01"] = [
        ("01_intro", "第一个游戏：车厢热搜榜。匿名投票加现场揭晓，把全车员工变成热搜制造机。"),
        ("01_step1", "第一步，主持人抛出一个轻松话题，比如最像徒步领队的人。"),
        ("01_step2", "第二步，全员用微信群或小程序匿名投票，30秒内完成。"),
        ("01_step3", "第三步，主持人现场公布前三名，被点名者完成获奖感言或出征姿势。"),
        ("01_rules", "规则：不能投自己。回应任务保持轻量，话题只做友好调侃，避开敏感内容。"),
        ("01_end", "适合开场快速破冰，让全车进入团建气氛。"),
    ]

    # ── Game 02: 大巴卧底旅行团 ──
    all_segments["02"] = [
        ("02_intro", "第二个游戏：大巴卧底旅行团。隐藏身份加一句话发言加轻推理。"),
        ("02_step1", "第一步，主持人私发身份。大多数人拿同一个关键词，5名卧底拿到相近但不同的词。"),
        ("02_step2", "第二步，每轮给一个话题，所有人依次说一句话描述，不能直接说出关键词。"),
        ("02_step3", "第三步，全车投票淘汰1至2人。卧底坚持到最后3人以内则卧底获胜。"),
        ("02_examples", "关键词组合如：徒步对逛商场，爬山对泡温泉，团建对年会，背包对行李箱。"),
        ("02_end", "比传统谁是卧底更贴合出行场景，推理轻节奏快，适合中段提神。"),
    ]

    # ── Game 03: 即兴配音巴士 ──
    all_segments["03"] = [
        ("03_intro", "第三个游戏：即兴配音巴士。场景题加情绪题，把窗外风景变成即兴配音短剧。"),
        ("03_step1", "第一步，6到8人一组，每组抽取一个场景题和一种风格题。"),
        ("03_step2", "第二步，在座位上快速分配台词，准备1分钟，表演1分钟。"),
        ("03_step3", "第三步，全车投票评出最佳配音组、最佳戏精和最佳反差感。"),
        ("03_examples", "场景示例：精英徒步队只带了零食没带水。风格可选悬疑片、新闻联播、霸总剧、武侠片。"),
        ("03_end", "综艺效果最强的游戏，适合后段提神，注意控制音量和动作。"),
    ]

    # ── Game 04: 车厢任务盲盒 ──
    all_segments["04"] = [
        ("04_intro", "第四个游戏：车厢任务盲盒。隐藏任务加自然触发加阶段结算。"),
        ("04_step1", "第一步，上车后每人抽取一张任务卡，只有自己知道，不能展示给别人。"),
        ("04_step2", "第二步，在聊天和互动中自然完成任务，完成后向主持人认证得分。"),
        ("04_step3", "第三步，被别人猜中任务则失败。每15到20分钟结算一次积分。"),
        ("04_examples", "任务示例：让3个人主动跟你击掌，让5个人说出今天一定能登顶，让一个人唱一句歌。"),
        ("04_end", "最适合全程穿插，让不爱表演的人也能悄悄参与，积分最高者获奖。"),
    ]

    # ── Game 05: 沿途情报猎人 ──
    all_segments["05"] = [
        ("05_intro", "第五个游戏：沿途情报猎人。窗外观察加小组共创，抵达前颁奖。"),
        ("05_step1", "第一步，全车分成5到7组，每组发放沿途情报清单。"),
        ("05_step2", "第二步，小组在车程中观察窗外风景和团队状态，完成打卡任务。"),
        ("05_step3", "第三步，各组派代表做30秒分享，展示队名、口号和创意故事。"),
        ("05_examples", "清单示例：找到最像徒步电影开场的窗外画面，给本车起队名，设计徒步口号。"),
        ("05_end", "临近目的地使用效果最好，能把车上情绪自然转到下车后的徒步队伍。"),
    ]

    for game_num in all_segments:
        for filename, text in all_segments[game_num]:
            tts(text, f"{filename}.mp3")

    print("✓ 全部语音片段生成完毕")
    return all_segments


# ═══════════════════════════════════════════════════════════
#  游戏 01：车厢热搜榜
# ═══════════════════════════════════════════════════════════
class Game01HotSearch(Scene):
    def construct(self):
        self.camera.background_color = BG

        # 标题
        num = Text("01", font="sans-serif", weight=BOLD, font_size=96, color=ACCENT)
        name = Text("车厢热搜榜", font="sans-serif", weight=BOLD, font_size=60, color=WHITE)
        tag  = Text("匿名投票 + 现场揭晓 + 轻量回应", font="sans-serif", font_size=28, color=LIGHT)
        VGroup(num, name, tag).arrange(DOWN, buff=0.3)
        self.add_sound(os.path.join(AUDIO_DIR, "01_intro.mp3"))
        self.play(Write(num), Write(name), run_time=1.5)
        self.play(FadeIn(tag), run_time=0.5)
        self.wait(1.0)

        self.play(FadeOut(num), FadeOut(name), FadeOut(tag))

        # 步骤
        for seg, num_txt, title_txt, desc_txt in [
            ("01_step1", "1", "主持人抛出热搜话题", "例如「最像徒步领队的人」"),
            ("01_step2", "2", "全员匿名投票", "微信群/小程序，30秒内完成"),
            ("01_step3", "3", "现场揭晓前三名", "被点名者完成获奖感言或出征姿势"),
        ]:
            box = RoundedRectangle(corner_radius=0.15, width=10, height=1.1,
                                    fill_color=CARD_BG, fill_opacity=0.7,
                                    stroke_color=ACCENT, stroke_width=1)
            n = Text(num_txt, font="sans-serif", font_size=36, color=ACCENT, weight=BOLD)
            t = Text(title_txt, font="sans-serif", font_size=26, color=WHITE, weight=BOLD)
            d = Text(desc_txt, font="sans-serif", font_size=20, color=LIGHT)
            left = VGroup(n, t).arrange(RIGHT, buff=0.3)
            g = VGroup(left, d).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
            g.move_to(box.get_center())
            group = VGroup(box, g)

            self.add_sound(os.path.join(AUDIO_DIR, f"{seg}.mp3"))
            self.play(FadeIn(group, shift=RIGHT * 0.3), run_time=0.8)
            self.wait(2.5)

        self.play(*[FadeOut(m) for m in self.mobjects])

        # 规则
        r_title = Text("规则要点", font="sans-serif", font_size=40, color=GOLD)
        r_title.to_edge(UP, buff=0.8)
        rules = VGroup(
            self._rule("不能投自己"),
            self._rule("回应任务保持轻量，不强迫表演"),
            self._rule("话题只做友好调侃，避开敏感内容"),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        rules.next_to(r_title, DOWN, buff=0.7)

        self.add_sound(os.path.join(AUDIO_DIR, "01_rules.mp3"))
        self.play(FadeIn(r_title))
        for r in rules:
            self.play(FadeIn(r, shift=UP * 0.2), run_time=0.3)
        self.wait(2.0)

        # 结尾
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.add_sound(os.path.join(AUDIO_DIR, "01_end.mp3"))
        t1 = Text("适合开场快速破冰", font="sans-serif", font_size=32, color=GOLD)
        t2 = Text("让全车在不强迫表演的情况下进入团建气氛", font="sans-serif", font_size=24, color=LIGHT)
        VGroup(t1, t2).arrange(DOWN, buff=0.3)
        self.play(FadeIn(t1), FadeIn(t2))
        self.wait(3.0)

    def _rule(self, text):
        dot = Dot(color=ACCENT, radius=0.12)
        txt = Text(text, font="sans-serif", font_size=24, color=LIGHT)
        return VGroup(dot, txt).arrange(RIGHT, buff=0.35, aligned_edge=LEFT)


# ═══════════════════════════════════════════════════════════
#  游戏 02：大巴卧底旅行团
# ═══════════════════════════════════════════════════════════
class Game02Undercover(Scene):
    def construct(self):
        self.camera.background_color = BG

        num = Text("02", font="sans-serif", weight=BOLD, font_size=96, color=ACCENT)
        name = Text("大巴卧底旅行团", font="sans-serif", weight=BOLD, font_size=60, color=WHITE)
        tag  = Text("隐藏身份 + 一句话发言 + 轻推理", font="sans-serif", font_size=28, color=LIGHT)
        VGroup(num, name, tag).arrange(DOWN, buff=0.3)
        self.add_sound(os.path.join(AUDIO_DIR, "02_intro.mp3"))
        self.play(Write(num), Write(name), run_time=1.5)
        self.play(FadeIn(tag), run_time=0.5)
        self.wait(1.0)
        self.play(FadeOut(num), FadeOut(name), FadeOut(tag))

        for seg, num_txt, title_txt, desc_txt in [
            ("02_step1", "1", "主持人私发身份", "多数人同一关键词，5名卧底拿到相近但不同的词"),
            ("02_step2", "2", "每轮一句话描述", "不能直接说出关键词，根据发言推理找卧底"),
            ("02_step3", "3", "全车投票淘汰", "每轮淘汰1-2人，卧底坚持到最后3人则获胜"),
        ]:
            box = RoundedRectangle(corner_radius=0.15, width=10, height=1.1,
                                    fill_color=CARD_BG, fill_opacity=0.7,
                                    stroke_color=ACCENT, stroke_width=1)
            n = Text(num_txt, font="sans-serif", font_size=36, color=ACCENT, weight=BOLD)
            t = Text(title_txt, font="sans-serif", font_size=26, color=WHITE, weight=BOLD)
            d = Text(desc_txt, font="sans-serif", font_size=20, color=LIGHT)
            left = VGroup(n, t).arrange(RIGHT, buff=0.3)
            g = VGroup(left, d).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
            g.move_to(box.get_center())
            group = VGroup(box, g)

            self.add_sound(os.path.join(AUDIO_DIR, f"{seg}.mp3"))
            self.play(FadeIn(group, shift=RIGHT * 0.3), run_time=0.8)
            self.wait(2.5)

        self.play(*[FadeOut(m) for m in self.mobjects])

        # 关键词
        k_title = Text("关键词组合示例", font="sans-serif", font_size=36, color=GOLD)
        k_title.to_edge(UP, buff=0.8)
        pairs = VGroup(
            Text("徒步 🆚 逛商场    爬山 🆚 泡温泉", font="sans-serif", font_size=24, color=LIGHT),
            Text("团建 🆚 年会      背包 🆚 行李箱", font="sans-serif", font_size=24, color=LIGHT),
            Text("山顶 🆚 餐厅      运动鞋 🆚 拖鞋", font="sans-serif", font_size=24, color=LIGHT),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        pairs.next_to(k_title, DOWN, buff=0.6)

        self.add_sound(os.path.join(AUDIO_DIR, "02_examples.mp3"))
        self.play(FadeIn(k_title))
        for p in pairs:
            self.play(FadeIn(p), run_time=0.3)
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in self.mobjects])
        self.add_sound(os.path.join(AUDIO_DIR, "02_end.mp3"))
        t1 = Text("比传统「谁是卧底」更贴合出行场景", font="sans-serif", font_size=32, color=GOLD)
        t2 = Text("推理轻、节奏快，适合中段把气氛再次拉起来", font="sans-serif", font_size=24, color=LIGHT)
        VGroup(t1, t2).arrange(DOWN, buff=0.3)
        self.play(FadeIn(t1), FadeIn(t2))
        self.wait(3.0)


# ═══════════════════════════════════════════════════════════
#  游戏 03：即兴配音巴士
# ═══════════════════════════════════════════════════════════
class Game03Dubbing(Scene):
    def construct(self):
        self.camera.background_color = BG

        num = Text("03", font="sans-serif", weight=BOLD, font_size=96, color=ACCENT)
        name = Text("即兴配音巴士", font="sans-serif", weight=BOLD, font_size=60, color=WHITE)
        tag  = Text("场景题 + 情绪题 + 1分钟短剧", font="sans-serif", font_size=28, color=LIGHT)
        VGroup(num, name, tag).arrange(DOWN, buff=0.3)
        self.add_sound(os.path.join(AUDIO_DIR, "03_intro.mp3"))
        self.play(Write(num), Write(name), run_time=1.5)
        self.play(FadeIn(tag), run_time=0.5)
        self.wait(1.0)
        self.play(FadeOut(num), FadeOut(name), FadeOut(tag))

        for seg, num_txt, title_txt, desc_txt in [
            ("03_step1", "1", "分组抽题", "6-8人一组，抽「场景题」+「情绪题」"),
            ("03_step2", "2", "准备1分钟，表演1分钟", "在座位上分配台词，即兴演绎"),
            ("03_step3", "3", "全车投票评奖", "最佳配音组、最佳戏精、最佳反差感"),
        ]:
            box = RoundedRectangle(corner_radius=0.15, width=10, height=1.1,
                                    fill_color=CARD_BG, fill_opacity=0.7,
                                    stroke_color=ACCENT, stroke_width=1)
            n = Text(num_txt, font="sans-serif", font_size=36, color=ACCENT, weight=BOLD)
            t = Text(title_txt, font="sans-serif", font_size=26, color=WHITE, weight=BOLD)
            d = Text(desc_txt, font="sans-serif", font_size=20, color=LIGHT)
            left = VGroup(n, t).arrange(RIGHT, buff=0.3)
            g = VGroup(left, d).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
            g.move_to(box.get_center())
            group = VGroup(box, g)

            self.add_sound(os.path.join(AUDIO_DIR, f"{seg}.mp3"))
            self.play(FadeIn(group, shift=RIGHT * 0.3), run_time=0.8)
            self.wait(2.5)

        self.play(*[FadeOut(m) for m in self.mobjects])

        # 题卡
        c_title = Text("题卡示例", font="sans-serif", font_size=36, color=GOLD)
        c_title.to_edge(UP, buff=0.8)
        content = Text(
            "场景：精英徒步队只带了零食没带水\n        山顶神秘任务 · 大巴变冠军领奖台\n\n"
            "风格：悬疑片 · 新闻联播 · 霸总剧\n        动物世界 · 武侠片 · 选秀导师",
            font="sans-serif", font_size=22, color=LIGHT, line_spacing=0.5
        )
        content.next_to(c_title, DOWN, buff=0.5)
        self.add_sound(os.path.join(AUDIO_DIR, "03_examples.mp3"))
        self.play(FadeIn(c_title), FadeIn(content))
        self.wait(3.0)

        self.play(*[FadeOut(m) for m in self.mobjects])
        self.add_sound(os.path.join(AUDIO_DIR, "03_end.mp3"))
        t1 = Text("综艺效果最强", font="sans-serif", font_size=32, color=GOLD)
        t2 = Text("适合后段提神，控制音量和动作确保行车安全", font="sans-serif", font_size=24, color=LIGHT)
        VGroup(t1, t2).arrange(DOWN, buff=0.3)
        self.play(FadeIn(t1), FadeIn(t2))
        self.wait(3.0)


# ═══════════════════════════════════════════════════════════
#  游戏 04：车厢任务盲盒
# ═══════════════════════════════════════════════════════════
class Game04BlindBox(Scene):
    def construct(self):
        self.camera.background_color = BG

        num = Text("04", font="sans-serif", weight=BOLD, font_size=96, color=ACCENT)
        name = Text("车厢任务盲盒", font="sans-serif", weight=BOLD, font_size=60, color=WHITE)
        tag  = Text("隐藏任务 + 自然触发 + 阶段结算", font="sans-serif", font_size=28, color=LIGHT)
        VGroup(num, name, tag).arrange(DOWN, buff=0.3)
        self.add_sound(os.path.join(AUDIO_DIR, "04_intro.mp3"))
        self.play(Write(num), Write(name), run_time=1.5)
        self.play(FadeIn(tag), run_time=0.5)
        self.wait(1.0)
        self.play(FadeOut(num), FadeOut(name), FadeOut(tag))

        for seg, num_txt, title_txt, desc_txt in [
            ("04_step1", "1", "每人抽取隐藏任务卡", "只有自己知道，不能展示给别人"),
            ("04_step2", "2", "自然互动中完成", "聊天中悄悄完成任务，向主持人认证得分"),
            ("04_step3", "3", "阶段结算积分", "被猜中任务则失败，每15-20分钟结算一次"),
        ]:
            box = RoundedRectangle(corner_radius=0.15, width=10, height=1.1,
                                    fill_color=CARD_BG, fill_opacity=0.7,
                                    stroke_color=ACCENT, stroke_width=1)
            n = Text(num_txt, font="sans-serif", font_size=36, color=ACCENT, weight=BOLD)
            t = Text(title_txt, font="sans-serif", font_size=26, color=WHITE, weight=BOLD)
            d = Text(desc_txt, font="sans-serif", font_size=20, color=LIGHT)
            left = VGroup(n, t).arrange(RIGHT, buff=0.3)
            g = VGroup(left, d).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
            g.move_to(box.get_center())
            group = VGroup(box, g)

            self.add_sound(os.path.join(AUDIO_DIR, f"{seg}.mp3"))
            self.play(FadeIn(group, shift=RIGHT * 0.3), run_time=0.8)
            self.wait(2.5)

        self.play(*[FadeOut(m) for m in self.mobjects])

        # 任务示例
        t_title = Text("任务卡示例", font="sans-serif", font_size=36, color=GOLD)
        t_title.to_edge(UP, buff=0.8)
        tasks = Text(
            "让3个人主动跟你击掌\n让5个人说出「今天一定能登顶」\n"
            "让一个人唱一句歌\n找到同月生日的人\n"
            "让一位同事夸你的装备\n让10个人一起做出发手势",
            font="sans-serif", font_size=22, color=LIGHT, line_spacing=0.35
        )
        tasks.next_to(t_title, DOWN, buff=0.5)
        self.add_sound(os.path.join(AUDIO_DIR, "04_examples.mp3"))
        self.play(FadeIn(t_title), FadeIn(tasks))
        self.wait(3.5)

        self.play(*[FadeOut(m) for m in self.mobjects])
        self.add_sound(os.path.join(AUDIO_DIR, "04_end.mp3"))
        t1 = Text("全程穿插，互动自然", font="sans-serif", font_size=32, color=GOLD)
        t2 = Text("让不爱表演的人也能悄悄参与进来", font="sans-serif", font_size=24, color=LIGHT)
        VGroup(t1, t2).arrange(DOWN, buff=0.3)
        self.play(FadeIn(t1), FadeIn(t2))
        self.wait(3.0)


# ═══════════════════════════════════════════════════════════
#  游戏 05：沿途情报猎人
# ═══════════════════════════════════════════════════════════
class Game05Hunter(Scene):
    def construct(self):
        self.camera.background_color = BG

        num = Text("05", font="sans-serif", weight=BOLD, font_size=96, color=ACCENT)
        name = Text("沿途情报猎人", font="sans-serif", weight=BOLD, font_size=60, color=WHITE)
        tag  = Text("窗外观察 + 小组共创 + 抵达前颁奖", font="sans-serif", font_size=28, color=LIGHT)
        VGroup(num, name, tag).arrange(DOWN, buff=0.3)
        self.add_sound(os.path.join(AUDIO_DIR, "05_intro.mp3"))
        self.play(Write(num), Write(name), run_time=1.5)
        self.play(FadeIn(tag), run_time=0.5)
        self.wait(1.0)
        self.play(FadeOut(num), FadeOut(name), FadeOut(tag))

        for seg, num_txt, title_txt, desc_txt in [
            ("05_step1", "1", "分组发放情报清单", "5-7组，观察窗外、车内、团队状态"),
            ("05_step2", "2", "小组共创打卡", "记录画面、故事、团队角色，完成清单"),
            ("05_step3", "3", "30秒分享 + 颁奖", "展示队名、口号、创意故事，总分最高获奖"),
        ]:
            box = RoundedRectangle(corner_radius=0.15, width=10, height=1.1,
                                    fill_color=CARD_BG, fill_opacity=0.7,
                                    stroke_color=ACCENT, stroke_width=1)
            n = Text(num_txt, font="sans-serif", font_size=36, color=ACCENT, weight=BOLD)
            t = Text(title_txt, font="sans-serif", font_size=26, color=WHITE, weight=BOLD)
            d = Text(desc_txt, font="sans-serif", font_size=20, color=LIGHT)
            left = VGroup(n, t).arrange(RIGHT, buff=0.3)
            g = VGroup(left, d).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
            g.move_to(box.get_center())
            group = VGroup(box, g)

            self.add_sound(os.path.join(AUDIO_DIR, f"{seg}.mp3"))
            self.play(FadeIn(group, shift=RIGHT * 0.3), run_time=0.8)
            self.wait(2.5)

        self.play(*[FadeOut(m) for m in self.mobjects])

        # 清单
        l_title = Text("情报清单示例", font="sans-serif", font_size=36, color=GOLD)
        l_title.to_edge(UP, buff=0.8)
        items = Text(
            "找到最像徒步电影开场的窗外画面\n发现绿色元素招牌\n"
            "给本车起队名 · 设计徒步口号\n"
            "用窗外三个元素编30秒故事\n找到适合拍团建大片的路段",
            font="sans-serif", font_size=22, color=LIGHT, line_spacing=0.35
        )
        items.next_to(l_title, DOWN, buff=0.5)
        self.add_sound(os.path.join(AUDIO_DIR, "05_examples.mp3"))
        self.play(FadeIn(l_title), FadeIn(items))
        self.wait(3.5)

        self.play(*[FadeOut(m) for m in self.mobjects])
        self.add_sound(os.path.join(AUDIO_DIR, "05_end.mp3"))
        t1 = Text("临近目的地使用效果最佳", font="sans-serif", font_size=32, color=GOLD)
        t2 = Text("把车上情绪自然转到下车后的徒步队伍", font="sans-serif", font_size=24, color=LIGHT)
        VGroup(t1, t2).arrange(DOWN, buff=0.3)
        self.play(FadeIn(t1), FadeIn(t2))
        self.wait(3.0)


SCENES = [Game01HotSearch, Game02Undercover, Game03Dubbing, Game04BlindBox, Game05Hunter]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        idx = int(sys.argv[1]) - 1
        if 0 <= idx < len(SCENES):
            pre_generate_all_audio()
            SCENES[idx]().render()
    else:
        print("Usage: python sync_videos.py <1-5>")
