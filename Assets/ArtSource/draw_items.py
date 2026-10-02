"""Icon 24x24 cho kỷ vật, đồ lễ, đồ chiến đấu và nguyên liệu. Đổ bóng theo bậc, viền màu.
Chạy: python draw_items.py → ghi thẳng vào Assets/Resources/Items/<tên bỏ dấu>.png"""
from PIL import Image, ImageDraw, ImageFont
import math
import os

N = 24
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
ASSETS = PARENT if os.path.basename(PARENT) == "Assets" else os.path.join(PARENT, "Assets")
OUT = os.path.join(ASSETS, "Resources", "Items")
PREVIEW = os.path.join(HERE, "sprites")
os.makedirs(OUT, exist_ok=True)
os.makedirs(PREVIEW, exist_ok=True)


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c[:3])


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


class I:
    def __init__(self):
        self.img = Image.new("RGBA", (N, N), (0, 0, 0, 0))
        self.px = self.img.load()

    def p(self, x, y, c, a=255):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < N and 0 <= y < N:
            self.px[x, y] = tuple(c[:3]) + (a,)

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.p(x, y, c)

    def blob(self, cx, cy, rx, ry, base, light=1.2, dark=0.68, tones=4):
        for y in range(int(cy - ry - 1), int(cy + ry + 2)):
            for x in range(int(cx - rx - 1), int(cx + rx + 2)):
                dx, dy = (x - cx) / (rx + 0.4), (y - cy) / (ry + 0.4)
                if dx * dx + dy * dy <= 1:
                    t = (dx + dy * 1.1) * 0.5 + 0.5
                    step = min(tones - 1, max(0, int(t * tones)))
                    self.p(x, y, shade(base, light + (dark - light) * step / (tones - 1)))

    def line(self, x0, y0, x1, y1, c, w=1):
        n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
        for i in range(n + 1):
            t = i / max(1, n)
            for k in range(w):
                self.p(x0 + (x1 - x0) * t + k, y0 + (y1 - y0) * t, c)

    def poly(self, pts, c):
        ImageDraw.Draw(self.img).polygon(pts, fill=tuple(c) + (255,))

    def outline(self):
        src = self.img.copy().load()
        for y in range(N):
            for x in range(N):
                if src[x, y][3]:
                    continue
                nb = [src[x + dx, y + dy] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                      if 0 <= x + dx < N and 0 <= y + dy < N and src[x + dx, y + dy][3] > 100]
                if nb:
                    d = min(nb, key=lambda c: c[0] + c[1] + c[2])
                    self.px[x, y] = mix(shade(d, 0.4), (28, 20, 24), 0.5) + (255,)


def tray(s, cy=15):
    """Mẹt tre đan: hình bầu dục nhìn nghiêng, có vân đan."""
    rim, weave = (150, 108, 62), (190, 146, 90)
    s.blob(12, cy + 2, 10, 5, rim, 1.1, 0.7, 3)
    for y in range(cy - 1, cy + 5):
        for x in range(3, 21):
            if ((x - 12) / 9.0) ** 2 + ((y - cy - 1) / 3.6) ** 2 <= 1:
                s.p(x, y, weave if (x + y) % 3 else shade(weave, 0.82))


# ---------- Kỷ vật ----------

def chuong_ba_noi():
    s = I()
    brass = (214, 168, 64)
    s.rect(11, 1, 12, 3, (196, 44, 44))  # dây đỏ
    s.blob(12, 4, 2, 1.5, brass)
    for y in range(5, 18):  # thân chuông loe dần
        half = 3 + (y - 5) * 0.55 + (2 if y > 15 else 0)
        for x in range(int(12 - half), int(12 + half) + 1):
            t = (x - 12) / half
            c = shade(brass, 1.25 if t < -0.5 else 1.05 if t < 0 else 0.85 if t < 0.55 else 0.68)
            s.p(x, y, c)
    s.rect(4, 18, 20, 18, shade(brass, 0.6))
    s.rect(5, 10, 18, 10, shade(brass, 0.78))  # vành trang trí
    s.p(8, 7, (255, 240, 190)); s.p(8, 8, (250, 220, 140))
    s.blob(12, 20, 1.5, 1.5, (120, 90, 40))  # quả lắc
    s.outline()
    return s


