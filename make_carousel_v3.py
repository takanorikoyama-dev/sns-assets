"""IG初回カルーセル v3 — アートディレクション全面リデザイン（5枚）。
方針: 高コントラスト / 1ページ1メッセージ / 大胆な余白 / 大きなキャラ(丸囲み廃止・ソフトカット) /
芽の成長を主役級に(種→発芽→双葉→成長→花) / やわらかい光＋紙質感 / タイポの強弱。
ブランド色(ミント/ネイビー/グリーン)維持＋光のイエローを限定使用。
"""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = H = 1080
INK = (20, 40, 70)        # 濃いネイビー（高コントラスト見出し）
INK2 = (54, 78, 112)
GREEN = (95, 146, 92); GREEN_D = (74, 122, 72); GREEN2 = (150, 188, 140)
GRAYT = (96, 110, 100)    # 本文グレー（薄すぎない）
SOIL = (132, 104, 76); GOLD = (246, 206, 90); PETAL = (250, 214, 150)
WHITE = (255, 255, 255)
FB = "C:/Windows/Fonts/YuGothB.ttc"; FM = "C:/Windows/Fonts/YuGothM.ttc"
ICON = "C:/Users/takanori.koyama/Desktop/Claude/sns-assets/icon"
OUT = "C:/Users/takanori.koyama/Desktop/Claude/sns-assets/images"
FACES = {k: Image.open(f"{ICON}/coach-{k}.png").convert("RGBA")
         for k in ("thinking", "happy", "smile", "sheepish")}

_GRAIN = Image.effect_noise((W, H), 20).convert("L")


def Fnt(p, s):
    return ImageFont.truetype(p, s)


def bg(top, bot, glow=None):
    img = Image.new("RGB", (W, H), top)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = (y / H) ** 1.1
        d.line([(0, y), (W, y)], fill=tuple(int(top[i] * (1 - t) + bot[i] * t) for i in range(3)))
    img = img.convert("RGBA")
    if glow:
        cx, cy, R, col, a = glow
        add_glow(img, cx, cy, R, col, a)
    grain = Image.merge("RGBA", (_GRAIN, _GRAIN, _GRAIN, Image.new("L", (W, H), 10)))
    img.alpha_composite(grain)
    return img


def add_glow(img, cx, cy, R, color=GOLD, max_a=90, steps=34):
    for i in range(steps):
        r = R * (1 - i / steps)
        a = int(max_a * (i / steps) ** 1.5)
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(layer).ellipse((cx - r, cy - r, cx + r, cy + r), fill=color + (a,))
        img.alpha_composite(layer)


def coach(img, face, size, xy, flip=False, feather=34):
    """丸囲みをやめ、ふちをぼかしたソフトカットで大きく配置（画面端から見切れOK）。"""
    im = FACES[face].resize((size, size), Image.LANCZOS)
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((feather, feather, size - feather, size - feather), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(feather * 0.7))
    img.paste(im, xy, mask)  # paste は負座標OK（見切れ表現）


def leaf(d, x, y, size, side, color):
    if side < 0:
        d.ellipse((x - size, y - size * 0.55, x + size * 0.12, y + size * 0.55), fill=color)
    else:
        d.ellipse((x - size * 0.12, y - size * 0.55, x + size, y + size * 0.55), fill=color)


def plant(d, x, by, stage, s=1.0):
    """種→発芽→双葉→成長→花。主役級に大きく描く。"""
    if stage == 0:  # 種
        d.ellipse((x - 22 * s, by - 40 * s, x + 22 * s, by), fill=SOIL)
        d.arc((x - 22 * s, by - 40 * s, x + 22 * s, by), 200, 340, fill=(96, 74, 56), width=int(4 * s))
        return
    if stage == 1:  # 発芽
        d.line([(x, by), (x, by - 64 * s)], fill=GREEN, width=int(12 * s))
        leaf(d, x + 8 * s, by - 74 * s, 38 * s, 1, GREEN2)
        return
    if stage == 2:  # 双葉
        d.line([(x, by), (x, by - 96 * s)], fill=GREEN, width=int(13 * s))
        leaf(d, x, by - 108 * s, 62 * s, -1, GREEN)
        leaf(d, x, by - 108 * s, 62 * s, 1, GREEN2)
        return
    if stage == 3:  # 成長
        d.line([(x, by), (x, by - 200 * s)], fill=GREEN, width=int(14 * s))
        leaf(d, x, by - 70 * s, 56 * s, -1, GREEN)
        leaf(d, x, by - 120 * s, 60 * s, 1, GREEN2)
        leaf(d, x, by - 170 * s, 54 * s, -1, GREEN)
        leaf(d, x, by - 210 * s, 64 * s, 1, GREEN2)
        return
    # stage 4: 花
    d.line([(x, by), (x, by - 215 * s)], fill=GREEN, width=int(15 * s))
    leaf(d, x, by - 85 * s, 60 * s, -1, GREEN)
    leaf(d, x, by - 140 * s, 64 * s, 1, GREEN2)
    cx, cy = x, by - 250 * s
    for ang in range(0, 360, 72):
        dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        d.ellipse((cx + dx * 38 * s - 34 * s, cy + dy * 38 * s - 34 * s,
                   cx + dx * 38 * s + 34 * s, cy + dy * 38 * s + 34 * s), fill=PETAL)
    d.ellipse((cx - 28 * s, cy - 28 * s, cx + 28 * s, cy + 28 * s), fill=GOLD)


