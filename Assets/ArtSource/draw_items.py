"""Icon 16x16 cho kỷ vật, đồ lễ và đồ chiến đấu. Chạy: python3 draw_items.py"""
from PIL import Image, ImageDraw, ImageFont
import os

N = 16
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "sprites", "items")
os.makedirs(OUT, exist_ok=True)
OUTLINE = (30, 22, 26, 255)


def shade(c, f):
    return (max(0, min(255, int(c[0] * f))), max(0, min(255, int(c[1] * f))), max(0, min(255, int(c[2] * f))), 255)


class I:
    def __init__(self):
        self.img = Image.new("RGBA", (N, N), (0, 0, 0, 0))
        self.px = self.img.load()

    def p(self, x, y, c):
        if 0 <= x < N and 0 <= y < N:
            self.px[x, y] = c

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.p(x, y, c)

    def ellipse(self, cx, cy, rx, ry, c):
        for y in range(N):
            for x in range(N):
                if ((x - cx) / (rx + 0.5)) ** 2 + ((y - cy) / (ry + 0.5)) ** 2 <= 1:
                    self.p(x, y, c)

    def line(self, pts, c):
        ImageDraw.Draw(self.img).line(pts, fill=c, width=1)

    def outline(self):
        src = self.img.copy().load()
        for y in range(N):
            for x in range(N):
                if src[x, y][3] == 0:
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < N and 0 <= ny < N and src[nx, ny][3] > 0 and src[nx, ny] != OUTLINE:
                            self.px[x, y] = OUTLINE
                            break

    def save(self, name):
        self.outline()
        self.img.save(os.path.join(OUT, name + ".png"))
        return self.img


# ---------- Kỷ vật ----------

def chuong():
    s = I()
    brass, red = (214, 168, 64, 255), (196, 44, 44, 255)
    s.rect(7, 1, 8, 3, red)                       # dây đỏ
    s.rows = None
    for y, (a, b) in enumerate([(6, 9), (5, 10), (5, 10), (4, 11), (4, 11), (4, 11), (3, 12), (2, 13)]):
        s.rect(a, 4 + y, b, 4 + y, brass)
    s.rect(2, 12, 13, 12, shade(brass, 0.8))      # vành chuông
    s.rect(9, 5, 11, 11, shade(brass, 0.8))       # bóng phải
    s.p(5, 6, shade(brass, 1.3)); s.p(5, 7, shade(brass, 1.3))
    s.rect(7, 13, 8, 14, (120, 92, 40, 255))      # quả lắc
    return s.save("chuong_ba_noi")


def dieu():
    s = I()
    paper, bamboo, tail = (236, 176, 60, 255), (150, 110, 60, 255), (200, 50, 50, 255)
    for y in range(0, 13):                         # thân diều hình thoi
        half = y if y <= 6 else 12 - y
        s.rect(7 - half, y, 8 + half, y, paper)
    s.rect(2, 6, 13, 6, (220, 90, 60, 255))        # sọc ngang
    s.line([(7, 0), (7, 12)], bamboo); s.line([(1, 6), (14, 6)], bamboo)
    s.rect(9, 1, 13, 5, shade(paper, 0.85)) if False else None
    for x, y in ((8, 13), (9, 14), (10, 15), (11, 14), (12, 15)):  # đuôi
        s.p(x, y, tail)
    return s.save("dieu_hai_lam")


def luu_but_nhom():
    s = I()
    cover, page, ink = (120, 70, 50, 255), (240, 230, 206, 255), (110, 100, 130, 255)
    s.rect(0, 4, 15, 13, cover)                   # bìa mở
    s.rect(1, 3, 7, 12, page); s.rect(8, 3, 14, 12, shade(page, 0.92))
    s.line([(7, 3), (7, 12)], shade(page, 0.7))   # gáy giữa
    for y in (5, 7, 9):
        s.line([(2, y), (6, y)], ink)
        s.line([(9, y), (13, y)], ink)
    s.p(11, 10, (200, 60, 70, 255))               # trái tim nhỏ ai đó vẽ
    return s.save("luu_but_nhom")


