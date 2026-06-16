"""IG初回カルーセル v5 — アカウント紹介（4枚）。テイストはv4を維持。
名称: AIコーチこれから｜やさしいAI活用研究室 / 伴走のメッセージ。
鉄則: テキスト帯(上 y<=530)とビジュアル帯(下 y>=560)を分離→文字と人物/植物を重ねない。
芽の成長: 種→発芽→双葉→花。背景は1→4で少しずつ明るく。
"""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = H = 1080
ML = 96
INK = (20, 40, 70); INK2 = (52, 76, 110)
GREEN = (92, 144, 90); GREEN_D = (70, 118, 70); GREEN2 = (152, 190, 142)
GRAYT = (82, 98, 90); SOIL = (132, 104, 76); GOLD = (246, 206, 92); PETAL = (250, 214, 150)
FB = "C:/Windows/Fonts/YuGothB.ttc"; FM = "C:/Windows/Fonts/YuGothM.ttc"
ICON = "C:/Users/takanori.koyama/Desktop/Claude/sns-assets/icon"
OUT = "C:/Users/takanori.koyama/Desktop/Claude/sns-assets/images"
FACES = {k: Image.open(f"{ICON}/coach-{k}.png").convert("RGBA")
         for k in ("thinking", "happy", "smile", "sheepish")}
_GRAIN = Image.effect_noise((W, H), 18).convert("L")


def Fnt(p, s):
    return ImageFont.truetype(p, s)


def bg(top, bot):
    img = Image.new("RGB", (W, H), top)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = (y / H) ** 1.1
        d.line([(0, y), (W, y)], fill=tuple(int(top[i] * (1 - t) + bot[i] * t) for i in range(3)))
    img = img.convert("RGBA")
    img.alpha_composite(Image.merge("RGBA", (_GRAIN, _GRAIN, _GRAIN, Image.new("L", (W, H), 8))))
    return img


def glow(img, cx, cy, R, color=GOLD, max_a=80, steps=30):
    for i in range(steps):
        r = R * (1 - i / steps)
        a = int(max_a * (i / steps) ** 1.5)
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(layer).ellipse((cx - r, cy - r, cx + r, cy + r), fill=color + (a,))
        img.alpha_composite(layer)


def coach(img, face, size, xy, flip=False, feather=34):
    im = FACES[face].resize((size, size), Image.LANCZOS)
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((feather, feather, size - feather, size - feather), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(feather * 0.7))
    img.paste(im, xy, mask)


def leaf(d, x, y, size, side, color):
    if side < 0:
        d.ellipse((x - size, y - size * 0.55, x + size * 0.12, y + size * 0.55), fill=color)
    else:
        d.ellipse((x - size * 0.12, y - size * 0.55, x + size, y + size * 0.55), fill=color)


def plant(d, x, by, stage, s=1.0):
    if stage == 0:
        d.ellipse((x - 24 * s, by - 42 * s, x + 24 * s, by), fill=SOIL)
        d.arc((x - 24 * s, by - 42 * s, x + 24 * s, by), 200, 340, fill=(96, 74, 56), width=int(4 * s))
        return
    if stage == 1:
        d.line([(x, by), (x, by - 70 * s)], fill=GREEN, width=int(13 * s))
        leaf(d, x + 8 * s, by - 80 * s, 42 * s, 1, GREEN2)
        return
    if stage == 2:
        d.line([(x, by), (x, by - 100 * s)], fill=GREEN, width=int(14 * s))
        leaf(d, x, by - 112 * s, 66 * s, -1, GREEN)
        leaf(d, x, by - 112 * s, 66 * s, 1, GREEN2)
        return
    # 4: 花
    d.line([(x, by), (x, by - 215 * s)], fill=GREEN, width=int(15 * s))
    leaf(d, x, by - 88 * s, 60 * s, -1, GREEN)
    leaf(d, x, by - 142 * s, 64 * s, 1, GREEN2)
    cx, cy = x, by - 250 * s
    for ang in range(0, 360, 72):
        dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        d.ellipse((cx + dx * 40 * s - 36 * s, cy + dy * 40 * s - 36 * s,
                   cx + dx * 40 * s + 36 * s, cy + dy * 40 * s + 36 * s), fill=PETAL)
    d.ellipse((cx - 30 * s, cy - 30 * s, cx + 30 * s, cy + 30 * s), fill=GOLD)


