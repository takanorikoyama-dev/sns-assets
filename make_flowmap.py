# -*- coding: utf-8 -*-
"""アカウント運用代行 ×AI 業務フローマップ（A:UGC / B:Tips）スイムレーン図。"""
from PIL import Image, ImageDraw, ImageFont
import os
OUT="C:/Users/takanori.koyama/Desktop/Claude/sns-assets/flowmap_ops_ai.png"
W,H=2100,1500
img=Image.new("RGB",(W,H),"#FFFFFF"); d=ImageDraw.Draw(img)
def F(sz,bold=True):
    p="C:/Windows/Fonts/"+("YuGothB.ttc" if bold else "YuGothM.ttc")
    return ImageFont.truetype(p,sz)
NAVY="#16263A"; CY="#00A0DC"; CYBG="#E7F4FB"; AM="#E08600"; AMBG="#FFF3DF"
GRY="#5B6B7B"; GRYBG="#ECEFF3"; LINE="#C7D0D9"
def wrap(text,font,maxw):
    out=[]
    for raw in text.split("\n"):
        line=""
        for ch in raw:
            if d.textlength(line+ch,font=font)<=maxw: line+=ch
            else: out.append(line); line=ch
        out.append(line)
    return out
def boxtext(x,y,w,h,lines_spec,pad=12):
    cy=y+pad
    for txt,font,fill,gap in lines_spec:
        for ln in wrap(txt,font,w-2*pad):
            d.text((x+pad,cy),ln,font=font,fill=fill); cy+=font.size+gap
def rrect(x,y,w,h,fill,outline=None,r=14,ow=2):
    d.rounded_rectangle([x,y,x+w,y+h],radius=r,fill=fill,outline=outline,width=ow)

# タイトル
d.text((60,40),"アカウント運用代行 × AI 業務フローマップ",font=F(46),fill=NAVY)
d.text((62,104),"前提：運用担当が Claude を使える環境。🤖=AIで効率化（下書き/要約/整形/チェック）　🧑=人が介在（承認・交渉・撮影・法務・提出）　🛠=SocialPitt（進行管理＋分析DB）",font=F(20,False),fill=GRY)

cols=6; MX=60; gap=14
cw=(W-2*MX-gap*(cols-1))//cols
def colx(i): return MX+i*(cw+gap)

flows=[
 ("A. UGC制作フロー", [
   ("①IF DM/メール","候補の条件整理／パーソナライズ文面・返信・追客の下書き／敬語・翻訳","送信判断・関係構築/交渉・謝礼条件の決定"),
   ("②UGC制作(レシピ/ハウツー)","企画・構成・台本/ブリーフ／キャプション・ハッシュタグ案／競合リサーチ／薬機法・景表法チェック支援","撮影・実演／クリエイティブ最終判断／法務最終確認"),
   ("③進行管理","タスク分解・スケジュール案／リマインド文面／遅延の検知・要約","優先順位の意思決定・例外対応"),
   ("④予約投稿","キャプション整形／最適投稿時間の提案／投稿前チェック自動化","公開の最終承認・アカウント権限操作"),
   ("⑤DBへ集計","指標の取込・整形／表記揺れ吸収／異常値検知","データ接続の許可・最終確認"),
   ("⑥月次レポート","数値要約・考察ドラフト／KPI進捗の文章化／改善提案の素案・下書き","戦略考察・最終承認・クライアント提出"),
 ]),
 ("B. Tipsコンテンツ制作フロー", [
   ("①クライアントとメール","返信・議事録化／要件の論点整理／FAQ回答ドラフト／敬語・翻訳","送信・合意形成・交渉／機密判断"),
   ("②Tips制作(素材→)","構成・台本・キャプション／素材からの要点抽出／レイアウト下書き／薬機・景表チェック支援","撮影／デザイン最終仕上げ／法務・ブランド最終／クライアント承認取得"),
   ("③進行管理","タスク分解・スケジュール案／リマインド文面／遅延の検知・要約","優先順位の意思決定・例外対応"),
   ("④予約投稿","キャプション整形／最適投稿時間／投稿前チェック自動化","公開の最終承認・権限操作"),
   ("⑤DBへ集計","指標の取込・整形／表記揺れ吸収／異常値検知","データ接続の許可・確認"),
   ("⑥月次レポート","数値要約・考察ドラフト／KPI文章化／改善提案の素案","戦略考察・最終承認・提出"),
 ]),
]

y=150
for ftitle,steps in flows:
    # ブロック見出し
    rrect(MX,y,W-2*MX,46,NAVY,r=10); d.text((MX+16,y+8),ftitle,font=F(28),fill="#FFFFFF")
    yAI=y+58; hAI=190; yname=yAI+hAI+8; hname=44; yHU=yname+hname+8; hHU=190
    d.text((MX,yAI-2),"🤖 AIで効率化",font=F(20),fill=CY)
    d.text((MX,yHU-2+0),"",font=F(18),fill=AM)
    for i,(name,ai,hu) in enumerate(steps):
        x=colx(i)
        # AIセル
        rrect(x,yAI+26,cw,hAI-26,CYBG,outline=CY,r=12,ow=2)
        boxtext(x,yAI+26,cw,hAI-26,[(ai,F(17,False),NAVY,6)])
        # ステップ名
        rrect(x,yname,cw,hname,"#F4F7FA",outline=LINE,r=10,ow=1)
        d.text((x+12,yname+9),name,font=F(20),fill=NAVY)
        # 人セル
        rrect(x,yHU+26,cw,hHU-26,AMBG,outline=AM,r=12,ow=2)
        boxtext(x,yHU+26,cw,hHU-26,[(hu,F(17,False),"#5A3A00",6)])
        # 矢印
        if i<cols-1:
            ax=x+cw+2; ay=yname+hname//2
            d.line([ax,ay,ax+gap-2,ay],fill=GRY,width=3)
            d.polygon([(ax+gap-2,ay),(ax+gap-9,ay-5),(ax+gap-9,ay+5)],fill=GRY)
    d.text((MX,yHU-2),"🧑 人が介在（ゲート）",font=F(20),fill=AM)
    # SocialPitt 帯
    yb=yHU+hHU+12
    rrect(MX,yb,W-2*MX,40,GRYBG,outline=GRY,r=10,ow=1)
    d.text((MX+16,yb+8),"🛠 SocialPitt：候補/素材/成果物の進行管理 ・ 実績DB ・ 分析ダッシュボード（③〜⑥の基盤）",font=F(19),fill=GRY)
    y=yb+40+34

img.save(OUT)
print("SAVED",OUT,img.size)
