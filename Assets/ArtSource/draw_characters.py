"""Sprite pixel 32x48 cho 5 nhân vật chính. Chạy: python3 draw_characters.py"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 32, 48
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sprites")
os.makedirs(OUT, exist_ok=True)

OUTLINE = (34, 24, 30, 255)
SKIN = (238, 196, 158, 255)
SKIN_SH = (206, 150, 116, 255)
EYE = (40, 28, 30, 255)
BLUSH = (226, 140, 120, 255)


def shade(c, f):
    return (max(0, int(c[0] * f)), max(0, int(c[1] * f)), max(0, int(c[2] * f)), 255)


class S:
    def __init__(self):
        self.img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        self.px = self.img.load()

    def p(self, x, y, c):
        if 0 <= x < W and 0 <= y < H:
            self.px[x, y] = c

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.p(x, y, c)

    def rows(self, y0, spans, c):
        """spans: list of (x0, x1) per row starting at y0"""
        for i, (a, b) in enumerate(spans):
            for x in range(a, b + 1):
                self.p(x, y0 + i, c)

    def outline(self):
        src = self.img.copy().load()
        for y in range(H):
            for x in range(W):
                if src[x, y][3] == 0:
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < W and 0 <= ny < H and src[nx, ny][3] > 0 and src[nx, ny] != OUTLINE:
                            self.px[x, y] = OUTLINE
                            break

    def shadow_right(self, colors, x_from):
        """làm tối nửa phải cho các màu trong `colors` (ánh sáng từ trái)"""
        for y in range(H):
            for x in range(x_from, W):
                c = self.px[x, y]
                if c[3] and c[:3] in colors:
                    self.px[x, y] = shade(c, 0.78)


# ---------- phần thân dùng chung ----------

def face(s, y_eye=14):
    # đầu: x 10..21, y 7..19
    s.rows(7, [(12, 19), (11, 20), (10, 21), (10, 21), (10, 21), (10, 21), (10, 21),
               (10, 21), (10, 21), (10, 21), (11, 20), (12, 19), (13, 18)], SKIN)
    s.rect(19, 9, 21, 17, SKIN_SH)  # má phải tối
    s.rect(12, y_eye, 13, y_eye + 1, EYE)
    s.rect(17, y_eye, 18, y_eye + 1, EYE)
    s.p(12, y_eye + 3, BLUSH)
    s.p(19, y_eye + 3, BLUSH)
    s.rect(15, y_eye + 4, 16, y_eye + 4, shade(SKIN_SH, 0.9))  # miệng
    s.rect(14, 20, 17, 21, SKIN_SH)  # cổ


def body(s, shirt, pants, shoes, wide=0, sleeve=None, hands=True):
    sleeve = sleeve or shirt
    x0, x1 = 10 - wide, 21 + wide
    s.rect(x0 + 1, 22, x1 - 1, 22, shirt)         # vai bo tròn
    s.rect(x0, 23, x1, 33, shirt)                 # thân áo
    s.rect(x0 - 3, 23, x0 - 2, 31, sleeve)        # tay trái (cách thân 1px để có viền)
    s.rect(x1 + 2, 23, x1 + 3, 31, sleeve)        # tay phải
    if hands:
        s.rect(x0 - 3, 32, x0 - 2, 33, SKIN)
        s.rect(x1 + 2, 32, x1 + 3, 33, SKIN_SH)
    s.rect(11 - wide, 34, 14, 43, pants)          # chân trái
    s.rect(17, 34, 20 + wide, 43, pants)          # chân phải (khe giữa 2 chân)
    s.rect(15, 34, 16, 35, pants)                 # đũng quần
    s.rect(10 - wide, 44, 14, 45, shoes)
    s.rect(17, 44, 21 + wide, 45, shoes)


def hair_shine(s, hair, pts):
    for x, y in pts:
        s.p(x, y, shade(hair, 2.2))


def finish(s, name, darken):
    s.shadow_right(darken, 17)
    s.outline()
    s.img.save(os.path.join(OUT, name + ".png"))
    return s.img


# ---------- 5 nhân vật ----------

def minh():
    s = S()
    jacket = (44, 62, 112, 255)
    tee = (232, 232, 236, 255)
    jeans = (52, 56, 72, 255)
    body(s, jacket, jeans, (30, 30, 36, 255))
    s.rect(14, 22, 17, 33, tee)                   # áo thun trong áo khoác mở
    s.rect(7, 31, 8, 31, (200, 40, 40, 255))      # chỉ đỏ ở cổ tay (bùa)
    face(s)
    hair = (28, 26, 34, 255)
    s.rows(4, [(13, 14), (11, 19), (10, 21), (9, 22), (9, 22), (9, 22)], hair)   # tóc rối
    s.p(17, 3, hair); s.p(20, 4, hair); s.p(10, 5, hair)
    s.rect(9, 10, 10, 15, hair); s.rect(21, 10, 22, 13, hair)                    # tóc mai
    s.rect(11, 10, 13, 11, hair); s.rect(16, 10, 18, 10, hair)                   # tóc mái lệch
    hair_shine(s, hair, [(12, 5), (13, 5), (11, 6)])
    return finish(s, "minh", [jacket[:3], jeans[:3], tee[:3]])


def vy():
    s = S()
    coat = (232, 182, 52, 255)
    legs = (48, 44, 58, 255)
    body(s, coat, legs, (236, 236, 236, 255))
    s.rect(9, 34, 22, 36, coat)                   # áo mưa dài qua hông
    s.rect(15, 22, 16, 36, shade(coat, 0.85))     # khóa áo
    face(s)
    hair = (78, 46, 34, 255)
    s.rows(5, [(12, 19), (10, 21), (9, 22), (9, 22)], hair)
    s.rect(9, 9, 10, 18, hair); s.rect(21, 9, 22, 18, hair)                      # tóc bob
    s.rect(11, 9, 20, 11, hair)                                                   # mái bằng
    s.rect(23, 9, 24, 14, hair)                                                   # đuôi tóc nhỏ
    s.p(22, 8, (220, 70, 60, 255)); s.p(23, 8, (220, 70, 60, 255))               # dây buộc tóc
    hair_shine(s, hair, [(12, 6), (13, 6), (11, 7)])
    return finish(s, "vy", [coat[:3], legs[:3]])


def lan():
    s = S()
    ao = (62, 120, 84, 255)
    quan = (32, 32, 38, 255)
    body(s, ao, quan, (96, 64, 44, 255))
    s.rect(10, 32, 21, 35, ao)                    # vạt áo bà ba
    s.rect(15, 22, 16, 29, shade(ao, 0.85))
    s.rect(10, 36, 14, 43, quan); s.rect(17, 36, 21, 43, quan)  # quần ống rộng
    s.rect(10, 44, 14, 45, (96, 64, 44, 255)); s.rect(17, 44, 21, 45, (96, 64, 44, 255))
    face(s, y_eye=14)
    hair = (24, 22, 28, 255)
    s.rect(10, 9, 21, 11, hair)
    s.rect(9, 10, 10, 16, hair); s.rect(21, 10, 22, 16, hair)
    s.rect(19, 18, 20, 30, hair)                  # bím tóc dài vắt trước vai
    s.p(19, 31, (200, 60, 60, 255)); s.p(20, 31, (200, 60, 60, 255))
    hat = (226, 206, 150, 255)                    # nón lá
    s.rows(1, [(15, 16), (14, 17), (13, 18), (12, 19), (11, 20), (9, 22), (7, 24), (5, 26)], hat)
    s.rect(9, 7, 22, 7, shade(hat, 0.85))
    return finish(s, "lan", [ao[:3], quan[:3], hat[:3]])


def tuan():
    s = S()
    shirt = (236, 236, 242, 255)
    slacks = (86, 88, 98, 255)
    body(s, shirt, slacks, (24, 22, 26, 255))
    s.rect(15, 22, 16, 31, (150, 34, 44, 255))   # cà vạt nới lỏng
    s.p(14, 22, (150, 34, 44, 255))
    s.rect(7, 31, 8, 31, (220, 180, 60, 255))     # đồng hồ vàng
    s.rect(10, 33, 21, 33, (40, 36, 40, 255))     # thắt lưng
    face(s)
    hair = (40, 30, 26, 255)
    s.rows(5, [(12, 20), (10, 21), (9, 22), (9, 22)], hair)
    s.rect(9, 9, 13, 10, hair)                    # tóc vuốt rẽ ngôi
    s.rect(9, 9, 10, 13, hair); s.rect(21, 9, 22, 12, hair)
    hair_shine(s, hair, [(12, 6), (13, 6), (14, 6)])  # bóng tóc keo
    return finish(s, "tuan", [shirt[:3], slacks[:3]])


def khoa():
    s = S()
    shirt = (138, 128, 82, 255)
    pants = (70, 74, 60, 255)
    body(s, shirt, pants, (92, 60, 36, 255), wide=1)
    s.rect(12, 22, 12, 33, (60, 50, 40, 255)); s.rect(19, 22, 19, 33, (60, 50, 40, 255))  # dây balo
    s.rect(24, 30, 26, 35, (240, 210, 80, 255))  # đèn pin
    s.rect(24, 30, 26, 30, (250, 240, 170, 255))
    face(s)
    hair = (30, 28, 30, 255)
    s.rows(5, [(12, 19), (10, 21), (9, 22)], hair)
    s.rect(9, 8, 22, 9, hair)
    s.rect(9, 8, 10, 12, hair); s.rect(21, 8, 22, 12, hair)
    hair_shine(s, hair, [(12, 6), (13, 6)])
    frame = (20, 20, 24, 255)                     # kính
    s.rect(11, 13, 14, 16, frame); s.rect(17, 13, 20, 16, frame)
    s.rect(12, 14, 13, 15, (170, 200, 220, 255)); s.rect(18, 14, 19, 15, (170, 200, 220, 255))
    s.rect(15, 14, 16, 14, frame)
    return finish(s, "khoa", [shirt[:3], pants[:3]])


def phong():
    # con nhà thủ nhang, mang căn, đã bị tha hóa một phần
    s = S()
    shirt = (58, 46, 44, 255)
    pants = (36, 34, 40, 255)
    body(s, shirt, pants, (22, 20, 24, 255))
    s.rect(10, 22, 21, 23, shade(shirt, 1.25))          # cổ áo
    beads = (150, 96, 48, 255)                           # chuỗi hạt trầm ở cổ tay
    for x in (6, 8):
        s.p(x, 30, beads)
    s.p(7, 30, (196, 140, 70, 255))
    face(s)
    s.rect(12, 16, 13, 16, (176, 128, 128, 255))        # quầng thâm dưới mắt trái
    s.p(12, 17, SKIN)
    s.p(15, 18, SKIN_SH); s.p(16, 18, SKIN_SH)          # miệng mím
    corrupt = (96, 52, 120, 255)                          # vệt tha hóa lan từ cổ lên má phải
    for x, y in ((18, 20), (19, 19), (19, 18), (20, 17), (20, 16), (21, 15), (17, 21), (18, 22)):
        s.p(x, y, corrupt)
    hair = (22, 20, 26, 255)
    s.rows(5, [(12, 19), (10, 21), (9, 22), (9, 22)], hair)
    s.rect(9, 9, 10, 14, hair); s.rect(21, 9, 22, 13, hair)
    s.rect(12, 9, 20, 11, hair)
    s.rect(16, 12, 21, 15, hair)                         # tóc mái dài che mắt phải
    s.p(17, 16, hair); s.p(19, 16, hair)
    hair_shine(s, hair, [(12, 6), (13, 6)])
    return finish(s, "phong", [shirt[:3], pants[:3]])


def hai():
    # Hải trong ký ức: vẫn là cậu học sinh năm ấy, ướt sũng, da tái
    s = S()
    shirt = (226, 232, 236, 255)
    shorts = (40, 56, 96, 255)
    skin_pale = (204, 206, 196, 255)
    body(s, shirt, shorts, (70, 70, 80, 255), hands=False)
    s.rect(7, 32, 8, 33, skin_pale); s.rect(23, 32, 24, 33, shade(skin_pale, 0.85))
    s.rect(11, 39, 14, 43, skin_pale); s.rect(17, 39, 20, 43, shade(skin_pale, 0.85))   # quần đùi, chân trần
    s.rect(14, 26, 14, 26, (200, 40, 40, 255))          # phù hiệu đỏ trên túi áo
    s.rect(16, 24, 18, 24, (60, 90, 160, 255))           # khăn/tên trường
    face(s)
    for y in range(7, 22):                               # nhuộm da tái
        for x in range(9, 23):
            c = s.px[x, y]
            if c[3] and c[:3] == SKIN[:3]:
                s.px[x, y] = skin_pale
            elif c[3] and c[:3] == SKIN_SH[:3]:
                s.px[x, y] = shade(skin_pale, 0.82)
            elif c[3] and c[:3] == BLUSH[:3]:
                s.px[x, y] = shade(skin_pale, 0.9)
    s.rect(12, 14, 13, 15, (14, 14, 20, 255)); s.rect(17, 14, 18, 15, (14, 14, 20, 255))  # mắt đen đặc
    hair = (24, 28, 34, 255)                             # tóc ướt bết xuống
    s.rows(5, [(12, 19), (10, 21), (9, 22), (9, 22)], hair)
    s.rect(9, 9, 10, 17, hair); s.rect(21, 9, 22, 17, hair)
    for x in (11, 13, 15, 18, 20):                       # tóc mái bết thành sợi
        s.rect(x, 9, x, 12 + (x % 3), hair)
    s.rect(11, 9, 20, 10, hair)
    water = (120, 180, 210, 255)
    for x, y in ((9, 19), (22, 20), (7, 35), (24, 36), (12, 47), (19, 47)):  # nước nhỏ giọt
        s.p(x, y, water)
    hair_shine(s, hair, [(12, 6), (14, 6)])
    return finish(s, "hai", [shirt[:3], shorts[:3]])


def ong_cu():
    s = S()
    jacket = (70, 60, 56, 255)
    pants = (54, 50, 48, 255)
    skin = (222, 182, 146, 255)
    body(s, jacket, pants, (40, 34, 30, 255))
    s.rect(10, 22, 21, 23, shade(jacket, 1.3))          # cổ áo
    for y in (25, 28, 31):                               # cúc áo
        s.p(15, y, (190, 170, 120, 255))
    face(s, y_eye=15)
    for y in range(7, 22):                               # da ngăm hơn
        for x in range(9, 23):
            c = s.px[x, y]
            if c[3] and c[:3] == SKIN[:3]:
                s.px[x, y] = skin
    s.p(12, 17, shade(skin, 0.85)); s.p(18, 17, shade(skin, 0.85))   # bọng mắt
    s.p(19, 18, skin); s.p(12, 18, skin)
    hair = (196, 196, 200, 255)                          # tóc bạc thưa, trán hói
    s.rect(9, 9, 10, 15, hair); s.rect(21, 9, 22, 15, hair)
    s.rect(13, 6, 18, 6, hair); s.p(11, 7, hair); s.p(20, 7, hair)
    s.rect(14, 19, 17, 21, (214, 214, 218, 255))         # râu
    s.rect(15, 22, 16, 22, (214, 214, 218, 255))
    return finish(s, "ong_cu", [jacket[:3], pants[:3]])


def sheet(imgs, names):
    scale = 8
    pad = 24
    cw = W * scale
    img = Image.new("RGBA", (len(imgs) * (cw + pad) + pad, H * scale + 80), (30, 30, 40, 255))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
    except OSError:
        font = ImageFont.load_default()
    for i, (im, n) in enumerate(zip(imgs, names)):
        x = pad + i * (cw + pad)
        img.alpha_composite(im.resize((W * scale, H * scale), Image.NEAREST), (x, 20))
        tw = d.textlength(n, font=font)
        d.text((x + (cw - tw) / 2, H * scale + 32), n, fill=(240, 230, 210), font=font)
    img.save(os.path.join(OUT, "_sheet_preview.png"))


if __name__ == "__main__":
    imgs = [minh(), vy(), lan(), tuan(), khoa(), phong(), hai(), ong_cu()]
    sheet(imgs, ["Minh", "Vy", "Lan", "Tuấn", "Khoa", "Phong", "Hải", "Ông cụ"])
    print("done")