def luu_but():
    s = I()
    cover, pages, strap = (70, 96, 150, 255), (236, 228, 204, 255), (180, 140, 60, 255)
    s.rect(3, 1, 12, 14, cover)
    s.rect(12, 2, 13, 13, pages)                  # mép giấy
    s.rect(3, 1, 4, 14, shade(cover, 0.7))        # gáy
    s.rect(6, 4, 10, 6, (226, 214, 180, 255))     # nhãn
    s.rect(3, 9, 13, 10, strap)                   # dây cài
    s.p(13, 9, shade(strap, 1.2))
    return s.save("luu_but")


def bi_ve():
    s = I()
    glass, swirl = (90, 170, 120, 255), (200, 80, 60, 255)
    s.ellipse(7, 8, 5, 5, glass)
    s.line([(4, 9), (6, 7), (9, 9), (11, 7)], swirl)  # vân màu trong bi
    s.ellipse(10, 10, 2, 2, shade(glass, 0.75))
    s.p(5, 5, (236, 250, 240, 255)); s.p(6, 5, (236, 250, 240, 255)); s.p(5, 6, (236, 250, 240, 255))
    return s.save("bi_ve")


def la_ban():
    s = I()
    rim, face = (150, 120, 80, 255), (236, 226, 196, 255)
    s.ellipse(7, 8, 6, 6, rim)
    s.ellipse(7, 8, 4, 4, face)
    s.rect(7, 1, 8, 2, rim)                       # khuyên đeo
    s.line([(7, 5), (7, 8)], (200, 40, 40, 255))  # kim đỏ chỉ bắc
    s.line([(7, 9), (7, 11)], (60, 60, 70, 255))
    s.p(7, 8, (40, 40, 40, 255))
    s.p(4, 8, shade(face, 0.8)); s.p(10, 8, shade(face, 0.8))
    s.rect(11, 11, 12, 12, (180, 160, 120, 255))  # vết băng dính (tự chế)
    return s.save("la_ban_tu_che")


def anh_nhom():
    s = I()
    frame, sky = (190, 170, 130, 255), (150, 180, 200, 255)
    s.rect(0, 2, 15, 13, frame)
    s.rect(1, 3, 14, 12, sky)
    s.rect(1, 10, 14, 12, (110, 140, 90, 255))    # bãi cỏ
    heads = [(2, 8), (4, 7), (6, 8), (8, 7), (10, 8), (12, 7), (13, 9)]
    for i, (x, y) in enumerate(heads):
        s.p(x, y, (40, 34, 36, 255))
        s.p(x, y + 1, (232, 196, 160, 255))
        s.p(x, y + 2, [(60, 70, 120, 255), (230, 180, 60, 255), (70, 120, 80, 255), (230, 230, 236, 255),
                       (140, 128, 80, 255), (70, 56, 54, 255), (226, 232, 236, 255)][i])
    s.rect(13, 3, 14, 6, (90, 80, 100, 255))      # một góc ảnh bị gạch mờ
    return s.save("anh_nhom_7")


# ---------- Đồ lễ ----------

def met(s, fill_fn):
    tray, rim = (186, 146, 86, 255), (140, 100, 54, 255)
    s.ellipse(7, 11, 7, 3, rim)
    s.ellipse(7, 10, 7, 3, tray)
    for x in range(2, 14, 3):
        s.p(x, 10, shade(tray, 0.85))
    fill_fn(s)


def met_gao_muoi():
    s = I()
    def f(s):
        s.ellipse(5, 8, 3, 2, (244, 240, 230, 255))       # gạo
        s.ellipse(10, 8, 3, 2, (228, 232, 240, 255))      # muối
        for x, y in ((4, 7), (6, 8), (10, 7), (11, 8)):
            s.p(x, y, (210, 204, 190, 255))
    met(s, f)
    return s.save("met_gao_muoi")


def bo_nhang():
    s = I()
    stick, handle, ember = (150, 90, 60, 255), (196, 40, 50, 255), (255, 150, 60, 255)
    for i, x in enumerate((5, 7, 9, 11)):
        top = 2 + (i % 2)
        s.line([(x, top), (x - 1, 10)], stick)
        s.p(x, top, ember)
    s.rect(3, 10, 10, 14, handle)                 # chân nhang đỏ bó lại
    s.rect(3, 11, 10, 11, (230, 200, 90, 255))    # dây buộc
    s.p(6, 0, (180, 180, 190, 255)); s.p(10, 1, (180, 180, 190, 255))  # khói
    return s.save("bo_nhang")