def dieu_hai_lam():
    s = I()
    s.poly([(12, 1), (21, 9), (12, 17), (3, 9)], (232, 164, 52))
    s.poly([(12, 1), (21, 9), (12, 9)], (246, 196, 82))
    s.poly([(3, 9), (12, 17), (12, 9)], (206, 126, 40))
    s.line(12, 1, 12, 17, (120, 76, 40))
    s.line(3, 9, 21, 9, (120, 76, 40))
    for i, (x, y) in enumerate(((13, 18), (14, 20), (16, 21), (18, 22), (20, 23))):  # đuôi diều
        s.p(x, y, (200, 50, 46) if i % 2 == 0 else (240, 230, 210))
        s.p(x + 1, y, (200, 50, 46) if i % 2 == 0 else (240, 230, 210))
    s.outline()
    return s


def luu_but_nhom():
    s = I()
    cover = (124, 76, 52)
    s.rect(1, 6, 22, 19, cover)
    s.rect(2, 5, 11, 18, (244, 234, 210))
    s.rect(12, 5, 21, 18, (232, 220, 194))
    s.rect(11, 5, 12, 18, shade(cover, 0.8))
    for y in (8, 10, 12, 14):
        s.rect(4, y, 9, y, (120, 110, 150))
        s.rect(14, y, 19 - (y == 14) * 3, y, (120, 110, 150))
    s.rect(17, 3, 18, 8, (196, 44, 44))  # dải đánh dấu
    s.rect(2, 18, 11, 18, (210, 198, 176))
    s.outline()
    return s


def luu_but():
    s = I()
    blue = (62, 92, 158)
    s.rect(5, 2, 19, 21, blue)
    s.rect(5, 2, 7, 21, shade(blue, 1.25))
    s.rect(17, 2, 19, 21, shade(blue, 0.75))
    s.rect(18, 3, 20, 21, (236, 226, 204))  # mép giấy
    s.rect(9, 6, 16, 10, (232, 218, 176))  # nhãn
    s.rect(10, 8, 15, 8, (150, 130, 100))
    s.rect(5, 15, 19, 16, (214, 176, 72))  # dây gài
    s.outline()
    return s


def bi_ve():
    s = I()
    s.blob(12, 12, 8, 8, (70, 170, 120), 1.3, 0.6, 5)
    for i in range(10):  # vân xoắn trong viên bi
        a = i * 0.6
        s.p(12 + math.cos(a) * (2 + i * 0.45), 12 + math.sin(a) * (2 + i * 0.45), (200, 60, 60) if i % 3 else (240, 240, 220))
    s.rect(7, 7, 8, 8, (240, 255, 245))
    s.p(9, 6, (210, 240, 225))
    s.outline()
    return s


def la_ban_tu_che():
    s = I()
    s.blob(12, 12, 10, 10, (176, 128, 70), 1.25, 0.65, 4)
    s.blob(12, 12, 7, 7, (240, 232, 210), 1.05, 0.88, 2)
    for a in range(0, 360, 45):
        x, y = 12 + math.cos(math.radians(a)) * 6, 12 + math.sin(math.radians(a)) * 6
        s.p(x, y, (120, 100, 80))
    s.line(12, 6, 12, 11, (200, 40, 40))
    s.line(12, 13, 12, 18, (60, 80, 150))
    s.p(12, 12, (60, 50, 40))
    s.rect(11, 0, 13, 2, (176, 128, 70))
    s.outline()
    return s


def anh_nhom_7():
    s = I()
    s.rect(1, 3, 22, 20, (150, 112, 66))
    s.rect(1, 3, 22, 3, (186, 146, 92))
    s.rect(3, 5, 20, 18, (150, 188, 214))  # trời
    s.rect(3, 14, 20, 18, (110, 150, 80))  # cỏ
    colors = [(60, 70, 120), (230, 180, 50), (60, 120, 80), (230, 230, 236), (120, 118, 70), (60, 46, 44), (226, 232, 236)]
    for i, c in enumerate(colors):  # 7 người
        x = 4 + i * 2 + (1 if i > 3 else 0)
        s.p(x, 11, (236, 192, 156))
        s.p(x, 10, (30, 26, 30))
        s.rect(x, 12, x, 14, c)
    s.rect(18, 5, 20, 8, (100, 100, 120))  # góc ảnh ố
    s.outline()
    return s


# ---------- Đồ lễ ----------

def met_gao_muoi():
    s = I()
    tray(s)
    s.blob(8, 12, 4, 3, (246, 244, 236), 1.05, 0.82, 3)
    s.blob(16, 12, 4, 3, (226, 232, 240), 1.08, 0.8, 3)
    for x, y in ((7, 11), (9, 12), (15, 11), (17, 12)):
        s.p(x, y, (255, 255, 255))
    s.outline()
    return s