def counter(img, idx, n=4):
    ImageDraw.Draw(img).text((W - 150, 66), f"{idx + 1} / {n}", font=Fnt(FM, 30), fill=INK2)


def L(d, t, f, x, y, fill):
    d.text((x, y), t, font=f, fill=fill)


def save(img, n):
    img.convert("RGB").save(f"{OUT}/ig-carousel-{n}.jpg", "JPEG", quality=92)


# ===== P1: 表紙（コンセプトの一言） / 種 =====
img = bg((226, 236, 219), (208, 224, 204))
d = ImageDraw.Draw(img)
L(d, "AIに興味はあるけど、何から…という方へ。", Fnt(FM, 36), ML, 165, GRAYT)
L(d, "AI、むずかしく", Fnt(FB, 108), ML, 255, INK)
L(d, "考えなくていい。", Fnt(FB, 108), ML, 395, INK)
plant(d, 540, 900, 0, s=3.0)  # 種
counter(img, 0)
save(img, 1)

# ===== P2: こんな方へ（共感） / 発芽 =====
img = bg((231, 239, 222), (214, 230, 209))
d = ImageDraw.Draw(img)
L(d, "記事は見る。すごいのも分かる。", Fnt(FM, 36), ML, 165, GRAYT)
L(d, "でも、自分の", Fnt(FB, 116), ML, 260, INK)
L(d, "仕事では？", Fnt(FB, 116), ML, 400, INK)
plant(d, 850, 940, 1, s=2.6)  # 発芽
counter(img, 1)
save(img, 2)

# ===== P3: 発信すること（価値） / 双葉・案内役登場 =====
img = bg((235, 242, 226), (220, 234, 213))
glow(img, 780, 800, 290, color=(255, 238, 170), max_a=78)
coach(img, "smile", 470, (610, 590))  # 右に大きく
d = ImageDraw.Draw(img)
L(d, "毎週、仕事に効く", Fnt(FB, 92), ML, 150, INK)
L(d, "AIを、やさしく。", Fnt(FB, 92), ML, 270, INK)
L(d, "・職種別の使い方（営業／人事／DX推進…）", Fnt(FM, 33), ML, 410, INK2)
L(d, "・今週のAIを“あなたの業務”に翻訳", Fnt(FM, 33), ML, 458, INK2)
L(d, "・初めての「これ何？」に1問1答", Fnt(FM, 33), ML, 506, INK2)
plant(d, 250, 980, 2, s=2.4)  # 双葉
counter(img, 2)
save(img, 3)

# ===== P4: 案内役＋CTA（伴走） / 花・最も明るい =====
img = bg((240, 244, 229), (230, 241, 218))
glow(img, 880, 800, 280, color=(255, 238, 165), max_a=70)
coach(img, "happy", 380, (-20, 600))  # 左・笑顔
d = ImageDraw.Draw(img)
L(d, "最初の一歩に、", Fnt(FB, 100), ML, 150, INK)
L(d, "伴走します。", Fnt(FB, 116), ML, 285, GREEN_D)  # 希望＝グリーン
L(d, "AIコーチ“これから”｜やさしいAI活用研究室", Fnt(FM, 28), ML, 430, INK2)
L(d, "フォローで、はじめよう。", Fnt(FB, 44), ML, 472, INK)
L(d, "@ai_coach_korekara", Fnt(FB, 40), ML, 528, GREEN_D)
plant(d, 920, 1000, 4, s=1.4)  # 花
counter(img, 3)
save(img, 4)

print("done: 4 slides (v5) ->", OUT)
