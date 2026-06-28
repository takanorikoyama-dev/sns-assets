# -*- coding: utf-8 -*-
"""開始画像から15-18秒のリールを完全ローカル生成（無料）。
ゆっくりズーム(Ken Burns)＋微ドリフト＋字幕アニメ＋やわらかBGM。"""
import os, subprocess, shutil
import imageio_ffmpeg

BASE = "C:/Users/takanori.koyama/Desktop/Claude/sns-assets"
SRC  = f"{BASE}/reel_starts/R7_start.jpg"
OUT  = f"{BASE}/videos/reel_R7.mp4"
os.makedirs(f"{BASE}/videos", exist_ok=True)
DUR  = 18

shutil.copy("C:/Windows/Fonts/YuGothB.ttc", f"{BASE}/_yugo.ttc")

# R7 字幕（5ビート・上部ミント余白に表示／手動改行で幅調整）
caps = [
    (0.2, 3.2,  "AI、もう71%が\n使ってる。"),
    (3.6, 7.2,  "でも“使いこなせてる”\nのは約23%だけ。"),
    (7.6,11.2,  "＝差がつくのは\nこれから。"),
    (11.6,15.0, "勝ち筋は\n“毎日ひとつ試す”。"),
    (15.4,18.0, "今日のひとつ、\n何にする？"),
]
for i,(a,b,t) in enumerate(caps,1):
    with open(f"{BASE}/_r7_{i}.txt","w",encoding="utf-8") as f:
        f.write(t)

# ゆっくりズーム＋微ドリフト（2x拡大してから zoompan で滑らかに）
vf = (
    "scale=2160:3840,"
    "zoompan=z='min(1.0+0.0010*on,1.13)':"
    "x='iw/2-(iw/zoom/2)+sin(on/50)*12':"
    "y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,"
    "format=yuv420p"
)
# 字幕（濃ネイビー＋白縁・フェードイン/アウト）
# zoompanがPTSを乱すため、タイミングはフレーム番号 n で指定（30fps）
FPS=30; FADE=12  # 0.4s
draws=[]
for i,(a,b,_) in enumerate(caps,1):
    fa=int(a*FPS); fb=int(b*FPS)
    fade=(f"alpha='if(lt(n,{fa}),0,if(lt(n,{fa}+{FADE}),(n-{fa})/{FADE},"
          f"if(lt(n,{fb}-{FADE}),1,if(lt(n,{fb}),({fb}-n)/{FADE},0))))'")
    draws.append(
        f"drawtext=fontfile=_yugo.ttc:textfile=_r7_{i}.txt:expansion=none:"
        f"fontcolor=0x16263A:fontsize=72:line_spacing=14:"
        f"borderw=5:bordercolor=white@0.85:"
        f"x=(w-text_w)/2:y=150:enable='between(n,{fa},{fb})':{fade}"
    )
vf = vf + "," + ",".join(draws)

# やわらかBGM（C4+E4の柔らかいパッド・トレモロ・低音量・フェード）
abuf = (f"aevalsrc=0.18*sin(2*PI*261.63*t)+0.14*sin(2*PI*329.63*t)"
        f"+0.10*sin(2*PI*392.0*t):d={DUR}:s=44100,"
        f"tremolo=f=0.18:d=0.4,lowpass=f=1100,volume=0.12,"
        f"afade=t=in:d=2,afade=t=out:st={DUR-2.5}:d=2.5")

ff = imageio_ffmpeg.get_ffmpeg_exe()
cmd=[ff,"-y","-loop","1","-t",str(DUR),"-i",SRC,
     "-f","lavfi","-i",abuf,
     "-vf",vf,"-c:v","libx264","-pix_fmt","yuv420p","-r","30",
     "-c:a","aac","-b:a","128k","-shortest","-movflags","+faststart",OUT]
print("rendering...")
p=subprocess.run(cmd,cwd=BASE,capture_output=True,text=True,encoding="utf-8",errors="ignore")
if p.returncode!=0:
    print("ERR:\n",p.stderr[-1800:])
else:
    print("OK ->",OUT,os.path.getsize(OUT),"bytes")
