# -*- coding: utf-8 -*-
"""主体別スイムレーンの業務フローマップ（A:UGC / B:Tips）。
レーン=主体(🤖AI/🏢弊社/📸IF/🤝クライアント)、列=ステップ。"""
from PIL import Image, ImageDraw, ImageFont
OUT="C:/Users/takanori.koyama/Desktop/Claude/sns-assets/flowmap_ops_ai_v2.png"
W,H=2300,1780
img=Image.new("RGB",(W,H),"#FFFFFF"); d=ImageDraw.Draw(img)
def F(sz,bold=True):
    return ImageFont.truetype("C:/Windows/Fonts/"+("YuGothB.ttc" if bold else "YuGothM.ttc"),sz)
NAVY="#16263A"; GRY="#5B6B7B"; LINE="#C7D0D9"
# 主体カラー (header, bg)
CO={"AI":("#0090C8","#E7F4FB"),"CO":("#16263A","#E7EBF1"),
    "IF":("#2E9E57","#E7F5EC"),"CL":("#D98200","#FFF1DC")}
def wrap(text,font,maxw):
    out=[]
    for raw in text.split("\n"):
        line=""
        for ch in raw:
            if d.textlength(line+ch,font=font)<=maxw: line+=ch
            else: out.append(line); line=ch
        out.append(line)
    return out
def rr(x,y,w,h,fill,outline=None,r=12,ow=2):
    d.rounded_rectangle([x,y,x+w,y+h],radius=r,fill=fill,outline=outline,width=ow)
def celltext(x,y,w,h,txt,font,fill,pad=10):
    lines=wrap(txt,font,w-2*pad); ch=font.size+5
    cy=y+(h-len(lines)*ch)//2+2
    for ln in lines:
        d.text((x+pad,cy),ln,font=font,fill=fill); cy+=ch
def arrow_down(cx,y0,y1,color):
    d.line([cx,y0,cx,y1-7],fill=color,width=3)
    d.polygon([(cx,y1),(cx-5,y1-8),(cx+5,y1-8)],fill=color)

# タイトル
d.text((50,34),"アカウント運用代行 × AI 業務フローマップ（主体別）",font=F(46),fill=NAVY)
d.text((52,98),"レーン＝誰が主体か。🤖AI(Claude)＝下書き/整形/要約　🏢弊社スタッフ＝判断/承認/制作/法務　📸インフルエンサー＝UGC制作　🤝クライアント＝依頼/素材/承認",font=F(20,False),fill=GRY)

LBL=230; MX=50; gap=12
steps_area=W-2*MX-LBL
cw=(steps_area-gap*5)//6
def cx(i): return MX+LBL+i*(cw+gap)
LH=150  # レーン高

def block(y0,ftitle,stepnames,lanes):
    # ブロック見出し
    rr(MX,y0,W-2*MX,46,NAVY,r=10); d.text((MX+16,y0+8),ftitle,font=F(28),fill="#FFFFFF")
    yhead=y0+58
    # ステップ見出し行（フロー矢印）
    d.text((MX+8,yhead+14),"ステップ",font=F(18),fill=GRY)
    for i,sn in enumerate(stepnames):
        x=cx(i); rr(x,yhead,cw,46,"#EEF2F6",outline=LINE,r=8,ow=1)
        celltext(x,yhead,cw,46,sn,F(20),NAVY)
        if i<5:
            ax=x+cw; ay=yhead+23
            d.line([ax,ay,ax+gap,ay],fill=GRY,width=3)
            d.polygon([(ax+gap,ay),(ax+gap-7,ay-5),(ax+gap-7,ay+5)],fill=GRY)
    # レーン
    yl=yhead+46+14
    laneY={}
    for li,(key,name,cells) in enumerate(lanes):
        hdr,bg=CO[key]
        ytop=yl+li*(LH+12)
        laneY[key]=ytop
        rr(MX,ytop,LBL-10,LH,hdr,r=10)
        celltext(MX,ytop,LBL-10,LH,name,F(22),"#FFFFFF")
        for i,c in enumerate(cells):
            x=cx(i)
            if c.strip():
                rr(x,ytop,cw,LH,bg,outline=hdr,r=12,ow=2)
                celltext(x,ytop,cw,LH,c,F(18,False),NAVY)
            else:
                rr(x,ytop,cw,LH,"#FAFBFC",outline="#E5E9EE",r=12,ow=1)
    return laneY,yl+len(lanes)*(LH+12)

