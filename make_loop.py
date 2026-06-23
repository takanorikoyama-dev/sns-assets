# -*- coding: utf-8 -*-
"""コンテンツ運用ループ図（仮説→投稿→検証→学び→次へ／学びストック中核）。"""
from PIL import Image, ImageDraw, ImageFont
import math
OUT = "C:/Users/takanori.koyama/Desktop/Claude/sns-assets/loop_design.png"
W, H = 1740, 1360
img = Image.new("RGB", (W, H), "#FFFFFF")
d = ImageDraw.Draw(img)


def F(sz, bold=True):
    return ImageFont.truetype("C:/Windows/Fonts/" + ("YuGothB.ttc" if bold else "YuGothM.ttc"), sz)


NAVY = "#16263A"; CY = "#0090C8"; GRY = "#5B6B7B"; GOLD = "#D98200"


def wrap(text, font, maxw):
    out = []
    line = ""
    for ch in text:
        if d.textlength(line + ch, font=font) <= maxw:
            line += ch
        else:
            out.append(line); line = ch
    out.append(line)
    return out


def ctext(cx, cy, txt, font, fill, maxw, gap=4):
    lines = wrap(txt, font, maxw); ch = font.size + gap; ty = cy - len(lines) * ch // 2
    for ln in lines:
        w = d.textlength(ln, font=font); d.text((cx - w / 2, ty), ln, font=font, fill=fill); ty += ch


def node(cx, cy, w, h, title, sub, col):
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=16, fill="#FFFFFF", outline=col, width=4)
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy - h / 2 + 40], radius=16, fill=col)
    d.rectangle([cx - w / 2, cy - h / 2 + 24, cx + w / 2, cy - h / 2 + 40], fill=col)
    tw = d.textlength(title, font=F(22)); d.text((cx - tw / 2, cy - h / 2 + 8), title, font=F(22), fill="#FFFFFF")
    ctext(cx, cy + 14, sub, F(16, False), NAVY, w - 28)


d.text((50, 34), "コンテンツ運用ループ（仮説 → 投稿 → 検証 → 学び → 次の企画）", font=F(42), fill=NAVY)
d.text((52, 92), "自社アカウント／運用代行の共通設計。(AI)=AI主体　(人)=弊社スタッフ主体。学びを貯めて毎回かしこくする。", font=F(20, False), fill=GRY)

CX, CY, R = 820, 760, 400
nodes = [
    ("① 企画 Plan", "仮説を立てる(人)。テーマ×差別化フォーマット・フック・KPI目標", NAVY),
    ("② 制作 Make", "AIが下書き ＋ 人が仕上げ", CY),
    ("③ 投稿 Publish", "承認→予約投稿(人)。投稿条件を記録(日時/型/フック)", CY),
    ("④ 計測 Measure", "48h・7dで指標取得(AI)。リーチ/保存/維持/フォロー転換", CY),
    ("⑤ 振り返り Review", "勝敗要因をAIが要約→人が解釈・学びを言語化", GOLD),
    ("⑥ 学びの反映", "続ける/変える/やめるを決定(人)→次の①へ", GOLD),
]
ang = [-90, -30, 30, 90, 150, 210]
pts = [(CX + R * math.cos(math.radians(a)), CY + R * math.sin(math.radians(a))) for a in ang]


def arrow(p0, p1, col, trim=150):
    x0, y0 = p0; x1, y1 = p1; dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    sx, sy = x0 + ux * trim, y0 + uy * trim; ex, ey = x1 - ux * trim, y1 - uy * trim
    d.line([sx, sy, ex, ey], fill=col, width=7)
    a = math.atan2(ey - sy, ex - sx)
    for s in (0.42, -0.42):
        d.line([ex, ey, ex - 26 * math.cos(a - s), ey - 26 * math.sin(a - s)], fill=col, width=7)


for i in range(6):
    arrow(pts[i], pts[(i + 1) % 6], GOLD if i == 5 else "#9AA7B3")

mx, my = (pts[5][0] + pts[0][0]) / 2, (pts[5][1] + pts[0][1]) / 2
d.text((mx - 150, my - 70), "学びを次の企画へ", font=F(20), fill=GOLD)

hub = 190
d.ellipse([CX - hub, CY - hub, CX + hub, CY + hub], fill="#FFF7E9", outline=GOLD, width=4)
ctext(CX, CY - 34, "学びストック", F(28), GOLD, hub * 2 - 40)
ctext(CX, CY + 4, "Learnings DB", F(18, False), GOLD, hub * 2 - 40)
ctext(CX, CY + 50, "仮説・結果・学びを蓄積。AIが横断要約し勝ちパターンを抽出", F(15, False), NAVY, hub * 2 - 46)

for (t, s, c), (px, py) in zip(nodes, pts):
    node(px, py, 300, 122, t, s, c)


def dline(p0, p1, col):
    x0, y0 = p0; x1, y1 = p1; n = 24
    for k in range(n):
        if k % 2:
            continue
        d.line([x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n,
                x0 + (x1 - x0) * (k + 1) / n, y0 + (y1 - y0) * (k + 1) / n], fill=col, width=3)


for idx in (3, 4):
    dline(pts[idx], (CX, CY), "#E0B775")
dline((CX, CY), pts[0], "#E0B775")

lx, ly, lw, lh = 1330, 180, 370, 256
d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=14, fill="#F4F7FA", outline=GRY, width=2)
d.text((lx + 18, ly + 14), "3つの回転速度（入れ子ループ）", font=F(20), fill=NAVY)
rows = [("速い (投稿ごと/48h)", "フック・サムネ・投稿時間を微調整"),
        ("中 (週次)", "勝ちフォーマット特定→翌週企画へ"),
        ("遅い (月次)", "KGI進捗→戦略・配分／月次レポート")]
yy = ly + 56
for h, s in rows:
    d.text((lx + 18, yy), "・" + h, font=F(18), fill=CY); yy += 26
    ctext(lx + lw / 2 + 10, yy + 10, s, F(15, False), NAVY, lw - 60); yy += 48

img.save(OUT)
print("SAVED", OUT, img.size)
