#!/usr/bin/env python3
"""TOEFL ITP Score Report の個人情報部分を黒塗りマスク"""

from PIL import Image, ImageDraw, ImageFont
import sys

src = "/Users/kwi/Downloads/Kose_Score.jpg"
dst = "/Users/kwi/Desktop/tutor-lp/images/toefl-score.jpg"
debug = "/Users/kwi/Desktop/tutor-lp/images/toefl-score-debug.jpg"

img = Image.open(src).convert("RGB")
W, H = img.size
print(f"size: {W}x{H}")

# === Debug: グリッド描画版 ===
if "--debug" in sys.argv:
    dbg = img.copy()
    d = ImageDraw.Draw(dbg)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", 20)
    except Exception:
        font = ImageFont.load_default()
    # 縦100pxごとの線+ラベル
    for x in range(0, W, 100):
        d.line([(x, 0), (x, H)], fill=(255, 0, 0), width=1)
        d.text((x + 2, 2), str(x), fill=(255, 0, 0), font=font)
    for y in range(0, H, 50):
        d.line([(0, y), (W, y)], fill=(0, 0, 255), width=1)
        d.text((2, y + 2), str(y), fill=(0, 0, 255), font=font)
    dbg.save(debug, "JPEG", quality=80)
    print(f"debug saved: {debug}")
    sys.exit(0)

# === 本番マスク ===
draw = ImageDraw.Draw(img)

# 上部のセンシティブ情報を黒塗り
regions = [
    # DOB の値「11/22/2003」
    (220, 280, 520, 340),
    # Student Number の値「2201057」
    (1450, 225, 1800, 290),
]
for x1, y1, x2, y2 in regions:
    draw.rectangle([(x1, y1), (x2, y2)], fill=(20, 20, 20))

# 下端のシリアル行（I.N. 770462, 153761-16573 等）はクロップで消す
img_cropped = img.crop((0, 0, W, 780))

img_cropped.save(dst, "JPEG", quality=88)
print(f"saved: {dst} (cropped to {img_cropped.size})")