# Flow A
y=160
stepsA=["①IF DM/メール","②UGC制作\n(レシピ/ハウツー)","③進行管理","④予約投稿","⑤DBへ集計","⑥月次レポート"]
lanesA=[
 ("AI","🤖 AI\n(Claude)",["DM/メール文面の下書き・返信案","台本/ブリーフ・キャプション案・競合リサーチ","スケジュール案・リマインド文・遅延要約","キャプション整形・最適時間・投稿前チェック","取込整形・表記揺れ吸収・集計","レポート下書き・数値要約・改善提案案"]),
 ("CO","🏢 弊社\nスタッフ",["送信・交渉・謝礼条件の決定","ブリーフ確定・ディレクション・法務最終","進行管理・優先順位の判断","公開の最終承認・投稿操作(権限)","データ確認","考察・最終承認"]),
 ("IF","📸 インフル\nエンサー",["","UGC制作(撮影・実演)","","(本人投稿/タグ付け)","",""]),
 ("CL","🤝 クライ\nアント",["(起用の承認)","","","投稿前の内容承認","","レポート受領・フィードバック"]),
]
laneYA,yend=block(y,"A. UGC制作フロー",stepsA,lanesA)
# AI→弊社 受け渡し矢印
for i in range(6):
    arrow_down(cx(i)+cw//2, laneYA["AI"]+LH, laneYA["CO"], CO["AI"][0])
# SocialPitt 帯
rr(MX,yend,W-2*MX,40,"#ECEFF3",outline=GRY,r=10,ow=1)
d.text((MX+16,yend+8),"🛠 SocialPitt：候補/成果物の進行管理 ・ 実績DB ・ 分析ダッシュボード（③〜⑥を支える）",font=F(19),fill=GRY)

# Flow B
y=yend+40+40
stepsB=["①クライアント\nとメール","②Tips制作\n(素材→)","③進行管理","④予約投稿","⑤DBへ集計","⑥月次レポート"]
lanesB=[
 ("AI","🤖 AI\n(Claude)",["返信・議事録化・論点整理・FAQ案","構成/台本/キャプション・素材要点抽出・レイアウト案","スケジュール案・リマインド文","キャプション整形・最適時間・投稿前チェック","取込整形・表記揺れ吸収・集計","レポート下書き・数値要約・改善提案案"]),
 ("CO","🏢 弊社\nスタッフ",["メール対応・要件整理","Tips制作(素材編集/デザイン仕上げ)・法務最終","進行管理・優先順位の判断","公開の最終承認・投稿操作(権限)","データ確認","考察・最終承認"]),
 ("CL","🤝 クライ\nアント",["要望・依頼","素材提供・内容承認","","(投稿前の承認)","","レポート受領・フィードバック"]),
]
laneYB,yend2=block(y,"B. Tipsコンテンツ制作フロー",stepsB,lanesB)
for i in range(6):
    arrow_down(cx(i)+cw//2, laneYB["AI"]+LH, laneYB["CO"], CO["AI"][0])
rr(MX,yend2,W-2*MX,40,"#ECEFF3",outline=GRY,r=10,ow=1)
d.text((MX+16,yend2+8),"🛠 SocialPitt：依頼/成果物の進行管理 ・ 実績DB ・ 分析ダッシュボード（③〜⑥を支える）",font=F(19),fill=GRY)

img.save(OUT); print("SAVED",OUT,img.size,"/ bottom",yend2)
