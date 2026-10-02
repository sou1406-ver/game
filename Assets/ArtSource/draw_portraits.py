"""Chân dung hội thoại 48x48. Chạy: python3 draw_portraits.py"""
from PIL import Image, ImageDraw, ImageFont
import os

N = 48
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "sprites", "portraits")
os.makedirs(OUT, exist_ok=True)
OUTLINE = (30, 20, 26, 255)
SKIN = (238, 196, 158, 255)
EYE = (36, 26, 30, 255)
WHITE = (246, 240, 236, 255)


def shade(c, f):
    return (max(0, min(255, int(c[0] * f))), max(0, min(255, int(c[1] * f))), max(0, min(255, int(c[2] * f))), 255)


class P:
    def __init__(self, skin=SKIN):
        self.img = Image.new("RGBA", (N, N), (0, 0, 0, 0))
        self.px = self.img.load()
        self.skin = skin
        self.skin_sh = shade(skin, 0.84)

    def p(self, x, y, c):
        if 0 <= x < N and 0 <= y < N:
            self.px[x, y] = c

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.p(x, y, c)

    def span(self, y, x0, x1, c):
        self.rect(x0, y, x1, y, c)

    def ellipse(self, cx, cy, rx, ry, c):
        for y in range(N):
            for x in range(N):
                if ((x - cx) / (rx + 0.5)) ** 2 + ((y - cy) / (ry + 0.5)) ** 2 <= 1:
                    self.p(x, y, c)

    def line(self, pts, c, w=1):
        ImageDraw.Draw(self.img).line(pts, fill=c, width=w)

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

    # ---- phần chung ----
    def shoulders(self, cloth, wide=0):
        for i, y in enumerate(range(38, 48)):
            half = min(17 + wide, 10 + i * 3 + wide)
            self.span(y, 24 - half, 23 + half, cloth)
        for y in range(38, 48):                       # bóng nửa phải
            for x in range(30, 48):
                if self.px[x, y][:3] == cloth[:3]:
                    self.px[x, y] = shade(cloth, 0.8)

    def head(self, jaw=0):
        s, sh = self.skin, self.skin_sh
        self.rect(20, 31, 27, 39, sh)                 # cổ
        rows = {}
        for y in range(9, 36):
            if y <= 24:
                half = 11
                if y < 13:
                    half = [7, 9, 10, 11][y - 9]
            else:
                half = max(4, 11 - (y - 24) * 2 // 3 - jaw)
            rows[y] = half
            self.span(y, 24 - half, 23 + half, s)
        for y, half in rows.items():                  # má phải tối
            self.span(y, 23 + half - 3, 23 + half, sh)
        self.rect(11, 20, 12, 25, s); self.rect(35, 20, 36, 25, sh)   # tai
        self.p(12, 22, sh)

    def eyes(self, y=21, color=EYE, look=0, tired=False, closed=False):
        for x0 in (16, 27):
            if closed:
                self.span(y + 1, x0, x0 + 3, color)
                continue
            self.rect(x0, y, x0 + 3, y + 2, WHITE)
            self.rect(x0 + 1 + look, y, x0 + 2 + look, y + 2, color)
            self.p(x0 + 1 + look, y, (250, 250, 255, 255))   # ánh mắt
            self.span(y - 1, x0, x0 + 3, OUTLINE)            # mí trên
            if tired:
                self.span(y + 3, x0, x0 + 3, (190, 140, 140, 255))

    def brows(self, hair, y=18, angry=False, sad=False):
        for x0, side in ((16, 0), (27, 1)):
            self.span(y, x0, x0 + 3, hair)
            if angry:
                self.p(x0 + (3 if side == 0 else 0), y + 1, hair)
            if sad:
                self.p(x0 + (0 if side == 0 else 3), y + 1, hair)

    def nose_mouth(self, mouth="flat", y=30):
        self.p(24, 26, self.skin_sh); self.p(24, 27, self.skin_sh); self.p(23, 27, shade(self.skin, 0.92))
        lip = shade(self.skin_sh, 0.75)
        if mouth == "flat":
            self.span(y, 22, 25, lip)
        elif mouth == "smile":
            self.span(y, 22, 25, lip); self.p(21, y - 1, lip); self.p(26, y - 1, lip)
        elif mouth == "smirk":
            self.span(y, 22, 25, lip); self.p(26, y - 1, lip)
        elif mouth == "open":
            self.rect(22, y - 1, 25, y + 1, (90, 30, 36, 255))
        elif mouth == "frown":
            self.span(y, 22, 25, lip); self.p(21, y + 1, lip); self.p(26, y + 1, lip)

    def blush(self):
        for x in (15, 16, 31, 32):
            self.p(x, 26, (228, 150, 130, 255))

    def save(self, name):
        self.outline()
        self.img.save(os.path.join(OUT, name + ".png"))
        return self.img


def hair_cap(s, c, top=6, side_to=22, fringe=None):
    """tóc trùm đầu: chỏm + hai bên; fringe: list (x0,x1,y_bottom) các mảng mái"""
    for y in range(N):                                 # chỏm tóc: chỉ phủ tới trán (y <= 13)
        for x in range(N):
            if ((x - 24) / 13.5) ** 2 + ((y - 15) / 10.5) ** 2 <= 1 and (y <= 13 or x <= 13 or x >= 34):
                s.p(x, y, c)
    s.rect(11, 14, 13, side_to, c); s.rect(34, 14, 36, side_to, c)
    for x0, x1, yb in (fringe or []):
        s.rect(x0, 12, x1, yb, c)


def shine(s, c, pts):
    for x, y in pts:
        s.p(x, y, shade(c, 2.0))


# ---------- nhân vật ----------

def minh():
    s = P()
    jacket, tee = (44, 62, 112, 255), (232, 232, 236, 255)
    s.shoulders(jacket)
    s.rect(19, 39, 28, 47, tee)
    s.head()
    s.eyes(look=-1); s.nose_mouth("flat")
    hair = (28, 26, 34, 255)
    hair_cap(s, hair, fringe=[(14, 18, 18), (19, 22, 16), (26, 30, 17)])
    for x, y in ((14, 4), (20, 3), (27, 4), (33, 6), (17, 5)):   # tóc rối dựng
        s.rect(x, y, x + 1, y + 3, hair)
    s.brows(hair, sad=True)
    shine(s, hair, [(18, 8), (19, 8), (20, 9)])
    return s.save("minh")


def vy():
    s = P()
    coat = (232, 182, 52, 255)
    s.shoulders(coat)
    s.rect(23, 39, 24, 47, shade(coat, 0.8))            # khóa áo
    s.head(jaw=1)
    s.eyes(); s.nose_mouth("smile"); s.blush()
    hair = (78, 46, 34, 255)
    hair_cap(s, hair, side_to=33, fringe=[(13, 34, 16)])  # tóc bob mái bằng
    s.rect(10, 18, 12, 33, hair); s.rect(35, 18, 37, 33, hair)
    s.rect(37, 12, 40, 22, hair)                          # đuôi tóc nhỏ
    s.rect(36, 11, 37, 12, (220, 70, 60, 255))
    s.brows(shade(hair, 0.8))
    shine(s, hair, [(17, 8), (18, 8), (19, 8), (16, 9)])
    return s.save("vy")


def lan():
    s = P()
    ao = (62, 120, 84, 255)
    s.shoulders(ao)
    s.span(38, 19, 28, shade(ao, 1.2))                   # cổ áo bà ba
    s.head(jaw=1)
    s.eyes(); s.nose_mouth("flat"); s.blush()
    hair = (24, 22, 28, 255)
    hair_cap(s, hair, side_to=26, fringe=[(13, 22, 15), (26, 34, 15)])
    s.rect(32, 26, 35, 46, hair)                          # bím tóc vắt trước vai
    for y in range(28, 46, 3):
        s.span(y, 32, 35, shade(hair, 1.6))
    s.rect(32, 44, 35, 45, (200, 60, 60, 255))
    s.brows(hair)
    hat = (226, 206, 150, 255)                            # nón lá đội lệch ra sau
    for i, y in enumerate(range(0, 10)):
        half = 2 + i * 2 + (i // 2)
        s.span(y, 24 - half, 23 + half, hat)
    for y in range(0, 10, 2):
        s.span(y, 24 - (2 + y * 2), 23 + (2 + y * 2), shade(hat, 0.9))
    s.span(9, 2, 45, shade(hat, 0.82))
    return s.save("lan")


def tuan():
    s = P()
    shirt, tie = (236, 236, 242, 255), (150, 34, 44, 255)
    s.shoulders(shirt)
    s.rect(22, 39, 25, 47, tie); s.rect(23, 38, 24, 38, tie)
    s.p(21, 39, tie)                                       # cà vạt nới lệch
    s.head(jaw=0)
    s.eyes(look=1); s.nose_mouth("smirk")
    hair = (40, 30, 26, 255)
    hair_cap(s, hair, side_to=19)
    s.rect(13, 12, 20, 15, hair)                          # tóc vuốt rẽ ngôi lệch
    s.rect(21, 11, 34, 13, hair)
    s.brows(hair, angry=True)
    shine(s, hair, [(17, 8), (18, 8), (19, 8), (20, 8), (21, 9)])
    return s.save("tuan")


def khoa():
    s = P()
    shirt, strap = (138, 128, 82, 255), (60, 50, 40, 255)
    s.shoulders(shirt, wide=2)
    s.rect(13, 40, 14, 47, strap); s.rect(33, 40, 34, 47, strap)
    s.head(jaw=-1)
    s.eyes(); s.nose_mouth("smile")
    frame = (20, 20, 24, 255)                            # kính gọng đen
    for x0 in (15, 26):
        s.rect(x0, 19, x0 + 5, 24, frame)
        s.rect(x0 + 1, 20, x0 + 4, 23, (176, 206, 224, 255))
        s.rect(x0 + 2, 21, x0 + 3, 22, EYE)
        s.p(x0 + 1, 20, WHITE)
    s.span(21, 21, 25, frame)
    hair = (30, 28, 30, 255)
    hair_cap(s, hair, side_to=19, fringe=[(13, 34, 14)])
    s.brows(hair, y=17)
    shine(s, hair, [(18, 8), (19, 8)])
    return s.save("khoa")


def phong():
    s = P()
    shirt = (58, 46, 44, 255)
    s.shoulders(shirt)
    s.span(38, 18, 29, shade(shirt, 1.3))
    s.head()
    s.eyes(tired=True, look=-1); s.nose_mouth("flat")
    corrupt = (100, 54, 126, 255)                         # vệt tha hóa lan từ cổ lên má phải
    for x, y in ((29, 38), (30, 36), (31, 35), (31, 33), (32, 31), (33, 29), (33, 27), (34, 26), (28, 39), (30, 34)):
        s.p(x, y, corrupt)
    s.p(32, 30, shade(corrupt, 1.4)); s.p(31, 34, shade(corrupt, 1.4))
    hair = (22, 20, 26, 255)
    hair_cap(s, hair, side_to=22, fringe=[(14, 20, 16)])
    s.rect(24, 12, 35, 24, hair)                          # mái dài che mắt phải
    s.rect(26, 25, 29, 26, hair); s.p(33, 25, hair)
    s.span(18, 16, 19, hair)
    shine(s, hair, [(18, 8), (19, 8)])
    beads = (150, 96, 48, 255)                            # chuỗi hạt quấn cổ
    for x in range(17, 31, 2):
        s.p(x, 40 + (1 if 20 < x < 28 else 0), beads)
    return s.save("phong")


def hai():
    s = P(skin=(204, 206, 196, 255))
    shirt = (226, 232, 236, 255)
    s.shoulders(shirt)
    s.span(38, 18, 29, (250, 250, 252, 255))
    s.p(15, 42, (200, 40, 40, 255)); s.rect(30, 41, 33, 41, (60, 90, 160, 255))   # phù hiệu, tên trường
    s.head(jaw=1)
    for x0 in (16, 27):                                   # mắt đen đặc, không tròng trắng
        s.rect(x0, 20, x0 + 3, 23, (14, 14, 20, 255))
    s.nose_mouth("flat")
    hair = (24, 28, 34, 255)
    hair_cap(s, hair, side_to=30)
    for i, x in enumerate(range(14, 34, 2)):              # mái bết thành sợi dài ngắn
        s.rect(x, 12, x, 16 + (i * 3) % 6, hair)
    s.rect(11, 22, 12, 32, hair); s.rect(35, 22, 36, 32, hair)
    water = (120, 180, 210, 255)
    for x, y in ((14, 30), (33, 28), (20, 35), (13, 34)):
        s.p(x, y, water)
    shine(s, hair, [(18, 8), (20, 8)])
    return s.save("hai")


def hai_tha_hoa():
    s = P(skin=(150, 160, 170, 255))
    shirt = (120, 130, 140, 255)
    s.shoulders(shirt)
    s.head(jaw=2)
    for x0 in (16, 27):                                   # hốc mắt sâu, đồng tử đỏ
        s.rect(x0 - 1, 19, x0 + 4, 24, (10, 8, 14, 255))
        s.p(x0 + 2, 21, (240, 40, 40, 255))
    s.rect(20, 28, 27, 32, (20, 6, 12, 255))              # miệng há rộng
    for x in (21, 23, 25, 27):
        s.p(x, 28, (220, 214, 200, 255))
    vein = (70, 40, 110, 255)
    for x, y in ((14, 26), (15, 28), (16, 30), (33, 25), (32, 27), (31, 29), (30, 31)):
        s.p(x, y, vein)
    hair = (12, 14, 20, 255)
    hair_cap(s, hair, side_to=40)
    s.rect(9, 18, 12, 44, hair); s.rect(35, 18, 38, 44, hair)
    for i, x in enumerate(range(13, 35, 2)):
        s.rect(x, 12, x, 17 + (i * 5) % 7, hair)
    for x, y in ((10, 46), (37, 45), (12, 47)):
        s.p(x, y, (120, 180, 210, 255))
    return s.save("hai_tha_hoa")


def ong_cu():
    s = P(skin=(222, 182, 146, 255))
    jacket = (70, 60, 56, 255)
    s.shoulders(jacket)
    s.span(38, 18, 29, shade(jacket, 1.3))
    s.head(jaw=0)
    s.eyes(y=22, closed=False)
    for x0 in (16, 27):                                   # nếp nhăn đuôi mắt, bọng mắt
        s.span(25, x0, x0 + 3, s.skin_sh)
    s.p(15, 22, s.skin_sh); s.p(32, 22, s.skin_sh)
    s.nose_mouth("frown", y=31)
    s.span(28, 18, 20, s.skin_sh); s.span(28, 27, 29, s.skin_sh)   # nếp má
    hair = (196, 196, 200, 255)                           # tóc bạc thưa, trán hói
    s.rect(11, 12, 14, 24, hair); s.rect(33, 12, 36, 24, hair)
    s.span(9, 18, 29, hair); s.span(10, 15, 17, hair); s.span(10, 30, 32, hair)
    s.brows((220, 220, 224, 255), y=19, sad=True)
    s.rect(21, 32, 26, 34, (210, 210, 214, 255))          # râu cằm
    s.rect(22, 35, 25, 36, (210, 210, 214, 255))
    return s.save("ong_cu")


ALL = [("Minh", minh), ("Vy", vy), ("Lan", lan), ("Tuấn", tuan), ("Khoa", khoa), ("Phong", phong),
       ("Hải", hai), ("Hải (tha hóa)", hai_tha_hoa), ("Ông cụ", ong_cu)]

if __name__ == "__main__":
    scale, cell, cols = 5, 260, 5
    rows = (len(ALL) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * cell + 20, rows * (N * scale + 60) + 20), (30, 30, 40, 255))
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
    for i, (label, fn) in enumerate(ALL):
        im = fn()
        x = 10 + (i % cols) * cell + (cell - N * scale) // 2
        y = 10 + (i // cols) * (N * scale + 60)
        frame = Image.new("RGBA", (N * scale, N * scale), (52, 50, 66, 255))
        frame.alpha_composite(im.resize((N * scale, N * scale), Image.NEAREST))
        sheet.alpha_composite(frame, (x, y))
        tw = d.textlength(label, font=font)
        d.text((x + (N * scale - tw) / 2, y + N * scale + 12), label, fill=(240, 230, 210), font=font)
    sheet.save(os.path.join(ROOT, "sprites", "_portraits_preview.png"))
    print("done")
