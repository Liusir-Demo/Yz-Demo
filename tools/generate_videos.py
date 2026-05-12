from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
IMG_DIR = ROOT / "assets" / "images"
VIDEO_DIR = ROOT / "assets" / "videos"
SCENE_DIR = ROOT / "assets" / "scenes"

HOST = IMG_DIR / "host.jpg"
LOGO = IMG_DIR / "site-logo.png"
FONT = "C\\:/Windows/Fonts/simhei.ttf"

W, H = 1280, 720


GAMES = [
    ("01-signal", "同频出发局", "隐藏任务卡", "聊天中悄悄完成任务", "互猜揭晓制造笑点", "#0b7f5b"),
    ("02-bullet", "大巴人生弹幕", "手机匿名提交", "主持人随机播报", "全车举手投票接梗", "#138a9e"),
    ("03-auction", "徒步搭子拍卖会", "每人100虚拟积分", "竞拍拍照/补给/导航搭子", "下车直接组成小队", "#d98c20"),
    ("04-show", "车厢微综艺", "抽取今日人设题", "全车投票提名主角", "正向称号带动氛围", "#c95f6a"),
    ("05-blindbox", "路线盲盒共创局", "抽取路线盲盒", "共创队名口号合照动作", "把去程延伸到徒步", "#4f8f35"),
]


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def cover(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    img = img.convert("RGB")
    scale = max(size[0] / img.width, size[1] / img.height)
    resized = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
    left = (resized.width - size[0]) // 2
    top = (resized.height - size[1]) // 2
    return resized.crop((left, top, left + size[0], top + size[1]))


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)
    return mask


def paste_rounded(base: Image.Image, img: Image.Image, box: tuple[int, int], radius: int) -> None:
    mask = rounded_mask(img.size, radius)
    base.paste(img, box, mask)


def draw_bus_scene(path: Path, title_slug: str, accent_hex: str) -> None:
    accent = hex_to_rgb(accent_hex)
    base = Image.new("RGB", (W, H), "#f9fbef")
    draw = ImageDraw.Draw(base)

    for y in range(H):
        t = y / H
        r = int(246 * (1 - t) + 214 * t)
        g = int(252 * (1 - t) + 240 * t)
        b = int(224 * (1 - t) + 206 * t)
        draw.line((0, y, W, y), fill=(r, g, b))

    draw.rounded_rectangle((70, 44, 1210, 680), radius=34, fill="#fffdf4", outline="#d7e5c9", width=3)
    draw.rounded_rectangle((130, 92, 1150, 315), radius=28, fill="#ccebd9", outline="#8ac6aa", width=4)
    draw.rectangle((166, 126, 1114, 300), fill="#bfe6dc")

    for x in range(190, 1050, 138):
        draw.rounded_rectangle((x, 332, x + 96, 565), radius=22, fill="#22423b")
        draw.rounded_rectangle((x + 10, 340, x + 86, 456), radius=18, fill="#2f5b51")
        draw.rounded_rectangle((x + 12, 462, x + 84, 610), radius=18, fill="#1b332f")

    colors = ["#f7b267", "#79b473", "#5aa9e6", "#f25f5c", "#b388eb", "#ffd166"]
    for i, x in enumerate([238, 382, 540, 706, 864, 1014]):
        y = 410 if i % 2 else 385
        c = colors[i % len(colors)]
        draw.ellipse((x, y, x + 46, y + 46), fill=c, outline="#12312b", width=3)
        draw.rounded_rectangle((x - 14, y + 54, x + 60, y + 140), radius=24, fill=c, outline="#12312b", width=3)

    host = cover(Image.open(HOST), (300, 390)).filter(ImageFilter.UnsharpMask(radius=1.2, percent=115))
    draw.rounded_rectangle((74, 264, 406, 678), radius=28, fill="#ffffff", outline="#f4b95a", width=6)
    paste_rounded(base, host, (90, 280), 22)
    draw.rounded_rectangle((94, 592, 390, 652), radius=18, fill=accent)
    draw.ellipse((340, 536, 388, 584), fill="#ffffff", outline=accent, width=5)
    draw.line((364, 584, 364, 640), fill="#ffffff", width=7)

    logo = cover(Image.open(LOGO), (150, 90))
    paste_rounded(base, logo, (980, 92), 12)

    draw.rounded_rectangle((450, 560, 1130, 632), radius=22, fill="#ffffff", outline="#d8e7ce", width=2)
    for i in range(4):
        x = 486 + i * 152
        draw.rounded_rectangle((x, 582, x + 118, 604), radius=11, fill=accent)

    base.save(path, quality=92)


def draw_hero() -> None:
    draw_bus_scene(IMG_DIR / "hero-bus-host.jpg", "hero", "#0b7f5b")


def q(text: str) -> str:
    return text.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")


def drawtext(text: str, x: str, y: str, size: int, color: str, extra: str = "") -> str:
    return f"drawtext=fontfile='{FONT}':text='{q(text)}':x={x}:y={y}:fontsize={size}:fontcolor={color}{extra}"


def make_video(slug: str, title: str, step1: str, step2: str, step3: str, accent: str) -> None:
    scene = SCENE_DIR / f"{slug}.jpg"
    draw_bus_scene(scene, slug, accent)
    out = VIDEO_DIR / f"{slug}.mp4"

    filters = [
        "scale=1320:742",
        "crop=1280:720:x='20+10*sin(2*PI*t/10)':y=11",
        "format=yuv420p",
        "drawbox=x=0:y=0:w=1280:h=720:color=0x082c24@0.16:t=fill",
        "drawbox=x=42:y=38:w=1196:h=644:color=0xffffff@0.18:t=2",
        f"drawbox=x=70:y=70:w=420:h=72:color={accent.replace('#', '0x')}@0.92:t=fill",
        drawtext(title, "92", "82", 42, "white"),
        drawtext("真人主持人演示 · 大巴车内互动玩法", "92", "155", 28, "white"),
        "drawbox=x=70:y=510:w=1140:h=116:color=0xffffff@0.88:t=fill",
        drawtext("0-3秒  " + step1, "110", "528", 30, "0x082c24", ":enable='between(t,0,3.2)'"),
        drawtext("3-6秒  " + step2, "110", "528", 30, "0x082c24", ":enable='between(t,3.2,6.6)'"),
        drawtext("6-9秒  " + step3, "110", "528", 30, "0x082c24", ":enable='between(t,6.6,9.1)'"),
        drawtext("9-10秒  安全坐姿 · 全员参与 · 去程热场", "110", "528", 30, "0x082c24", ":enable='gte(t,9.1)'"),
        f"drawbox=x=110:y=594:w='1060*t/10':h=12:color={accent.replace('#', '0x')}:t=fill",
        "drawbox=x=110:y=594:w=1060:h=12:color=0x082c24@0.18:t=2",
    ]

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loop",
            "1",
            "-i",
            str(scene),
            "-t",
            "10",
            "-r",
            "24",
            "-vf",
            ",".join(filters),
            "-an",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(out),
        ],
        check=True,
    )
    print(out)


def main() -> None:
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    SCENE_DIR.mkdir(parents=True, exist_ok=True)
    draw_hero()
    for game in GAMES:
        make_video(*game)


if __name__ == "__main__":
    main()
