"""
大巴团建互动游戏 - 5个介绍玩法视频 (manim 动画)
每个视频 60-90 秒，展示游戏名称、核心玩法、规则要点
"""
from manim import *
import os

# 输出目录
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "video_output")

# ── 配色 ──────────────────────────────────────────────
BG      = "#1a1a2e"
ACCENT  = "#e94560"
GOLD    = "#f5c518"
WHITE   = "#ffffff"
LIGHT   = "#c8d6e5"
CARD_BG = "#16213e"
GREEN   = "#0f9b58"

# ── 通用标题 Scene ────────────────────────────────────
class GameBase(Scene):
    game_num  = "00"
    game_name = ""
    game_tagline = ""
    duration  = ""
    players   = ""
    props     = ""

    def build_title(self, t=1.0):
        """统一的标题动画"""
        num = Text(self.game_num, font="sans-serif", weight=BOLD, font_size=96, color=ACCENT)
        name = Text(self.game_name, font="sans-serif", weight=BOLD, font_size=60, color=WHITE)
        tag  = Text(self.game_tagline, font="sans-serif", font_size=28, color=LIGHT)
        group = VGroup(num, name, tag).arrange(DOWN, buff=0.3)
        num.next_to(name, UP, buff=0.2)
        self.play(Write(num), Write(name), run_time=t)
        self.play(FadeIn(tag), run_time=0.8)
        self.wait(0.5)
        return group

    def build_meta_bar(self):
        """显示参与人数/时长/道具"""
        meta = Text(
            f"参与：{self.players}  |  时长：{self.duration}  |  道具：{self.props}",
            font="sans-serif", font_size=22, color=LIGHT
        )
        meta.to_edge(DOWN, buff=0.6)
        underline = Line(LEFT, RIGHT, color=ACCENT, stroke_width=2)
        underline.set_width(meta.get_width() + 0.4)
        underline.next_to(meta, DOWN, buff=0.15)
        self.play(FadeIn(meta), GrowFromEdge(underline, LEFT))
        return VGroup(meta, underline)


