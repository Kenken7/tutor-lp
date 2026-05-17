#!/usr/bin/env python3
"""LINE リッチメニュー画像生成
2500x1686 サイズ・3列×2行、LP配色（ネイビー/バーガンディ/クリーム）"""

from PIL import Image, ImageDraw, ImageFont

W, H = 2500, 1686
COLS, ROWS = 3, 2
CW, CH = W // COLS, H // ROWS  # 833 x 843

# LP 配色
CREAM = (245, 240, 232)
NAVY = (26, 41, 68)
BURGUNDY = (107, 31, 46)
LINE = (210, 200, 188)

MINCHO = "/System/Library/Fonts/ヒラギノ明朝 ProN.ttc"
GOTHIC = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
GOTHIC_THIN = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"

f_label_en = ImageFont.truetype(GOTHIC_THIN, 36)
f_label_jp = ImageFont.truetype(MINCHO, 110)
f_small = ImageFont.truetype(GOTHIC_THIN, 28)

# 各マス: (日本語ラベル, 英語サブラベル, 一行説明)
cells = [
    ("体験申込", "TRIAL", "90分・半額"),
    ("料金プラン", "PRICING", "コース一覧"),
    ("指導の流れ", "FLOW", "申込から開始まで"),
    ("公式サイト", "WEBSITE", "tutor.kawaichan.com"),
    ("プロフィール", "TUTOR", "川井 康聖"),
    ("Q & A", "FAQ", "よくあるご質問"),
]

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

# 縦の仕切り線
for c in range(1, COLS):
    x = c * CW
    d.line([(x, 40), (x, H - 40)], fill=LINE, width=3)
# 横の仕切り線
for r in range(1, ROWS):
    y = r * CH
    d.line([(40, y), (W - 40, y)], fill=LINE, width=3)

# 外周フレーム（バーガンディの細枠）
d.rectangle([(0, 0), (W - 1, H - 1)], outline=BURGUNDY, width=8)

# 各マス描画
for i, (jp, en, desc) in enumerate(cells):
    col = i % COLS
    row = i // COLS
    cx = col * CW + CW // 2
    cy = row * CH + CH // 2

    # 上部 装飾線（バーガンディ）
    line_y = cy - 200
    d.line([(cx - 110, line_y), (cx + 110, line_y)], fill=BURGUNDY, width=4)

    # 英語ラベル（バーガンディ斜体風 — 太めゴシックで代用）
    d.text((cx, cy - 145), en, fill=BURGUNDY, font=f_label_en, anchor="mm")

    # 日本語ラベル（ネイビー明朝）
    d.text((cx, cy + 5), jp, fill=NAVY, font=f_label_jp, anchor="mm")

    # 一行説明（細ゴシック）
    d.text((cx, cy + 145), desc, fill=NAVY, font=f_small, anchor="mm")

out = "/Users/kwi/Desktop/tutor-lp/images/richmenu.png"
img.save(out, "PNG", optimize=True)
print(f"saved: {out}")
print(f"size: {W}x{H}")
