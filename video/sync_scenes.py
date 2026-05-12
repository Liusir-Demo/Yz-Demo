"""
音画同步 manim 场景 - 每一步画面独立，不重叠
"""
from manim import *
import json
import os

TIMING_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                           "video_output", "sync_audio", "timing.json")

BG = "#1a1a2e"
ACCENT = "#e94560"
GOLD = "#f5c518"
WHITE = "#ffffff"
LIGHT = "#c8d6e5"
CARD_BG = "#16213e"


def load_timing(game_num):
    with open(TIMING_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data[f"{game_num:02d}"]


def make_step_box(num_txt, title_txt, desc_txt):
    box = RoundedRectangle(corner_radius=0.15, width=10, height=1.1,
                           fill_color=CARD_BG, fill_opacity=0.7,
                           stroke_color=ACCENT, stroke_width=1)
    n = Text(num_txt, font="sans-serif", font_size=36, color=ACCENT, weight=BOLD)
    t = Text(title_txt, font="sans-serif", font_size=26, color=WHITE, weight=BOLD)
    d = Text(desc_txt, font="sans-serif", font_size=20, color=LIGHT)
    left = VGroup(n, t).arrange(RIGHT, buff=0.3)
    g = VGroup(left, d).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
    g.move_to(box.get_center())
    return VGroup(box, g)


def rule_dot(icon, text):
    """规则行（圆点 + 文字）"""
    dot = Dot(color=ACCENT, radius=0.12)
    txt = Text(text, font="sans-serif", font_size=24, color=LIGHT)
    return VGroup(dot, txt).arrange(RIGHT, buff=0.35, aligned_edge=LEFT)


# ═══════════════════════════════════════════
#  通用模板
# ═══════════════════════════════════════════
def build_game(scene, game_num, game_name, tagline, steps_data, rules_title, rules_items, end_line1, end_line2):
    """统一构建逻辑：每一步独立画面，不重叠"""
    t = load_timing(game_num)
    scene.camera.background_color = BG

    # ── 1. 标题画面 ──
    title_objs = VGroup(
        Text(f"{game_num:02d}", font="sans-serif", weight=BOLD, font_size=96, color=ACCENT),
        Text(game_name, font="sans-serif", weight=BOLD, font_size=60, color=WHITE),
        Text(tagline, font="sans-serif", font_size=28, color=LIGHT),
    ).arrange(DOWN, buff=0.3)
    scene.play(Write(title_objs[0]), Write(title_objs[1]), run_time=1.0)
    scene.play(FadeIn(title_objs[2]), run_time=0.5)
    scene.wait(t["intro"]["dur"] - 1.5)
    scene.play(FadeOut(title_objs))

    # ── 2. 步骤画面（逐一展示，先清再放） ──
    current = None
    for i, (sn, st, sd) in enumerate(steps_data):
        if current is not None:
            scene.play(FadeOut(current), run_time=0.3)
        box = make_step_box(sn, st, sd)
        scene.play(FadeIn(box, shift=RIGHT * 0.3), run_time=0.5)
        scene.wait(t["steps"][i]["dur"] - 0.5)
        current = box
    if current is not None:
        scene.play(FadeOut(current), run_time=0.3)

    # ── 3. 规则/示例画面 ──
    rt = Text(rules_title, font="sans-serif", font_size=36, color=GOLD)
    rt.to_edge(UP, buff=0.8)
    rc = VGroup(*[rule_dot("", item) for item in rules_items]).arrange(
        DOWN, buff=0.35, aligned_edge=LEFT)
    rc.next_to(rt, DOWN, buff=0.7)
    scene.play(FadeIn(rt))
    for item in rc:
        scene.play(FadeIn(item, shift=UP * 0.15), run_time=0.25)
    rule_anim_time = 0.3 + 0.25 * len(rules_items)
    scene.wait(t["rules"]["dur"] - rule_anim_time)
    scene.play(FadeOut(rt), FadeOut(rc))

    # ── 4. 结尾画面 ──
    e1 = Text(end_line1, font="sans-serif", font_size=32, color=GOLD)
    e2 = Text(end_line2, font="sans-serif", font_size=24, color=LIGHT)
    VGroup(e1, e2).arrange(DOWN, buff=0.3)
    scene.play(FadeIn(e1), FadeIn(e2))
    scene.wait(t["end"]["dur"])


# ═══════════════════════════════════════════
#  Game 01
# ═══════════════════════════════════════════
class Game01Synced(Scene):
    def construct(self):
        build_game(self, 1, "车厢热搜榜", "匿名投票 + 现场揭晓 + 轻量回应",
            [("1", "主持人抛出热搜话题", "例如「最像徒步领队的人」"),
             ("2", "全员匿名投票", "微信群/小程序，30秒内完成"),
             ("3", "现场揭晓前三名", "被点名者完成获奖感言或出征姿势")],
            "规则要点",
            ["不能投自己",
             "回应任务保持轻量，不强迫表演",
             "话题只做友好调侃，避开敏感内容"],
            "适合开场快速破冰",
            "让全车在不强迫表演的情况下进入团建气氛")


# ═══════════════════════════════════════════
#  Game 02
# ═══════════════════════════════════════════
class Game02Synced(Scene):
    def construct(self):
        build_game(self, 2, "大巴卧底旅行团", "隐藏身份 + 一句话发言 + 轻推理",
            [("1", "主持人私发身份", "多数人拿同一个关键词，5名卧底拿相近但不同的词"),
             ("2", "每轮一句话描述", "不能直接说出关键词，根据发言找卧底"),
             ("3", "全车投票淘汰", "每轮淘汰1-2人，卧底坚持到最后3人则获胜")],
            "关键词组合示例",
            ["徒步 vs 逛商场      爬山 vs 泡温泉",
             "团建 vs 年会        背包 vs 行李箱",
             "山顶 vs 餐厅        运动鞋 vs 拖鞋"],
            "比传统「谁是卧底」更贴合出行场景",
            "推理轻、节奏快，适合中段把气氛再次拉起来")


# ═══════════════════════════════════════════
#  Game 03
# ═══════════════════════════════════════════
class Game03Synced(Scene):
    def construct(self):
        build_game(self, 3, "即兴配音巴士", "场景题 + 情绪题 + 1分钟短剧",
            [("1", "分组抽题", "6-8人一组，抽「场景题」+「情绪题」"),
             ("2", "准备1分钟，表演1分钟", "在座位上分配台词，即兴演绎"),
             ("3", "全车投票评奖", "最佳配音组、最佳戏精、最佳反差感")],
            "题卡示例",
            ["场景：精英徒步队只带了零食没带水 / 山顶神秘任务",
             "场景：大巴变冠军领奖台 / 户外纪录片解说员",
             "风格：悬疑片 / 新闻联播 / 霸总剧 / 武侠片 / 选秀导师"],
            "综艺效果最强",
            "适合后段提神，控制音量和动作确保行车安全")


# ═══════════════════════════════════════════
#  Game 04
# ═══════════════════════════════════════════
class Game04Synced(Scene):
    def construct(self):
        build_game(self, 4, "车厢任务盲盒", "隐藏任务 + 自然触发 + 阶段结算",
            [("1", "每人抽取隐藏任务卡", "只有自己知道，不能展示给别人"),
             ("2", "自然互动中完成", "聊天中悄悄完成任务，向主持人认证得分"),
             ("3", "阶段结算积分", "被猜中任务则失败，每15-20分钟结算一次")],
            "任务卡示例",
            ["让3个人主动跟你击掌",
             "让5个人说出「今天一定能登顶」",
             "让一个人唱一句歌 / 找到同月生日的人",
             "让一位同事夸你的装备 / 让10个人做出发手势"],
            "全程穿插，互动自然",
            "让不爱表演的人也能悄悄参与进来")


# ═══════════════════════════════════════════
#  Game 05
# ═══════════════════════════════════════════
class Game05Synced(Scene):
    def construct(self):
        build_game(self, 5, "沿途情报猎人", "窗外观察 + 小组共创 + 抵达前颁奖",
            [("1", "分组发放情报清单", "5-7组，观察窗外、车内、团队状态"),
             ("2", "小组共创打卡", "记录画面、故事、团队角色，完成清单任务"),
             ("3", "30秒分享 + 颁奖", "展示队名、口号、创意故事，总分最高获奖")],
            "情报清单示例",
            ["找到最像徒步电影开场的窗外画面",
             "发现绿色元素招牌 / 给本车起队名",
             "设计徒步口号 / 用窗外三个元素编30秒故事",
             "找到适合拍团建大片的路段"],
            "临近目的地使用效果最佳",
            "把车上情绪自然转到下车后的徒步队伍")
