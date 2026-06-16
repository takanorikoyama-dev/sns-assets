"""IG初回投稿カルーセル（4枚）を生成する。
ブランド配色（ミント×ネイビー×グリーン）＋キャラ合成。
イースターエッグ: 🌱が回を追うごとに育つ（本投稿内では 1→2→3）/ 最終スライドに隠れコーチの本音。
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080
BG = (236, 242, 230); NAVY = (31, 58, 95); GREEN = (104, 150, 100)
GREEN2 = (146, 184, 140); GRAY = (96, 110, 98); WHITE = (255, 255, 255)
FB = "C:/Windows/Fonts/YuGothB.ttc"; FM = "C:/Windows/Fonts/YuGothM.ttc"
ICON = "C:/Users/takanori.koyama/Desktop/Claude/sns-assets/icon"
OUT = "C:/Users/takanori.koyama/Desktop/Claude/sns-assets/images"

# 表情レパートリーを用途別に使い分け
_faces = {
    "thinking": Image.open(f"{ICON}/coach-thinking.png").convert("RGBA"),  # 🤔 問い
    "happy": Image.open(f"{ICON}/coach-happy.png").convert("RGBA"),        # 😄 あいさつ
    "smile": Image.open(f"{ICON}/coach-smile.png").convert("RGBA"),        # 🙂 標準
    "sheepish": Image.open(f"{ICON}/coach-sheepish.png").convert("RGBA"),  # 😅 本音
}


def font(p, s):
    return ImageFont.truetype(p, s)


def circle_avatar(face, size):
    im = _faces[face].resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)
    return out


def paste_circle(img, face, size, xy, ring=True):
    av = circle_avatar(face, size)
    img.paste(av, xy, av)
    if ring:
        d = ImageDraw.Draw(img)
        d.ellipse((xy[0], xy[1], xy[0] + size, xy[1] + size), outline=WHITE, width=10)
        d.ellipse((xy[0]+5, xy[1]+5, xy[0] + size-5, xy[1] + size-5), outline=GREEN, width=4)


def sprout(d, cx, cy, scale=1.0):
    d.line([(cx, cy), (cx, cy - int(46 * scale))], fill=GREEN, width=max(4, int(9 * scale)))
    d.ellipse((cx - 48 * scale, cy - 78 * scale, cx - 2, cy - 24 * scale), fill=GREEN)
    d.ellipse((cx + 2, cy - 78 * scale, cx + 48 * scale, cy - 24 * scale), fill=GREEN2)


def cline(d, text, fnt, y, fill, cx=W // 2):
    w = d.textlength(text, font=fnt)
    d.text((cx - w / 2, y), text, font=fnt, fill=fill)


def wrap(d, text, fnt, maxw):
    lines, cur = [], ""
    for ch in text:
        t = cur + ch
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = ch
    if cur:
        lines.append(cur)
    return lines


def base():
    img = Image.new("RGB", (W, H), BG)
    return img, ImageDraw.Draw(img)


def dots(d, idx, n=4):
    gap = 34; x0 = W // 2 - gap * (n - 1) // 2
    for i in range(n):
        c = NAVY if i == idx else (200, 210, 198)
        d.ellipse((x0 + i * gap - 7, 1010, x0 + i * gap + 7, 1024), fill=c)


# ---- Slide 1: 表紙/フック ----
img, d = base()
cline(d, "AI、何から", font(FB, 116), 150, NAVY)
cline(d, "始める？", font(FB, 116), 290, NAVY)
sprout(d, 200, 470, 1.1)                       # 🌱 1つ目
paste_circle(img, "thinking", 300, (W // 2 - 150, 470))  # 🤔 問い
d = ImageDraw.Draw(img)
# キャラのセリフ風スワイプ誘導
d.rounded_rectangle((300, 800, 780, 880), radius=40, fill=WHITE, outline=NAVY, width=3)
cline(d, "→ スワイプで自己紹介します", font(FM, 34), 818, NAVY)
dots(d, 0)
img.save(f"{OUT}/ig-carousel-1.jpg", "JPEG", quality=90)

# ---- Slide 2: 自己紹介 ----
img, d = base()
paste_circle(img, "happy", 340, (W // 2 - 170, 120))     # 😄 あいさつ
d = ImageDraw.Draw(img)
cline(d, "はじめまして", font(FB, 92), 500, NAVY)
sprout(d, 150, 980, 0.7)                        # 🌱（装飾・左下、テキストと干渉しない位置）
cline(d, "AIコーチ “これから” です", font(FM, 50), 630, NAVY)
for i, ln in enumerate(wrap(d, "AI・AX・DXを“あなたの職種の言葉”に翻訳して、やさしく。", font(FM, 38), 920)):
    cline(d, ln, font(FM, 38), 740 + i * 56, GRAY)
dots(d, 1)
img.save(f"{OUT}/ig-carousel-2.jpg", "JPEG", quality=90)

# ---- Slide 3: これから発信すること ----
img, d = base()
cline(d, "これから発信すること", font(FB, 72), 130, NAVY)
d.line([(W // 2 - 200, 240), (W // 2 + 200, 240)], fill=GREEN, width=4)
items = [
    "職種別のAI活用（営業／人事／DX推進…）",
    "今週のAI、業務でどう効く？",
    "初学者の「これ何？」に1問1答",
]
y = 320
for it in items:
    sprout(d, 150, y + 40, 0.55)
    d.text((210, y), it, font=font(FM, 42), fill=NAVY)
    y += 130
paste_circle(img, "smile", 180, (W - 250, H - 250))      # 🙂 標準（小・右下）
d = ImageDraw.Draw(img)
dots(d, 2)
img.save(f"{OUT}/ig-carousel-3.jpg", "JPEG", quality=90)

# ---- Slide 4: CTA＋イースターエッグ（隠れコーチの本音 / 育った芽） ----
img, d = base()
paste_circle(img, "sheepish", 240, (110, 140))          # 😅 本音
d = ImageDraw.Draw(img)
# 吹き出し（本音）
d.rounded_rectangle((380, 150, 1010, 380), radius=36, fill=WHITE, outline=NAVY, width=3)
d.polygon([(380, 240), (340, 260), (380, 290)], fill=WHITE)
for i, ln in enumerate(wrap(d, "正直、私も毎日ついていくの必死です(笑) だから一緒に、ゆっくり進みましょう。", font(FM, 36), 590)):
    d.text((410, 185 + i * 50), ln, font=font(FM, 36), fill=NAVY)
cline(d, "フォローで“最初の道しるべ”に。", font(FB, 56), 520, NAVY)
cline(d, "@ai_coach_korekara", font(FB, 46), 610, GREEN)
# 🌱が3つに育つ（イースターエッグ）
sprout(d, W // 2 - 120, 820, 1.0)
sprout(d, W // 2, 840, 1.3)
sprout(d, W // 2 + 120, 820, 1.0)
cline(d, "最後まで見てくれて、ありがとう。", font(FM, 30), 900, GRAY)
dots(d, 3)
img.save(f"{OUT}/ig-carousel-4.jpg", "JPEG", quality=90)

print("done: 4 slides ->", OUT)
