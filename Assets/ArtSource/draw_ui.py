"""Khung giao diện pixel (9-slice) cho IMGUI: bảng, nút, bảng tên, chú thích.
Chạy: python draw_ui.py → ghi vào Assets/Resources/UI/. Vẽ ở 1x rồi phóng x2 cho khớp độ to pixel của map.
Viền (border) khai báo trong DayController: panel 10, nút 8, bảng tên/chú thích 6."""
from PIL import Image
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
ASSETS = PARENT if os.path.basename(PARENT) == "Assets" else os.path.join(PARENT, "Assets")
OUT = os.path.join(ASSETS, "Resources", "UI")
os.makedirs(OUT, exist_ok=True)

GOLD_HI, GOLD, GOLD_LO = (226, 188, 104), (186, 142, 70), (120, 86, 44)


def frame(n, outline, rim_hi, rim_lo, fill, inner=None, corner=None, fill_alpha=255):
    img = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    px = img.load()
    for y in range(n):
        for x in range(n):
            edge = min(x, y, n - 1 - x, n - 1 - y)
            if edge == 0:
                if (x in (0, n - 1)) and (y in (0, n - 1)):
                    continue  # bo góc 1px
                c = outline + (255,)
            elif edge == 1:
                c = (rim_hi if (x == 1 or y == 1) and not (x == n - 2 or y == n - 2) else rim_lo) + (255,)
            elif edge == 2 and inner:
                c = inner + (255,)
            else:
                c = fill + (fill_alpha,)
            px[x, y] = c
    if corner:
        for cx, cy in ((3, 3), (n - 4, 3), (3, n - 4), (n - 4, n - 4)):
            px[cx, cy] = corner + (255,)
    return img


def save(img, name):
    img.resize((img.width * 2, img.height * 2), Image.NEAREST).save(os.path.join(OUT, name + ".png"))


def button(body, hi, lo, outline, inner=None):
    n = 12
    img = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    px = img.load()
    for y in range(n):
        for x in range(n):
            edge = min(x, y, n - 1 - x, n - 1 - y)
            if edge == 0:
                if (x in (0, n - 1)) and (y in (0, n - 1)):
                    continue
                c = outline
            elif inner and edge == 1:
                c = inner
            elif y <= 2:
                c = hi
            elif y >= n - 3:
                c = lo
            elif x == 1:
                c = hi
            elif x == n - 2:
                c = lo
            else:
                c = body
            px[x, y] = c + (255,)
    return img


if __name__ == "__main__":
    # bảng lớn: sơn mài tối, viền vàng đồng, chấm góc
    save(frame(16, (16, 10, 12), GOLD_HI, GOLD_LO, (32, 26, 30), inner=(46, 34, 30), corner=GOLD), "panel")
    # nút gỗ
    save(button((124, 78, 48), (166, 110, 66), (84, 52, 34), (34, 20, 16)), "button")
    save(button((148, 96, 56), (196, 138, 82), (98, 62, 38), (34, 20, 16), inner=GOLD_HI), "button_hover")
    save(button((96, 60, 38), (78, 48, 30), (112, 72, 44), (34, 20, 16), inner=GOLD), "button_down")
    # bảng tên trên map
    save(frame(10, (14, 10, 10), GOLD, GOLD_LO, (30, 24, 26), fill_alpha=236), "plaque")
    # chú thích: giấy dó
    save(frame(10, (70, 48, 30), (246, 236, 206), (196, 174, 130), (234, 220, 182)), "tip")
    print("done →", OUT)