def grow_bar(img, idx, n=5):
    """進行表示＝芽の成長ストーリー。現在地が光る。"""
    d = ImageDraw.Draw(img)
    gap = 104; x0 = W // 2 - gap * (n - 1) // 2; y = 1016
    d.line([(x0 - 16, y), (x0 + gap * (n - 1) + 16, y)], fill=(196, 208, 192), width=3)
    for i in range(n):
        x = x0 + i * gap
        if i == idx:
            add_glow(img, x, y - 18, 52, color=(196, 226, 150), max_a=130)
            d = ImageDraw.Draw(img)
        plant(d, x, y, min(i, 4), s=0.2 + i * 0.022)


def L(d, text, font, x, y, fill):
    d.text((x, y), text, font=font, fill=fill)


def save(img, n):
    img.convert("RGB").save(f"{OUT}/ig-carousel-{n}.jpg", "JPEG", quality=92)


# ===== P1: HOOK（種）— 不安。大胆な余白＋濃いネイビー =====
img = bg((233, 242, 228), (210, 226, 206))
d = ImageDraw.Draw(img)
L(d, "置いて", Fnt(FB, 168), 110, 230, INK)
L(d, "いかれそう。", Fnt(FB, 168), 110, 420, INK)
L(d, "なんとなく、そう感じていませんか？", Fnt(FM, 38), 114, 650, GRAYT)
plant(d, 250, 880, 0, s=2.4)  # 種（大きめ・これから育つ余白）
add_glow(img, 250, 835, 80, color=(150, 170, 140), max_a=45)
grow_bar(img, 0)
save(img, 1)

# ===== P2: EMPATHY（発芽）— 問い1つ。余白大 =====
img = bg((230, 240, 224), (208, 224, 203))
d = ImageDraw.Draw(img)
for t, x, y, sz in [("生成AI", 720, 150, 44), ("エージェント", 150, 200, 34), ("自動化", 820, 300, 32)]:
    L(d, t, Fnt(FM, sz), x, y, (182, 194, 180))
L(d, "“私の仕事”では、", Fnt(FB, 104), 110, 430, INK)
L(d, "どう使う？", Fnt(FB, 132), 110, 575, INK)
L(d, "ニュースは追える。でも、答えは出ない。", Fnt(FM, 36), 114, 770, GRAYT)
plant(d, 930, 900, 1, s=2.1)  # 発芽
grow_bar(img, 1)
save(img, 2)

# ===== P3: TURN（双葉）— 「大丈夫。」案内役が大きく登場＋光 =====
img = bg((232, 241, 226), (214, 232, 208), glow=(800, 430, 360, (255, 236, 168), 105))
coach(img, "smile", 620, (560, 70), feather=40)  # 大きく・右から見切れ
d = ImageDraw.Draw(img)
L(d, "大丈夫。", Fnt(FB, 180), 90, 300, INK)
L(d, "むずかしいことは、", Fnt(FM, 40), 96, 560, INK2)
L(d, "“あなたの言葉”に翻訳します。", Fnt(FB, 54), 96, 622, INK)
plant(d, 200, 940, 2, s=2.0)  # 双葉
grow_bar(img, 2)
save(img, 3)

# ===== P4: SELF（成長）— 「私にもできるかも」希望はグリーン =====
img = bg((233, 242, 226), (216, 234, 210), glow=(360, 430, 300, (210, 232, 150), 70))
coach(img, "thinking", 440, (-90, 560), flip=True, feather=38)  # 左から見切れ・別表情
d = ImageDraw.Draw(img)
L(d, "あ、これ私にも", Fnt(FB, 104), 110, 195, INK)
L(d, "できるかも。", Fnt(FB, 132), 110, 335, GREEN_D)  # 希望の語＝グリーン
L(d, "あなたの言葉なら、AIは身近に。", Fnt(FM, 36), 110, 510, GRAYT)
plant(d, 920, 1010, 3, s=1.4)  # 成長
grow_bar(img, 3)
save(img, 4)

# ===== P5: CTA（花）— 最も明るい。開花が主役 =====
img = bg((238, 244, 226), (224, 238, 210), glow=(540, 470, 380, (255, 238, 170), 90))
coach(img, "happy", 360, (-40, 560), feather=36)  # 左から見切れ・笑顔
d = ImageDraw.Draw(img)
L(d, "あなたの", Fnt(FB, 110), 110, 140, INK)
L(d, "“これから”を、", Fnt(FB, 110), 110, 275, INK)
L(d, "育てよう。", Fnt(FB, 140), 110, 410, GREEN_D)  # 希望＝グリーン
plant(d, 900, 880, 4, s=1.7)  # 花（開花が主役）
L(d, "毎週、仕事に効くAIをやさしく。", Fnt(FM, 34), 400, 660, INK2)
L(d, "フォローで、最初の一歩を。", Fnt(FB, 48), 400, 720, INK)
L(d, "@ai_coach_korekara", Fnt(FB, 46), 400, 800, GREEN_D)
grow_bar(img, 4)
save(img, 5)

print("done: 5 slides (v3) ->", OUT)