class Game01HotSearch(GameBase):
    """车厢热搜榜"""
    game_num     = "01"
    game_name    = "车厢热搜榜"
    game_tagline = "匿名投票 + 现场揭晓 + 轻量回应"
    duration     = "15-20分钟"
    players      = "全员"
    props        = "投票工具、题卡、奖品"

    def construct(self):
        self.camera.background_color = BG

        # ── 标题 ──
        self.build_title()
        self.build_meta_bar()
        self.wait(0.5)

        # ── 切换画面 ──
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        # ── 核心玩法步骤 ──
        title = Text("🎯 核心玩法", font="sans-serif", font_size=40, color=GOLD)
        title.to_edge(UP, buff=0.8)
        self.play(FadeIn(title))

        steps = VGroup(
            self._step_box("1", "主持人抛出热搜话题", "例如「最像徒步领队的人」"),
            self._step_box("2", "全员匿名投票", "微信群投票 / 小程序，30秒内完成"),
            self._step_box("3", "现场揭晓前三名", "被点名者完成获奖感言或出征姿势"),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        steps.next_to(title, DOWN, buff=0.7)

        for i, step in enumerate(steps):
            self.play(FadeIn(step, shift=RIGHT * 0.3), run_time=0.6)
            self.wait(0.3)

        self.wait(0.8)

        # ── 规则画面 ──
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        rule_title = Text("规则要点", font="sans-serif", font_size=40, color=GOLD)
        rule_title.to_edge(UP, buff=0.8)
        self.play(FadeIn(rule_title))

        rules = VGroup(
            self._rule_item("不能投自己"),
            self._rule_item("回应任务保持轻量，不强迫表演"),
            self._rule_item("话题只做友好调侃，避开敏感内容"),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        rules.next_to(rule_title, DOWN, buff=0.7)

        for rule in rules:
            self.play(FadeIn(rule, shift=UP * 0.2), run_time=0.4)
            self.wait(0.2)

        self.wait(1)

        # ── 结束语 ──
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self._end_card("适合开场快速破冰", "让全车在不强迫表演的情况下进入团建气氛")

    def _step_box(self, num, title, desc):
        box = RoundedRectangle(corner_radius=0.15, width=10, height=1.1, fill_color=CARD_BG, fill_opacity=0.7, stroke_color=ACCENT, stroke_width=1)
        num_t   = Text(num, font="sans-serif", font_size=36, color=ACCENT, weight=BOLD)
        title_t = Text(title, font="sans-serif", font_size=26, color=WHITE, weight=BOLD)
        desc_t  = Text(desc, font="sans-serif", font_size=20, color=LIGHT)
        left = VGroup(num_t, title_t).arrange(RIGHT, buff=0.3)
        group = VGroup(left, desc_t).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        group.move_to(box.get_center())
        return VGroup(box, group)

    def _rule_item(self, text):
        dot = Dot(color=ACCENT, radius=0.12)
        txt = Text(text, font="sans-serif", font_size=24, color=LIGHT)
        return VGroup(dot, txt).arrange(RIGHT, buff=0.35, aligned_edge=LEFT)

    def _end_card(self, line1, line2):
        t1 = Text(line1, font="sans-serif", font_size=32, color=GOLD)
        t2 = Text(line2, font="sans-serif", font_size=24, color=LIGHT)
        VGroup(t1, t2).arrange(DOWN, buff=0.3)
        self.play(FadeIn(t1), FadeIn(t2))
        self.wait(2)


class Game02Undercover(GameBase):
    """大巴卧底旅行团"""
    game_num     = "02"
    game_name    = "大巴卧底旅行团"
    game_tagline = "隐藏身份 + 一句话发言 + 轻推理"
    duration     = "20-25分钟"
    players      = "12-35人"
    props        = "身份卡、关键词题库"

    def construct(self):
        self.camera.background_color = BG

        self.build_title()
        self.build_meta_bar()
        self.wait(0.5)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        # 核心玩法
        title = Text("🎯 核心玩法", font="sans-serif", font_size=40, color=GOLD)
        title.to_edge(UP, buff=0.8)
        self.play(FadeIn(title))

        steps = VGroup(
            self._step("1", "主持人私发身份", "35人设5名卧底，其余人拿同一关键词"),
            self._step("2", "每轮一句话描述", "不能直接说出关键词，根据发言找卧底"),
            self._step("3", "投票淘汰", "每轮淘汰1-2人，卧底坚持到最后3人则获胜"),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        steps.next_to(title, DOWN, buff=0.7)

        for step in steps:
            self.play(FadeIn(step, shift=RIGHT * 0.3), run_time=0.6)
            self.wait(0.3)

        self.wait(0.5)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        # 关键词展示
        k_title = Text("关键词组合示例", font="sans-serif", font_size=36, color=GOLD)
        k_title.to_edge(UP, buff=0.8)
        self.play(FadeIn(k_title))

        pairs = [
            ("徒步 🆚 逛商场", "爬山 🆚 泡温泉"),
            ("团建 🆚 年会", "背包 🆚 行李箱"),
            ("山顶 🆚 餐厅", "运动鞋 🆚 拖鞋"),
        ]
        pair_groups = VGroup()
        for i, (left, right) in enumerate(pairs):
            p = Text(f"{left}        {right}", font="sans-serif", font_size=24, color=LIGHT)
            pair_groups.add(p)
        pair_groups.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        pair_groups.next_to(k_title, DOWN, buff=0.6)

        for p in pair_groups:
            self.play(FadeIn(p), run_time=0.4)
            self.wait(0.2)

        self.wait(0.5)

        # 规则
        rule = Text("规则：每人每轮只说一句话 · 不能直接说关键词 · 推理轻、节奏快", font="sans-serif", font_size=22, color=LIGHT)
        rule.to_edge(DOWN, buff=1)
        self.play(FadeIn(rule))
        self.wait(1.5)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self._end("中段提神利器", "比传统「谁是卧底」更贴合出行场景")

    def _step(self, num, title, desc):
        box = RoundedRectangle(corner_radius=0.15, width=10, height=1.1, fill_color=CARD_BG, fill_opacity=0.7, stroke_color=ACCENT, stroke_width=1)
        num_t   = Text(num, font="sans-serif", font_size=36, color=ACCENT, weight=BOLD)
        title_t = Text(title, font="sans-serif", font_size=26, color=WHITE, weight=BOLD)
        desc_t  = Text(desc, font="sans-serif", font_size=20, color=LIGHT)
        left = VGroup(num_t, title_t).arrange(RIGHT, buff=0.3)
        group = VGroup(left, desc_t).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        group.move_to(box.get_center())
        return VGroup(box, group)

    def _end(self, line1, line2):
        t1 = Text(line1, font="sans-serif", font_size=32, color=GOLD)
        t2 = Text(line2, font="sans-serif", font_size=24, color=LIGHT)
        VGroup(t1, t2).arrange(DOWN, buff=0.3)
        self.play(FadeIn(t1), FadeIn(t2))
        self.wait(2)


class Game03Dubbing(GameBase):
    """即兴配音巴士"""
    game_num     = "03"
    game_name    = "即兴配音巴士"
    game_tagline = "场景题 + 情绪题 + 1分钟短剧"
    duration     = "20分钟"
    players      = "每轮6-10人"
    props        = "题卡、音效、奖品"

    def construct(self):
        self.camera.background_color = BG

        self.build_title()
        self.build_meta_bar()
        self.wait(0.5)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        title = Text("🎯 核心玩法", font="sans-serif", font_size=40, color=GOLD)
        title.to_edge(UP, buff=0.8)
        self.play(FadeIn(title))

        steps = VGroup(
            self._step("1", "分组抽题", "6-8人一组，抽「场景题」+「情绪题」"),
            self._step("2", "准备1分钟，表演1分钟", "在座位上分配台词，即兴演绎"),
            self._step("3", "全车投票", "评出最佳配音组、最佳戏精、最佳反差感"),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        steps.next_to(title, DOWN, buff=0.7)

        for step in steps:
            self.play(FadeIn(step, shift=RIGHT * 0.3), run_time=0.6)
            self.wait(0.3)

        self.wait(0.5)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        # 题卡
        c_title = Text("题卡示例", font="sans-serif", font_size=36, color=GOLD)
        c_title.to_edge(UP, buff=0.8)
        self.play(FadeIn(c_title))

        scenes = Text("场景：精英徒步队只带了零食没带水 · 山顶神秘任务 · 大巴变冠军领奖台\n\n风格：悬疑片 · 新闻联播 · 霸总剧 · 动物世界 · 武侠片 · 选秀导师",
                      font="sans-serif", font_size=22, color=LIGHT, line_spacing=0.4)
        scenes.next_to(c_title, DOWN, buff=0.5)
        self.play(FadeIn(scenes))
        self.wait(1.5)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        self._end("综艺效果最强", "适合后段提神，控制音量和动作确保行车安全")

    def _step(self, num, title, desc):
        box = RoundedRectangle(corner_radius=0.15, width=10, height=1.1, fill_color=CARD_BG, fill_opacity=0.7, stroke_color=ACCENT, stroke_width=1)
        num_t   = Text(num, font="sans-serif", font_size=36, color=ACCENT, weight=BOLD)
        title_t = Text(title, font="sans-serif", font_size=26, color=WHITE, weight=BOLD)
        desc_t  = Text(desc, font="sans-serif", font_size=20, color=LIGHT)
        left = VGroup(num_t, title_t).arrange(RIGHT, buff=0.3)
        group = VGroup(left, desc_t).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        group.move_to(box.get_center())
        return VGroup(box, group)

    def _end(self, line1, line2):
        t1 = Text(line1, font="sans-serif", font_size=32, color=GOLD)
        t2 = Text(line2, font="sans-serif", font_size=24, color=LIGHT)
        VGroup(t1, t2).arrange(DOWN, buff=0.3)
        self.play(FadeIn(t1), FadeIn(t2))
        self.wait(2)


class Game04BlindBox(GameBase):
    """车厢任务盲盒"""
    game_num     = "04"
    game_name    = "车厢任务盲盒"
    game_tagline = "隐藏任务 + 自然触发 + 阶段结算"
    duration     = "全程穿插"
    players      = "全员"
    props        = "35张任务卡"

    def construct(self):
        self.camera.background_color = BG

        self.build_title()
        self.build_meta_bar()
        self.wait(0.5)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        title = Text("🎯 核心玩法", font="sans-serif", font_size=40, color=GOLD)
        title.to_edge(UP, buff=0.8)
        self.play(FadeIn(title))

        steps = VGroup(
            self._step("1", "每人抽取隐藏任务卡", "不能给别人看，只有自己知道任务"),
            self._step("2", "自然互动中完成", "聊天、互动时悄悄完成，向主持人认证"),
            self._step("3", "阶段结算积分", "每15-20分钟结算一次，积分最高者获奖"),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        steps.next_to(title, DOWN, buff=0.7)

        for step in steps:
            self.play(FadeIn(step, shift=RIGHT * 0.3), run_time=0.6)
            self.wait(0.3)

        self.wait(0.5)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        # 任务卡示例
        t_title = Text("任务卡示例", font="sans-serif", font_size=36, color=GOLD)
        t_title.to_edge(UP, buff=0.8)
        self.play(FadeIn(t_title))

        tasks = Text(
            "让3个人主动跟你击掌\n让5个人说出「今天一定能登顶」\n让一个人唱一句歌\n找到同月生日的人\n让一位同事夸你的装备\n让10个人一起做出发手势",
            font="sans-serif", font_size=22, color=LIGHT, line_spacing=0.3
        )
        tasks.next_to(t_title, DOWN, buff=0.5)
        self.play(FadeIn(tasks))
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        self._end("全程穿插，互动自然", "让不爱表演的人也能悄悄参与进来")

    def _step(self, num, title, desc):
        box = RoundedRectangle(corner_radius=0.15, width=10, height=1.1, fill_color=CARD_BG, fill_opacity=0.7, stroke_color=ACCENT, stroke_width=1)
        num_t   = Text(num, font="sans-serif", font_size=36, color=ACCENT, weight=BOLD)
        title_t = Text(title, font="sans-serif", font_size=26, color=WHITE, weight=BOLD)
        desc_t  = Text(desc, font="sans-serif", font_size=20, color=LIGHT)
        left = VGroup(num_t, title_t).arrange(RIGHT, buff=0.3)
        group = VGroup(left, desc_t).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        group.move_to(box.get_center())
        return VGroup(box, group)

    def _end(self, line1, line2):
        t1 = Text(line1, font="sans-serif", font_size=32, color=GOLD)
        t2 = Text(line2, font="sans-serif", font_size=24, color=LIGHT)
        VGroup(t1, t2).arrange(DOWN, buff=0.3)
        self.play(FadeIn(t1), FadeIn(t2))
        self.wait(2)


class Game05Hunter(GameBase):
    """沿途情报猎人"""
    game_num     = "05"
    game_name    = "沿途情报猎人"
    game_tagline = "窗外观察 + 小组共创 + 抵达前颁奖"
    duration     = "20-30分钟"
    players      = "5-7组（每组5-7人）"
    props        = "情报清单、笔、奖品"

    def construct(self):
        self.camera.background_color = BG

        self.build_title()
        self.build_meta_bar()
        self.wait(0.5)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        title = Text("🎯 核心玩法", font="sans-serif", font_size=40, color=GOLD)
        title.to_edge(UP, buff=0.8)
        self.play(FadeIn(title))

        steps = VGroup(
            self._step("1", "分组发放情报清单", "5-7组，观察窗外、车内、团队状态"),
            self._step("2", "小组共创打卡", "记录画面、故事、团队角色，完成清单任务"),
            self._step("3", "30秒分享 + 颁奖", "代表分享队名、口号、故事，总分最高获奖"),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        steps.next_to(title, DOWN, buff=0.7)

        for step in steps:
            self.play(FadeIn(step, shift=RIGHT * 0.3), run_time=0.6)
            self.wait(0.3)

        self.wait(0.5)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        # 清单示例
        l_title = Text("情报清单示例", font="sans-serif", font_size=36, color=GOLD)
        l_title.to_edge(UP, buff=0.8)
        self.play(FadeIn(l_title))

        items = Text(
            "找到最像徒步电影开场的窗外画面\n发现绿色元素招牌 · 给本车起队名\n设计徒步口号 · 找适合拍团建大片的路段\n用窗外三个元素编30秒故事",
            font="sans-serif", font_size=22, color=LIGHT, line_spacing=0.3
        )
        items.next_to(l_title, DOWN, buff=0.5)
        self.play(FadeIn(items))
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        self._end("临近目的地使用效果最佳", "把车上情绪自然转到下车后的徒步队伍")

    def _step(self, num, title, desc):
        box = RoundedRectangle(corner_radius=0.15, width=10, height=1.1, fill_color=CARD_BG, fill_opacity=0.7, stroke_color=ACCENT, stroke_width=1)
        num_t   = Text(num, font="sans-serif", font_size=36, color=ACCENT, weight=BOLD)
        title_t = Text(title, font="sans-serif", font_size=26, color=WHITE, weight=BOLD)
        desc_t  = Text(desc, font="sans-serif", font_size=20, color=LIGHT)
        left = VGroup(num_t, title_t).arrange(RIGHT, buff=0.3)
        group = VGroup(left, desc_t).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        group.move_to(box.get_center())
        return VGroup(box, group)

    def _end(self, line1, line2):
        t1 = Text(line1, font="sans-serif", font_size=32, color=GOLD)
        t2 = Text(line2, font="sans-serif", font_size=24, color=LIGHT)
        VGroup(t1, t2).arrange(DOWN, buff=0.3)
        self.play(FadeIn(t1), FadeIn(t2))
        self.wait(2)


# ── 批量渲染入口 ──
SCENES = [
    Game01HotSearch,
    Game02Undercover,
    Game03Dubbing,
    Game04BlindBox,
    Game05Hunter,
]

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        idx = int(sys.argv[1]) - 1
        if 0 <= idx < len(SCENES):
            scene = SCENES[idx]
            scene().render()
            print(f"DONE: {scene.__name__}")
        else:
            print(f"Invalid index: {idx+1}, must be 1-5")
    else:
        print("Usage: python generate_videos.py <1-5>")
        for i, s in enumerate(SCENES):
            print(f"  {i+1} = {s.__name__}")