def met_trau_cau():
    s = I()
    def f(s):
        leaf = (70, 140, 60, 255)
        s.ellipse(5, 8, 3, 2, leaf); s.ellipse(8, 7, 3, 2, shade(leaf, 0.85))
        s.line([(3, 8), (7, 8)], shade(leaf, 1.3))
        s.ellipse(11, 8, 2, 2, (196, 140, 60, 255))       # quả cau
        s.p(10, 7, (230, 190, 100, 255))
    met(s, f)
    return s.save("met_trau_cau")


def hoa_hue():
    s = I()
    stem, white = (70, 130, 60, 255), (246, 244, 236, 255)
    for x, top in ((5, 4), (8, 2), (11, 5)):
        s.line([(x, top + 2), (7, 14)], stem)
        s.rect(x - 1, top, x + 1, top + 1, white)
        s.p(x, top - 1, white)
        s.p(x + 1, top + 1, (220, 220, 200, 255))
    s.rect(6, 11, 8, 12, (230, 70, 80, 255))      # dây buộc
    return s.save("bo_hoa_hue")


# ---------- Đồ chiến đấu ----------

def bua_vang():
    s = I()
    paper, ink = (240, 204, 70, 255), (200, 36, 36, 255)
    s.rect(4, 0, 11, 15, paper)
    s.rect(10, 1, 11, 14, shade(paper, 0.85))
    s.rect(5, 2, 9, 2, ink)                       # nét bùa
    s.line([(7, 3), (7, 12)], ink)
    s.line([(5, 5), (9, 5)], ink)
    s.line([(5, 8), (9, 7)], ink)
    s.rect(6, 10, 8, 11, ink)
    s.rect(5, 13, 9, 13, ink)
    return s.save("bua_vang")


def chai(name, liquid):
    s = I()
    glass, cork = (200, 220, 230, 255), (150, 100, 60, 255)
    s.rect(6, 0, 9, 2, cork)
    s.rect(6, 3, 9, 4, glass)                     # cổ chai
    s.ellipse(7, 10, 5, 5, glass)
    s.ellipse(7, 11, 4, 3, liquid)
    s.rect(3, 9, 12, 9, shade(liquid, 1.2))       # mặt nước
    s.ellipse(9, 12, 2, 1, shade(liquid, 0.75))
    s.p(4, 7, (250, 250, 255, 255)); s.p(4, 8, (250, 250, 255, 255))
    return s.save(name)


ITEMS = [
    ("Chuông nhỏ bà nội", chuong), ("Con diều Hải làm", dieu), ("Lưu bút nhóm", luu_but_nhom),
    ("Lưu bút", luu_but), ("Viên bi ve", bi_ve), ("La bàn tự chế", la_ban), ("Ảnh nhóm 7 người", anh_nhom),
    ("Mẹt gạo muối", met_gao_muoi), ("Bó nhang", bo_nhang), ("Mẹt trầu cau", met_trau_cau), ("Bó hoa huệ", hoa_hue),
    ("Bùa vàng", bua_vang), ("Thuốc hồi HP", lambda: chai("thuoc_hoi_hp", (210, 50, 60, 255))),
    ("Thuốc giảm Âm khí", lambda: chai("thuoc_giam_am_khi", (80, 200, 170, 255))),
]

if __name__ == "__main__":
    scale, cell, cols = 8, 190, 7
    rows = (len(ITEMS) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * cell + 20, rows * (N * scale + 70) + 20), (30, 30, 40, 255))
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
    except OSError:
        font = ImageFont.load_default()
    for i, (label, fn) in enumerate(ITEMS):
        im = fn()
        x = 10 + (i % cols) * cell
        y = 10 + (i // cols) * (N * scale + 70)
        sheet.alpha_composite(im.resize((N * scale, N * scale), Image.NEAREST), (x + (cell - N * scale) // 2, y))
        tw = d.textlength(label, font=font)
        d.text((x + (cell - tw) / 2, y + N * scale + 12), label, fill=(240, 230, 210), font=font)
    sheet.save(os.path.join(ROOT, "sprites", "_items_preview.png"))
    print("done")
