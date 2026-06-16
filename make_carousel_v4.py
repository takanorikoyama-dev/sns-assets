"""IG初回カルーセル v4 — 前向き・やさしい全面改稿（6枚）。
方針: 不安で始めない／日常の小さな瞬間→希望。1ページ1メッセージ。
レイアウト鉄則: テキスト帯(上 y<=530)とビジュアル帯(下 y>=560)を完全分離→文字と人物/植物を絶対に重ねない。
キャラはページ毎にサイズ・表情・左右を変える(丸囲み廃止のソフトカット)。
芽の成長を投稿全体で連動(種→発芽→双葉→成長→つぼみ→花)。背景は1→6で少しずつ明るく。
"""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = H = 1080
TEXT_MAX_Y = 530    # これ以下にテキスト
VIS_MIN_Y = 560     # これ以上にビジュアル
ML = 96             # 左安全余白
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
    grain = Image.merge("RGBA", (_GRAIN, _GRAIN, _GRAIN, Image.new("L", (W, H), 8)))
    img.alpha_composite(grain)
    return img


def glow(img, cx, cy, R, color=GOLD, max_a=80, steps=30):
    for i in range(steps):
        r = R * (1 - i / steps)
        a = int(max_a * (i / steps) ** 1.5)
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(layer).ellipse((cx - r, cy - r, cx + r, cy + r), fill=color + (a,))
        img.alpha_composite(layer)


def coach(img, face, size, xy, flip=False, feather=34):
    """ソフトカット(丸囲み廃止)。ビジュアル帯(y>=560)にのみ配置する。"""
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
    """0種 1発芽 2双葉 3成長 4花 5つぼみ。主役級に大きく。"""
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
    if stage == 3:
        d.line([(x, by), (x, by - 200 * s)], fill=GREEN, width=int(14 * s))
        leaf(d, x, by - 74 * s, 58 * s, -1, GREEN)
        leaf(d, x, by - 124 * s, 62 * s, 1, GREEN2)
        leaf(d, x, by - 174 * s, 56 * s, -1, GREEN)
        leaf(d, x, by - 212 * s, 66 * s, 1, GREEN2)
        return
    if stage == 5:  # つぼみ
        d.line([(x, by), (x, by - 205 * s)], fill=GREEN, width=int(14 * s))
        leaf(d, x, by - 90 * s, 58 * s, -1, GREEN)
        leaf(d, x, by - 140 * s, 60 * s, 1, GREEN2)
        cx, cy = x, by - 240 * s
        d.ellipse((cx - 30 * s, cy - 40 * s, cx + 30 * s, cy + 30 * s), fill=GREEN2)
        d.ellipse((cx - 18 * s, cy - 54 * s, cx + 18 * s, cy - 16 * s), fill=GOLD)
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


def step_mark(img, idx, n=6):
    """進行カウンタ（右上・最小限）。成長ストーリーは各ページの大きな植物が担う。"""
    d = ImageDraw.Draw(img)
    d.text((W - 150, 66), f"{idx + 1} / {n}", font=Fnt(FM, 30), fill=INK2)


def L(d, t, f, x, y, fill):
    d.text((x, y), t, font=f, fill=fill)


def save(img, n):
    img.convert("RGB").save(f"{OUT}/ig-carousel-{n}.jpg", "JPEG", quality=92)


# ===== P1: 自分ごと（日常の小さな瞬間）／種 =====
img = bg((224, 235, 218), (205, 222, 202))
d = ImageDraw.Draw(img)
L(d, "いつもの仕事の途中、ふと思う。", Fnt(FM, 38), ML, 170, GRAYT)
L(d, "「もっとラクに、", Fnt(FB, 110), ML, 260, INK)
L(d, "できないかな」", Fnt(FB, 110), ML, 400, INK)
plant(d, 540, 900, 0, s=3.0)  # 種（ビジュアル帯・中央）
step_mark(img, 0)
save(img, 1)

# ===== P2: 共感（分かる）／発芽 =====
img = bg((228, 238, 221), (210, 226, 206))
d = ImageDraw.Draw(img)
L(d, "記事は見る。すごいのも分かる。", Fnt(FM, 38), ML, 170, GRAYT)
L(d, "でも、自分の", Fnt(FB, 116), ML, 270, INK)
L(d, "仕事では？", Fnt(FB, 116), ML, 410, INK)
plant(d, 850, 940, 1, s=2.6)  # 発芽（右）
step_mark(img, 1)
save(img, 2)

# ===== P3: 安心（案内役が大きく登場）／双葉 =====
img = bg((232, 240, 224), (215, 231, 209))
glow(img, 770, 800, 300, color=(255, 238, 170), max_a=80)  # 光はビジュアル帯のみ
coach(img, "smile", 480, (600, 580))  # 右に大きく（ソフトカット）
d = ImageDraw.Draw(img)
L(d, "大丈夫。", Fnt(FB, 170), ML, 200, INK)
L(d, "むずかしく、ありません。", Fnt(FM, 56), ML, 430, INK2)
plant(d, 240, 980, 2, s=2.6)  # 双葉（左）
step_mark(img, 2)
save(img, 3)

# ===== P4: 気づき（具体例）／成長 =====
img = bg((235, 242, 226), (220, 234, 213))
coach(img, "thinking", 360, (-40, 620), flip=True)  # 左・別表情/サイズ
d = ImageDraw.Draw(img)
L(d, "たとえば、毎日のメール。", Fnt(FM, 38), ML, 160, GRAYT)
L(d, "「下書き、お願い」", Fnt(FB, 100), ML, 250, INK)
L(d, "から始めてみる。", Fnt(FB, 100), ML, 385, INK)
plant(d, 930, 980, 3, s=1.6)  # 成長（右）
step_mark(img, 3)
save(img, 4)

# ===== P5: 試したくなる／つぼみ =====
img = bg((238, 243, 228), (226, 238, 216))
coach(img, "happy", 300, (770, 720))  # 右・小さめ
d = ImageDraw.Draw(img)
L(d, "明日、ひとつ", Fnt(FB, 116), ML, 200, INK)
L(d, "だけ試す。", Fnt(FB, 116), ML, 340, GREEN_D)  # 希望＝グリーン
L(d, "大きな変化じゃなくていい。小さな一歩から。", Fnt(FM, 33), ML, 460, GRAYT)
plant(d, 430, 1015, 5, s=1.15)  # つぼみ（中央左・文字帯の下）
step_mark(img, 4)
save(img, 5)

# ===== P6: フォロー（CTA）／花・最も明るい =====
img = bg((241, 245, 230), (231, 241, 219))
glow(img, 880, 800, 280, color=(255, 238, 165), max_a=70)
coach(img, "happy", 380, (-20, 600))  # 左・笑顔
d = ImageDraw.Draw(img)
L(d, "いっしょに、", Fnt(FB, 100), ML, 150, INK)
L(d, "ちいさく育てよう。", Fnt(FB, 100), ML, 285, GREEN_D)
L(d, "毎週ひとつ、あなたの仕事に効くAIを。", Fnt(FM, 32), ML, 410, INK2)
L(d, "フォローで、最初の一歩を。", Fnt(FB, 42), ML, 458, INK)
L(d, "@ai_coach_korekara", Fnt(FB, 40), ML, 512, GREEN_D)
plant(d, 920, 1000, 4, s=1.4)  # 花（右・ビジュアル帯）
step_mark(img, 5)
save(img, 6)

print("done: 6 slides (v4) ->", OUT)
