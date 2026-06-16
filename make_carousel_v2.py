"""IG初回カルーセル v2 — 読者を主人公にした物語型リデザイン（5枚）。
主人公=AIに不安を感じる読者 / AIコーチ=案内役。芽=読者の成長のメタファー。
ページごとにズーム・余白・構図・文字量・表情を変える。芽はスワイプで成長。
ページ番号=育つ芽の列＋現在地が光る。
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1080
NAVY = (28, 52, 88); NAVY2 = (60, 86, 124); GREEN = (104, 150, 100)
GREEN2 = (150, 186, 142); GRAY = (110, 124, 112); SOIL = (130, 104, 78)
GOLD = (250, 224, 140); PETAL = (245, 205, 160); WHITE = (255, 255, 255)
FB = "C:/Windows/Fonts/YuGothB.ttc"; FM = "C:/Windows/Fonts/YuGothM.ttc"
ICON = "C:/Users/takanori.koyama/Desktop/Claude/sns-assets/icon"
OUT = "C:/Users/takanori.koyama/Desktop/Claude/sns-assets/images"

FACES = {k: Image.open(f"{ICON}/coach-{k}.png").convert("RGBA")
         for k in ("thinking", "happy", "smile", "sheepish")}


def F(p, s):
    return ImageFont.truetype(p, s)


def vgrad(top, bot):
    img = Image.new("RGB", (W, H), top)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(top[i] * (1 - t) + bot[i] * t) for i in range(3)))
    return img.convert("RGBA")


def add_glow(img, cx, cy, R, color=GOLD, max_a=110, steps=32):
    for i in range(steps):
        r = R * (1 - i / steps)
        a = int(max_a * (i / steps) ** 1.4)
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(layer).ellipse((cx - r, cy - r, cx + r, cy + r), fill=color + (a,))
        img.alpha_composite(layer)


def circle(face, size):
    im = FACES[face].resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)
    return out


def coach(img, face, size, xy, flip=False, ring=GREEN):
    av = circle(face, size)
    if flip:
        av = av.transpose(Image.FLIP_LEFT_RIGHT)
    img.alpha_composite(av, xy)
    d = ImageDraw.Draw(img)
    d.ellipse((xy[0], xy[1], xy[0] + size, xy[1] + size), outline=WHITE, width=8)
    d.ellipse((xy[0] + 4, xy[1] + 4, xy[0] + size - 4, xy[1] + size - 4), outline=ring, width=3)


def leaf(d, x, y, size, side, color):
    if side < 0:
        d.ellipse((x - size, y - size * 0.55, x + size * 0.1, y + size * 0.55), fill=color)
    else:
        d.ellipse((x - size * 0.1, y - size * 0.55, x + size, y + size * 0.55), fill=color)


def plant(d, x, by, stage, s=1.0):
    """stage 0:種 1:芽吹き 2:双葉 3:育つ 4:開花"""
    if stage == 0:
        d.ellipse((x - 16 * s, by - 30 * s, x + 16 * s, by), fill=SOIL)
        d.arc((x - 16 * s, by - 30 * s, x + 16 * s, by), 200, 340, fill=(95, 75, 58), width=int(3 * s))
        return
    if stage == 1:
        d.line([(x, by), (x, by - 46 * s)], fill=GREEN, width=int(9 * s))
        leaf(d, x + 6 * s, by - 52 * s, 26 * s, 1, GREEN2)
        return
    if stage == 2:
        d.line([(x, by), (x, by - 72 * s)], fill=GREEN, width=int(10 * s))
        leaf(d, x, by - 80 * s, 46 * s, -1, GREEN)
        leaf(d, x, by - 80 * s, 46 * s, 1, GREEN2)
        return
    if stage == 3:
        d.line([(x, by), (x, by - 150 * s)], fill=GREEN, width=int(11 * s))
        leaf(d, x, by - 60 * s, 40 * s, -1, GREEN)
        leaf(d, x, by - 95 * s, 44 * s, 1, GREEN2)
        leaf(d, x, by - 130 * s, 40 * s, -1, GREEN)
        leaf(d, x, by - 160 * s, 48 * s, 1, GREEN2)
        return
    # stage 4: 開花
    d.line([(x, by), (x, by - 175 * s)], fill=GREEN, width=int(12 * s))
    leaf(d, x, by - 70 * s, 46 * s, -1, GREEN)
    leaf(d, x, by - 115 * s, 48 * s, 1, GREEN2)
    cx, cy = x, by - 205 * s
    for ang in range(0, 360, 72):
        dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        d.ellipse((cx + dx * 30 * s - 26 * s, cy + dy * 30 * s - 26 * s,
                   cx + dx * 30 * s + 26 * s, cy + dy * 30 * s + 26 * s), fill=PETAL)
    d.ellipse((cx - 22 * s, cy - 22 * s, cx + 22 * s, cy + 22 * s), fill=GOLD)


def grow_indicator(img, idx, n=5):
    d = ImageDraw.Draw(img)
    gap = 92; x0 = W // 2 - gap * (n - 1) // 2; y = 1018
    d.line([(x0 - 20, y), (x0 + gap * (n - 1) + 20, y)], fill=(200, 210, 198), width=3)
    for i in range(n):
        x = x0 + i * gap
        if i == idx:
            add_glow(img, x, y - 14, 46, color=(180, 220, 150), max_a=120)
            d = ImageDraw.Draw(img)
        plant(d, x, y, min(i, 4), s=0.16 + i * 0.015)


def c线():  # placeholder to avoid accidental name use
    pass


def ctext(d, text, font, y, fill, cx=W // 2):
    w = d.textlength(text, font=font)
    d.text((cx - w / 2, y), text, font=font, fill=fill)


def ltext(d, text, font, x, y, fill):
    d.text((x, y), text, font=font, fill=fill)


def tool(d, kind, cx, cy, s, color=NAVY):
    if kind == "case":
        d.rounded_rectangle((cx - 34 * s, cy - 20 * s, cx + 34 * s, cy + 26 * s), radius=8, outline=color, width=int(5 * s))
        d.rounded_rectangle((cx - 14 * s, cy - 32 * s, cx + 14 * s, cy - 18 * s), radius=5, outline=color, width=int(5 * s))
    elif kind == "chart":
        for k, hh in enumerate((18, 34, 26)):
            bx = cx - 30 * s + k * 26 * s
            d.rectangle((bx, cy + 26 * s - hh * s, bx + 16 * s, cy + 26 * s), fill=color)
    elif kind == "chat":
        d.rounded_rectangle((cx - 34 * s, cy - 26 * s, cx + 34 * s, cy + 16 * s), radius=12, outline=color, width=int(5 * s))
        d.polygon([(cx - 14 * s, cy + 14 * s), (cx - 30 * s, cy + 34 * s), (cx - 2 * s, cy + 16 * s)], fill=color)
    elif kind == "doc":
        d.rounded_rectangle((cx - 24 * s, cy - 32 * s, cx + 24 * s, cy + 30 * s), radius=8, outline=color, width=int(5 * s))
        for k in range(3):
            d.line([(cx - 12 * s, cy - 14 * s + k * 16 * s), (cx + 12 * s, cy - 14 * s + k * 16 * s)], fill=color, width=int(3 * s))


def save(img, n):
    img.convert("RGB").save(f"{OUT}/ig-carousel-{n}.jpg", "JPEG", quality=90)


# ===== Page 1: 不安の代弁（大胆タイポ・暗め・余白） =====
img = vgrad((212, 222, 210), (180, 193, 182))
d = ImageDraw.Draw(img)
ltext(d, "なんとなく、", F(FM, 44), 140, 150, GRAY)
ltext(d, "置いて", F(FB, 150), 120, 250, NAVY)
ltext(d, "いかれそう。", F(FB, 150), 120, 420, NAVY)
plant(d, 880, 760, 0, s=1.6)  # 種（右下・小さく孤独に）
add_glow(img, 880, 720, 70, color=(120, 140, 120), max_a=40)
d = ImageDraw.Draw(img)
ltext(d, "——そう感じているの、あなただけじゃありません。", F(FM, 34), 120, 880, GRAY)
grow_indicator(img, 0)
save(img, 1)

# ===== Page 2: 共感（情報の洪水・文字を散らす） =====
img = vgrad((224, 231, 219), (203, 213, 201))
d = ImageDraw.Draw(img)
jargon = [("ChatGPT", 120, 120, 40), ("生成AI", 760, 160, 46), ("エージェント", 540, 300, 38),
          ("LLM", 180, 340, 34), ("RAG", 860, 360, 34), ("自動化", 120, 470, 36),
          ("マルチモーダル", 600, 470, 30), ("プロンプト", 800, 560, 32)]
for t, x, y, sz in jargon:
    ltext(d, t, F(FM, sz), x, y, (170, 182, 170))
ltext(d, "ニュースは毎日。AIはどんどん進む。でも——", F(FM, 36), 120, 650, GRAY)
ltext(d, "「私の仕事」では、", F(FB, 88), 120, 720, NAVY)
ltext(d, "どう使えばいい？", F(FB, 88), 120, 830, NAVY)
plant(d, 980, 980, 1, s=1.1)  # 芽吹き
grow_indicator(img, 1)
save(img, 2)

# ===== Page 3: 転機「大丈夫」（案内役登場・AIの光・双葉） =====
img = vgrad((232, 240, 227), (212, 232, 208))
add_glow(img, 760, 360, 320, color=(255, 238, 175), max_a=95)  # AIの光
coach(img, "smile", 360, (560, 180))
d = ImageDraw.Draw(img)
ltext(d, "大丈夫。", F(FB, 150), 90, 280, NAVY)
ltext(d, "むずかしいことは、ぜんぶ", F(FM, 42), 95, 500, NAVY2)
ltext(d, "“あなたの言葉”に翻訳します。", F(FB, 52), 95, 565, NAVY)
plant(d, 180, 880, 2, s=1.5)  # 双葉
grow_indicator(img, 2)
save(img, 3)

# ===== Page 4: 自分ごと化（仕事道具が光る・育つ） =====
img = vgrad((235, 242, 228), (222, 238, 213))
d = ImageDraw.Draw(img)
ltext(d, "ある日、ふと気づく。", F(FM, 38), 110, 130, GRAY)
ltext(d, "「これ、私の", F(FB, 92), 100, 200, NAVY)
ltext(d, "仕事に使えるかも」", F(FB, 92), 100, 305, NAVY)
# 仕事道具が光る
tools = [("case", 230, "営業"), ("doc", 430, "資料"), ("chart", 630, "分析"), ("chat", 830, "対応")]
for kind, x, label in tools:
    add_glow(img, x, 560, 90, color=(255, 236, 170), max_a=80)
for kind, x, label in tools:
    dd = ImageDraw.Draw(img)
    tool(dd, kind, x, 560, 1.2, NAVY)
    ctext(dd, label, F(FM, 30), 620, NAVY2, cx=x)
d = ImageDraw.Draw(img)
ltext(d, "そう思えた瞬間から、AIは“味方”になる。", F(FM, 38), 110, 720, NAVY2)
coach(img, "thinking", 190, (150, 800), flip=True)
plant(d, 950, 1000, 3, s=1.0)  # 育つ
grow_indicator(img, 3)
save(img, 4)

# ===== Page 5: CTA（大胆タイポ・開花・最も明るい） =====
img = vgrad((240, 244, 228), (228, 240, 214))
add_glow(img, 520, 470, 340, color=(255, 240, 180), max_a=75)
d = ImageDraw.Draw(img)
ltext(d, "あなたの", F(FB, 112), 110, 150, NAVY)
ltext(d, "「これから」を、", F(FB, 112), 110, 280, NAVY)
ltext(d, "育てよう。", F(FB, 124), 110, 410, GREEN)
plant(d, 950, 840, 4, s=1.2)  # 開花（右・テキストと干渉回避）
coach(img, "happy", 220, (110, 600))
d = ImageDraw.Draw(img)
ltext(d, "毎週、仕事に効くAIをお届け。", F(FM, 32), 380, 645, NAVY2)
ltext(d, "フォローで、最初の一歩を。", F(FB, 44), 380, 705, NAVY)
ltext(d, "@ai_coach_korekara", F(FB, 46), 380, 780, GREEN)
grow_indicator(img, 4)
save(img, 5)

print("done: 5 slides (v2) ->", OUT)
