"""BtoB AX支援サービス素案のスライド(8枚・1920x1080)。大学生でも分かるビジュアル重視。"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
BG=(238,243,230); INK=(22,42,74); INK2=(60,84,120); GREEN=(92,144,90); GREEN_D=(70,118,70)
GREEN2=(150,188,140); GRAY=(96,110,100); WHITE=(255,255,255); CARD=(252,253,249)
ACCENT=(228,142,60); GOLD=(245,200,90); LIGHT=(245,248,240); SOFT=(232,240,228)
FB="C:/Windows/Fonts/YuGothB.ttc"; FM="C:/Windows/Fonts/YuGothM.ttc"
OUT="C:/Users/takanori.koyama/Desktop/Claude/sns-assets/slides"
os.makedirs(OUT, exist_ok=True)
TOTAL=10

def F(p,s): return ImageFont.truetype(p,s)

def wrap(d,t,f,maxw):
    out=[];cur=""
    for ch in t:
        if ch=="\n": out.append(cur);cur="";continue
        if d.textlength(cur+ch,font=f)<=maxw: cur+=ch
        else: out.append(cur);cur=ch
    if cur:out.append(cur)
    return out

def ctext(d,t,f,cx,y,fill):
    w=d.textlength(t,font=f); d.text((cx-w/2,y),t,font=f,fill=fill)

def base(title,page,sub=None):
    img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)
    d.rounded_rectangle((60,52,72,108),radius=6,fill=GREEN)
    d.text((92,48),title,font=F(FB,46),fill=INK)
    if sub: d.text((94,108),sub,font=F(FM,26),fill=INK2)
    d.text((W-180,60),f"{page} / {TOTAL}",font=F(FM,28),fill=GRAY)
    d.line((60,150,W-60,150),fill=GREEN2,width=3)
    d.text((60,H-52),"GREE｜AX支援サービス 素案",font=F(FM,22),fill=GRAY)
    return img,d

def card(d,box,fill=CARD,outline=GREEN,width=4,radius=20):
    d.rounded_rectangle(box,radius=radius,fill=fill,outline=outline,width=width)

def chip(d,x,y,text,col=GREEN,tcol=WHITE,fs=24,padx=18,pady=10):
    f=F(FB,fs); tw=d.textlength(text,font=f)
    d.rounded_rectangle((x,y,x+tw+padx*2,y+fs+pady*2),radius=(fs+pady*2)//2,fill=col)
    d.text((x+padx,y+pady),text,font=f,fill=tcol)
    return x+tw+padx*2

def arrow(d,x1,y1,x2,y2,col=INK2,w=5,head=14):
    d.line((x1,y1,x2,y2),fill=col,width=w)
    import math
    ang=math.atan2(y2-y1,x2-x1)
    d.polygon([(x2,y2),(x2-head*math.cos(ang-0.4),y2-head*math.sin(ang-0.4)),
               (x2-head*math.cos(ang+0.4),y2-head*math.sin(ang+0.4))],fill=col)

def table(d,x,y,colw,rows,fs=22,header_fill=GREEN,head_tcol=WHITE,zebra=True,hi_row=None):
    f=F(FM,fs); fh=F(FB,fs)
    # row heights from wrapped content
    heights=[]
    for r,row in enumerate(rows):
        maxlines=1
        for c,cell in enumerate(row):
            ff = fh if r==0 else f
            maxlines=max(maxlines,len(wrap(d,str(cell),ff,colw[c]-24)))
        heights.append(20+maxlines*(fs+8))
    yy=y
    for r,row in enumerate(rows):
        xx=x; rh=heights[r]
        for c,cell in enumerate(row):
            if r==0: fill=header_fill
            elif hi_row is not None and r==hi_row: fill=(255,244,228)
            elif zebra and r%2==0: fill=SOFT
            else: fill=CARD
            d.rectangle((xx,yy,xx+colw[c],yy+rh),fill=fill,outline=GREEN2,width=2)
            ff = fh if (r==0 or c==0) else f
            tc = head_tcol if r==0 else (ACCENT if (hi_row is not None and r==hi_row and c==0) else INK)
            ly=yy+10
            for ln in wrap(d,str(cell),ff,colw[c]-24):
                d.text((xx+12,ly),ln,font=ff,fill=tc); ly+=fs+8
            xx+=colw[c]
        yy+=rh
    return yy

def save(img,n): img.save(f"{OUT}/btob-{n:02d}.png","PNG")

# ===== S1 表紙 =====
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)
d.rounded_rectangle((0,0,W,16),fill=GREEN)
ctext(d,"BtoB AX支援サービス（素案）",F(FB,86),W/2,330,INK)
ctext(d,"SNS運用 × AI × 人 × SocialPitt",F(FB,46),W/2,470,GREEN_D)
ctext(d,"「続ける」だけでなく「伸ばす」。",F(FM,38),W/2,580,INK2)
ctext(d,"フォロワー・エンゲージメント拡大まで、代理店が伴走する。",F(FM,38),W/2,636,INK2)
chipx=W/2-150
d.rounded_rectangle((W/2-220,760,W/2+220,824),radius=32,fill=GREEN)
ctext(d,"GREE ／ 2026-06 ／ 大学生でも分かる版",F(FB,26),W/2,778,WHITE)
save(img,1)

# ===== S2 課題 =====
img,d=base("よくある悩み：「投稿は続いた。でも“伸びない”。」",2)
# 左カード：AIだけ
card(d,(80,200,940,560),outline=GRAY)
d.text((110,225),"AIだけだと…",font=F(FB,34),fill=INK)
chip(d,110,300,"効率（量・継続・一貫性）",GREEN); d.text((600,308),"○ 出る",font=F(FB,30),fill=GREEN_D)
chip(d,110,380,"成果（フォロワー・ENG）",GRAY); d.text((600,388),"△ 不透明",font=F(FB,30),fill=ACCENT)
d.text((110,470),"量産はできても、“伸ばす”仕掛けが足りない。",font=F(FM,26),fill=INK2)
# 右：ペイン一覧
card(d,(980,200,1840,560),outline=ACCENT)
d.text((1010,225),"現場のペイン",font=F(FB,34),fill=INK)
for i,t in enumerate(["ネタ切れ・制作工数で続かない","トンマナ・品質がぶれる",
                      "何を出せばいいか戦略がない","効果が見えない／改善できない"]):
    yy=300+i*60
    d.ellipse((1015,yy+6,1035,yy+26),fill=ACCENT)
    d.text((1055,yy),t,font=F(FM,28),fill=INK)
ctext(d,"「効率」と「成果」は別物。成果には“もう2つの力”が要る。",F(FB,36),W/2,640,ACCENT)
save(img,2)

# ===== S3 解：3レイヤー =====
img,d=base("解決：3つの力を組み合わせる",3)
cards=[("AI（仕組み）",GREEN,"続ける／そろえる","半自動で量産・キャラ統一・予約投稿"),
       ("人（GREE）",ACCENT,"当てる／磨く","戦略・編集・コメント運用・改善判断"),
       ("SocialPitt",GREEN_D,"測る／回す","KPI可視化・競合ベンチ・勝ち筋抽出")]
bw=560; gap=40; x0=80; ty=210
for i,(t,col,role,desc) in enumerate(cards):
    x=x0+i*(bw+gap)
    card(d,(x,ty,x+bw,ty+330),outline=col)
    d.rounded_rectangle((x,ty,x+bw,ty+74),radius=20,fill=col); d.rectangle((x,ty+46,x+bw,ty+74),fill=col)
    ctext(d,t,F(FB,38),x+bw/2,ty+14,WHITE)
    ctext(d,role,F(FB,40),x+bw/2,ty+110,col)
    for j,ln in enumerate(wrap(d,desc,F(FM,28),bw-60)):
        ctext(d,ln,F(FM,28),x+bw/2,ty+200+j*40,INK)
# ループ
ly=600
nodes=["データ(SocialPitt)","人が“次の企画”に翻訳","AIが量産","投稿→計測"]
nx=110; nw=400; ng=60
for i,t in enumerate(nodes):
    x=nx+i*(nw+ng)
    card(d,(x,ly,x+nw,ly+90),fill=LIGHT,outline=GREEN2,width=3,radius=16)
    ctext(d,t,F(FB,26),x+nw/2,ly+30,INK)
    if i<len(nodes)-1: arrow(d,x+nw+8,ly+45,x+nw+ng-8,ly+45)
arrow(d,nx+ (nw+ng)*3+nw/2, ly+98, nx+nw/2, ly+98+0, col=GREEN)  # placeholder
d.line((nx+nw/2,ly+150,nx+(nw+ng)*3+nw/2,ly+150),fill=GREEN,width=4)
d.line((nx+nw/2,ly+98,nx+nw/2,ly+150),fill=GREEN,width=4)
d.line((nx+(nw+ng)*3+nw/2,ly+98,nx+(nw+ng)*3+nw/2,ly+150),fill=GREEN,width=4)
arrow(d,nx+nw/2,ly+150,nx+nw/2,ly+102,col=GREEN)
ctext(d,"このループ（PDCA）が回るほど伸びる",F(FB,30),W/2,ly+170,GREEN_D)
save(img,3)

# ===== S4 KPIツリー =====
img,d=base("なぜ“伸びる”のか（フォロワーの増え方）",4)
card(d,(80,200,1840,360),fill=LIGHT,outline=GREEN)
ctext(d,"フォロワー純増 ＝ リーチ × プロフィール訪問率 × フォロー転換率 −（離脱）",F(FB,40),W/2,250,INK)
ctext(d,"ENG率 ＝ （保存＋いいね＋コメント＋シェア）÷ リーチ",F(FB,36),W/2,310,INK2)
rows=[["伸ばす要素","担い手","具体"],
      ["露出量（量・継続・一貫性）","AI","半自動で量産・毎日投稿"],
      ["当たり化（実用性・フック・トンマナ）","人(GREE)","企画・編集・見せ方"],
      ["最適化（時間/ハッシュタグ/競合比較）","SocialPitt","データで勝ち筋を発見"],
      ["関係づくり（コメント返信）","人(GREE)","ファン化→アルゴリズム評価↑"]]
table(d,80,400,[700,300,760],rows,fs=26)
save(img,4)

# ===== S5 オペレーション =====
img,d=base("回し方（毎週まわすPDCA）",5)
cyc=["①分析\n(SocialPitt)","②企画\n(人)","③量産\n(AI)","④承認\n(顧客)","⑤投稿\n→運用(人)"]
nw=300;ng=60;x0=110;ty=260
for i,t in enumerate(cyc):
    x=x0+i*(nw+ng)
    col=ACCENT if i==3 else GREEN
    card(d,(x,ty,x+nw,ty+170),outline=col)
    for j,ln in enumerate(t.split("\n")):
        ctext(d,ln,F(FB,34),x+nw/2,ty+40+j*48,(ACCENT if i==3 else INK))
    if i<len(cyc)-1: arrow(d,x+nw+8,ty+85,x+nw+ng-8,ty+85)
# loop back
bx0=x0+nw/2; bxN=x0+(nw+ng)*4+nw/2
d.line((bx0,ty+178,bx0,ty+250),fill=GREEN,width=4)
d.line((bxN,ty+178,bxN,ty+250),fill=GREEN,width=4)
d.line((bx0,ty+250,bxN,ty+250),fill=GREEN,width=4)
arrow(d,bx0,ty+250,bx0,ty+182,col=GREEN)
ctext(d,"週次：勝ち筋を翌週の企画へ反映　／　月次：戦略・テーマ配分・広告ブーストを見直し",F(FM,30),W/2,ty+300,INK2)
ctext(d,"④承認（顧客）＝“勝手に出さない”安全装置",F(FB,30),W/2,ty+370,ACCENT)
save(img,5)

# ===== S6 権限・セキュリティ =====
img,d=base("安心して任せられる仕組み（権限・セキュリティ）",6)
rows=[["観点","どうする"],
      ["アカウント所有","クライアントが保有（代理店に譲渡しない）"],
      ["代理店の権限","Metaパートナー連携で“最小権限”のみ付与"],
      ["代行投稿","可。ただし最終OK（承認）は必ず顧客"],
      ["トークン/秘密情報","顧客資産として管理・平文コミット禁止・漏洩時は即再発行"],
      ["記録","誰が承認・投稿したかの監査ログを保持"],
      ["AIに入れない","顧客の機密・個人情報は投入しない"],
      ["ブランドセーフティ","炎上回避チェック（誇大・不安訴求・権利侵害を排除）"]]
table(d,80,200,[460,1300],rows,fs=26)
chip(d,80,H-150,"キモ：代行はするが、“最終OKは顧客”＋データは守る",ACCENT,WHITE,28)
save(img,6)

# ===== S7 パッケージ =====
img,d=base("料金プラン（4段階・成果志向）",7)
rows=[["プラン","狙い","AI","人(GREE)","SocialPitt","投稿/レポート","KPI"],
      ["① Starter","立ち上げ","設計・テンプレ・初期投稿","戦略設計・初期伴走","KPI設計＋ダッシュボード","月8〜12／月次","基盤・初期母数"],
      ["② Standard","続けて磨く","半自動量産・予約","編集監修・週次改善・コメント","週次分析・ベンチ","月12〜20／隔週","ENG率改善"],
      ["③ Growth ★","伸ばす","量産＋A/B＋リール","プランナー＋アナリスト本格","高度分析・競合/タグ最適化","月20〜30＋リール／週次","フォロワー純増・ENGに数値コミット"],
      ["④ Enablement","内製化/研修","仕組み移管・プロンプト資産","研修・伴走・レビュー","自社運用へ移管","顧客運用／月次","内製能力の獲得"]]
cw=[200,150,250,250,250,290,290]
table(d,40,185,cw,rows,fs=20,hi_row=3)
ctext(d,"成果（フォロワー/ENG）が要件なら → 人＋SocialPittの比重が高い ③Growth が必須",F(FB,28),W/2,H-110,ACCENT)
save(img,7)

# ===== S8 提供の座組マトリクス（A/B/C） =====
img,d=base("提供の座組（A／B／C）— AI活用の観点で",8)
rows=[["観点","A：フル外注","B：部分外注","C：AI内製化コンサル"],
 ["クライアントの役割","承認＋レポート受領＋継続判断のみ","自社制作・投稿は内製／一部を選択外注","運用は自社（仕組みを受け取る）"],
 ["GREEの役割","企画〜制作〜投稿〜分析〜改善まで全部代行","選択領域(キャンペーン/UGC/SocialPitt)を支援","Claude活用の内製化を設計・実装・研修"],
 ["AI活用（誰が使う）","GREEがAIで量産・効率化（顧客はAIレス）","役割分担：外注=GREEのAI／内製=顧客","顧客自身がAIで作れるように（AIの民主化）"],
 ["SocialPitt","GREEが運用しレポート","分析だけ単体外注も可","自社ダッシュボードとして導入支援"],
 ["人(GREE)の関与","高（フル運用）","中（選択領域のみ）","初期=高 → 移管後=低"],
 ["向く顧客","リソース無い／丸ごと任せたい","内製体制あり／繁忙・専門領域を補完","内製化・恒久コスト削減・ノウハウ蓄積"],
 ["課金イメージ","月額運用（高）","メニュー/プロジェクト＋SocialPitt月額","コンサル/実装プロジェクト＋研修"],
 ["対応パッケージ","②Standard〜③Growth","①Starter／②部分＋オプション","④Enablement（＋①設計）"]]
table(d,60,180,[300,500,500,500],rows,fs=20)
chip(d,60,H-150,"A：提供中",GREEN,WHITE,24)
chip(d,300,H-150,"B：提供中",GREEN,WHITE,24)
chip(d,560,H-150,"C：新規（今回追加）",ACCENT,WHITE,24)
save(img,8)

# ===== S9 AI活用の3類型 =====
img,d=base("AI活用の3類型（座組の本質＝“誰がAIを操るか”）",9)
cards=[("代行型（A）",GREEN,"GREEがAIで“代わりに”回す","手離れ・継続・成果重視","②③ / フル外注"),
       ("ハイブリッド型（B）",ACCENT,"AIの使い手を分担する","柔軟・コスト最適・補完","① 部分＋SocialPitt"),
       ("内製化型（C）",GREEN_D,"顧客がAIを使えるように","自走・恒久効率・ノウハウ","④ Enablement")]
bw=560;gap=40;x0=80;ty=210
for i,(t,col,role,val,pkg) in enumerate(cards):
    x=x0+i*(bw+gap)
    card(d,(x,ty,x+bw,ty+420),outline=col)
    d.rounded_rectangle((x,ty,x+bw,ty+74),radius=20,fill=col); d.rectangle((x,ty+46,x+bw,ty+74),fill=col)
    ctext(d,t,F(FB,36),x+bw/2,ty+16,WHITE)
    ctext(d,role,F(FB,30),x+bw/2,ty+110,col)
    d.text((x+40,ty+185),"提供価値",font=F(FB,24),fill=GRAY)
    for j,ln in enumerate(wrap(d,val,F(FM,28),bw-80)):
        d.text((x+40,ty+222+j*38),ln,font=F(FM,28),fill=INK)
    d.text((x+40,ty+320),"対応",font=F(FB,24),fill=GRAY)
    d.text((x+40,ty+356),pkg,font=F(FB,26),fill=col)
card(d,(80,680,1840,800),fill=LIGHT,outline=GREEN_D)
ctext(d,"どれもAIが“てこ”。違いは「誰がAIを操るか」だけ。",F(FB,40),W/2,710,GREEN_D)
ctext(d,"顧客の体制・目的に合わせて A/B/C を選ぶ（組み合わせも可）",F(FM,28),W/2,766,INK2)
save(img,9)

# ===== S10 導入ステップ＋まとめ =====
img,d=base("はじめ方（3ステップ）とまとめ",10)
steps=[("STEP 1","自社で実証","ai_coach_korekara を実績化（100フォロワー＆運用データ）"),
       ("STEP 2","パイロット1社","Growthで試行→フロー・権限・セキュリティを実地検証"),
       ("STEP 3","横展開","標準パッケージ化→最後に提案資料を作成")]
bw=560;gap=40;x0=80;ty=220
for i,(s,t,desc) in enumerate(steps):
    x=x0+i*(bw+gap)
    card(d,(x,ty,x+bw,ty+300),outline=GREEN)
    d.rounded_rectangle((x,ty,x+bw,ty+70),radius=20,fill=GREEN); d.rectangle((x,ty+42,x+bw,ty+70),fill=GREEN)
    ctext(d,s,F(FB,34),x+bw/2,ty+12,WHITE)
    ctext(d,t,F(FB,40),x+bw/2,ty+100,INK)
    for j,ln in enumerate(wrap(d,desc,F(FM,26),bw-60)):
        ctext(d,ln,F(FM,26),x+bw/2,ty+180+j*38,INK2)
    if i<2: arrow(d,x+bw+6,ty+150,x+bw+gap-6,ty+150)
card(d,(80,600,1840,760),fill=LIGHT,outline=GREEN_D)
ctext(d,"AIで速く。人で外さない。データで伸ばす。",F(FB,52),W/2,650,GREEN_D)
ctext(d,"“続ける”を超えて、“伸びる”をBtoBへ。",F(FM,32),W/2,720,INK2)
save(img,10)

print(f"done: {TOTAL} slides ->",OUT)