def bo_nhang():
    s = I()
    for i, x in enumerate(range(6, 18, 2)):
        top = 3 + (i % 3)
        s.rect(x, top, x, 20, (156, 70, 50) if i % 2 else (176, 84, 58))
        s.rect(x, top, x, top + 1, (250, 150, 60))  # đầu nhang cháy
        s.p(x, top - 2, (180, 180, 190), 160)
    s.rect(5, 15, 18, 18, (196, 40, 40))  # giấy đỏ bó
    s.rect(5, 16, 18, 16, (230, 190, 70))
    s.outline()
    return s


def met_trau_cau():
    s = I()
    tray(s)
    for cx, cy in ((7, 12), (11, 11)):  # lá trầu gấp
        s.blob(cx, cy, 3, 2.5, (70, 140, 60), 1.2, 0.7, 3)
    s.blob(16, 11, 2.5, 2.5, (214, 140, 50))  # quả cau
    s.blob(18, 13, 2, 2, (196, 120, 40))
    s.p(15, 10, (250, 200, 120))
    s.outline()
    return s


def bo_hoa_hue():
    s = I()
    for x0, x1 in ((11, 8), (12, 12), (13, 16)):
        s.line(x0, 21, x1, 8, (70, 130, 60))
    for cx, cy in ((8, 6), (12, 4), (16, 6), (10, 9), (14, 9)):
        s.blob(cx, cy, 2, 2, (248, 248, 240), 1.0, 0.82, 2)
        s.p(cx, cy, (240, 220, 140))
    s.poly([(8, 16), (16, 16), (14, 22), (10, 22)], (200, 50, 50))  # giấy gói
    s.rect(9, 17, 15, 17, (230, 190, 70))
    s.outline()
    return s


# ---------- Đồ chiến đấu ----------

def bua_vang():
    s = I()
    s.rect(7, 1, 16, 22, (236, 200, 70))
    s.rect(7, 1, 8, 22, (250, 222, 110))
    s.rect(15, 1, 16, 22, (204, 166, 50))
    red = (190, 36, 36)
    s.rect(9, 4, 14, 4, red)
    s.rect(11, 4, 12, 18, red)
    for y in (7, 10, 13):
        s.rect(9, y, 14, y, red)
    s.rect(9, 16, 10, 19, red)
    s.rect(13, 16, 14, 19, red)
    s.outline()
    return s


def bottle(liquid):
    s = I()
    glass = (190, 220, 230)
    s.rect(10, 1, 13, 4, (130, 90, 56))  # nút bần
    s.rect(10, 1, 13, 1, (166, 120, 80))
    s.rect(9, 5, 14, 7, glass)
    s.blob(12, 15, 7, 7, glass, 1.1, 0.8, 3)
    for y in range(12, 22):
        for x in range(5, 20):
            if ((x - 12) / 6.4) ** 2 + ((y - 15) / 6.4) ** 2 <= 1:
                s.p(x, y, shade(liquid, 1.15 if y == 12 else 1.0 if x < 13 else 0.8))
    s.rect(7, 11, 8, 13, (240, 250, 255))  # ánh sáng thuỷ tinh
    s.outline()
    return s


# ---------- Nguyên liệu ----------

def gao_nep():
    s = I()
    s.blob(12, 15, 8, 7, (214, 190, 140), 1.12, 0.7, 4)  # bao vải
    s.rect(9, 6, 15, 9, (196, 170, 120))
    s.rect(8, 9, 16, 10, (150, 110, 70))  # dây buộc
    for x, y in ((10, 4), (12, 3), (14, 4), (11, 5), (13, 5)):
        s.p(x, y, (250, 248, 238))
    s.outline()
    return s


def muoi():
    s = I()
    s.blob(12, 16, 9, 5, (110, 130, 170), 1.15, 0.7, 3)  # bát
    s.blob(12, 12, 7, 3.5, (240, 244, 250), 1.05, 0.85, 3)
    for x, y in ((9, 11), (13, 10), (15, 12)):
        s.p(x, y, (255, 255, 255))
    s.outline()
    return s


def trau():
    s = I()
    for y in range(3, 21):  # lá hình tim
        t = (y - 3) / 18.0
        half = 8 * math.sin(math.pi * min(1, t * 1.1 + 0.12)) * (1 - t * 0.35)
        for x in range(int(12 - half), int(12 + half) + 1):
            c = (80, 150, 66) if x < 12 else (60, 120, 52)
            if y < 5 and abs(x - 12) < 2:
                continue  # khe tim
            s.p(x, y, c)
    s.line(12, 5, 12, 21, (150, 190, 110))
    for k in range(3):
        s.line(12, 9 + k * 4, 8, 7 + k * 4, (120, 180, 96))
        s.line(12, 9 + k * 4, 16, 7 + k * 4, (96, 150, 80))
    s.outline()
    return s


def cau():
    s = I()
    s.line(12, 2, 12, 8, (120, 100, 60))
    for cx, cy in ((8, 12), (16, 12), (12, 16), (12, 9)):
        s.blob(cx, cy, 3.5, 4, (226, 150, 52), 1.2, 0.72, 3)
    s.p(7, 10, (255, 220, 160))
    s.outline()
    return s


def ngai_cuu():
    s = I()
    s.line(12, 22, 12, 4, (110, 130, 90))
    for k, y in enumerate(range(5, 20, 3)):  # lá xẻ thuỳ
        d = 1 if k % 2 else -1
        for i in range(5):
            s.p(12 + d * (i + 1), y + i // 2, (150, 176, 140) if i % 2 else (176, 200, 166))
            s.p(12 + d * (i + 1), y + i // 2 + 1, (120, 146, 112))
    s.outline()
    return s


def hoa_hue():
    s = I()
    s.line(12, 22, 12, 6, (70, 130, 60))
    s.line(12, 16, 8, 12, (80, 150, 66))
    for cx, cy in ((12, 4), (10, 7), (14, 7), (12, 10)):
        s.blob(cx, cy, 2, 2, (248, 248, 240), 1.0, 0.8, 2)
    s.p(12, 4, (240, 220, 140))
    s.outline()
    return s


ITEMS = [
    ("chuong_ba_noi", "Chuông nhỏ bà nội", chuong_ba_noi), ("dieu_hai_lam", "Con diều Hải làm", dieu_hai_lam),
    ("luu_but_nhom", "Lưu bút nhóm", luu_but_nhom), ("luu_but", "Lưu bút", luu_but), ("bi_ve", "Viên bi ve", bi_ve),
    ("la_ban_tu_che", "La bàn tự chế", la_ban_tu_che), ("anh_nhom_7", "Ảnh nhóm 7 người", anh_nhom_7),
    ("met_gao_muoi", "Mẹt gạo muối", met_gao_muoi), ("bo_nhang", "Bó nhang", bo_nhang),
    ("met_trau_cau", "Mẹt trầu cau", met_trau_cau), ("bo_hoa_hue", "Bó hoa huệ", bo_hoa_hue),
    ("bua_vang", "Bùa vàng", bua_vang), ("thuoc_hoi_hp", "Thuốc hồi HP", lambda: bottle((214, 52, 60))),
    ("thuoc_giam_am_khi", "Thuốc giảm Âm khí", lambda: bottle((70, 200, 170))),
    ("gao_nep", "Gạo nếp", gao_nep), ("muoi", "Muối", muoi), ("trau", "Trầu", trau), ("cau", "Cau", cau),
    ("ngai_cuu", "Ngải cứu", ngai_cuu), ("hoa_hue", "Hoa huệ", hoa_hue),
]


def main():
    imgs = []
    for key, label, fn in ITEMS:
        im = fn().img
        im.save(os.path.join(OUT, key + ".png"))
        imgs.append((label, im))
    sc, cw, cols = 5, 24 * 5 + 40, 7
    rows = (len(imgs) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * cw + 20, rows * (24 * sc + 50) + 20), (30, 30, 40, 255))
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 14)
    except OSError:
        font = ImageFont.load_default()
    for i, (label, im) in enumerate(imgs):
        x, y = 10 + (i % cols) * cw, 10 + (i // cols) * (24 * sc + 50)
        sheet.alpha_composite(im.resize((24 * sc, 24 * sc), Image.NEAREST), (x + 20, y))
        tw = d.textlength(label, font=font)
        d.text((x + (cw - tw) / 2, y + 24 * sc + 8), label, fill=(240, 230, 210), font=font)
    sheet.save(os.path.join(PREVIEW, "_items_preview.png"))


if __name__ == "__main__":
    main()
    print("done →", OUT)
