"""Sprite pixel 40x40 cho quái. Chạy: python3 draw_enemies.py"""
from PIL import Image, ImageDraw, ImageFont
import os
import draw_characters as dc

W, H = 40, 40
OUT = dc.OUT
OUTLINE = (20, 14, 22, 255)


class E(dc.S):
    def __init__(self):
        self.img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        self.px = self.img.load()

    def p(self, x, y, c):
        if 0 <= x < W and 0 <= y < H:
            self.px[x, y] = c

    def ellipse(self, cx, cy, rx, ry, c):
        for y in range(cy - ry, cy + ry + 1):
            for x in range(cx - rx, cx + rx + 1):
                if ((x - cx) / (rx + 0.5)) ** 2 + ((y - cy) / (ry + 0.5)) ** 2 <= 1:
                    self.p(x, y, c)

    def line(self, pts, c, width=1):
        d = ImageDraw.Draw(self.img)
        d.line(pts, fill=c, width=width)

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

    def shade_right(self, colors, x_from):
        for y in range(H):
            for x in range(x_from, W):
                c = self.px[x, y]
                if c[3] and c[:3] in colors:
                    self.px[x, y] = dc.shade(c, 0.75)


def ma_doi():
    # Ngạ quỷ: đầu to, cổ kim, bụng trương, tay chân que, miệng há
    s = E()
    skin = (128, 142, 112, 255)
    rag = (196, 188, 168, 255)
    # chân que, đứng khom
    s.line([(15, 30), (13, 37)], skin); s.line([(24, 30), (26, 37)], skin)
    s.rect(11, 37, 14, 38, skin); s.rect(25, 37, 28, 38, skin)
    s.ellipse(20, 26, 8, 6, skin)                     # bụng trương
    s.rect(13, 28, 27, 31, rag)                       # khố rách
    for x in (14, 17, 21, 25):
        s.p(x, 32, rag)
    s.ellipse(19, 24, 3, 2, dc.shade(skin, 1.15))     # sáng trên bụng
    for y in (20, 22):                                 # xương sườn
        s.line([(14, y), (17, y)], dc.shade(skin, 0.7))
    # tay que dài, ngón vuốt
    s.line([(12, 21), (6, 27), (5, 32)], skin)
    s.line([(28, 21), (33, 25), (35, 30)], skin)
    for x in (3, 5, 7):
        s.p(x, 33, (230, 226, 200, 255))
    for x in (34, 36):
        s.p(x, 31, (230, 226, 200, 255))
    s.rect(19, 15, 20, 19, skin)                      # cổ nhỏ như kim
    s.ellipse(19, 9, 8, 7, skin)                      # đầu to
    s.rect(13, 3, 15, 4, (60, 60, 56, 255)); s.rect(22, 2, 24, 3, (60, 60, 56, 255))  # tóc lơ thơ
    s.p(18, 2, (60, 60, 56, 255))
    s.ellipse(15, 8, 2, 2, (20, 16, 18, 255))         # hốc mắt
    s.ellipse(23, 8, 2, 2, (20, 16, 18, 255))
    s.p(15, 8, (250, 220, 90, 255)); s.p(23, 8, (250, 220, 90, 255))  # mắt đói phát sáng
    s.rect(15, 12, 23, 15, (60, 14, 20, 255))         # miệng há
    for x in (15, 17, 19, 21, 23):
        s.p(x, 12, (236, 230, 210, 255))
    for x in (16, 18, 20, 22):
        s.p(x, 15, (236, 230, 210, 255))
    s.shade_right([skin[:3], rag[:3]], 22)
    s.outline()
    s.img.save(os.path.join(OUT, "ma_doi.png"))
    return s.img


def ma_nuoc():
    # Ma da: tóc đen dài phủ mặt, da xanh tái, nửa dưới tan thành nước
    s = E()
    skin = (170, 196, 204, 255)
    hair = (16, 20, 28, 255)
    dress = (196, 206, 210, 255)
    water = (54, 108, 160, 255)
    water_hi = (84, 146, 196, 255)
    foam = (176, 218, 238, 255)
    # vai áo trắng và tay dài vươn về phía trước
    s.rect(11, 17, 29, 22, dress)
    s.line([(11, 19), (6, 23), (3, 21)], skin, 2)
    s.line([(29, 19), (34, 23), (37, 21)], skin, 2)
    for x, y in ((1, 20), (2, 19), (1, 22), (38, 20), (37, 19), (38, 22)):
        s.p(x, y, skin)
    # tóc: đỉnh tròn, loe dần xuống, mép so le thành lọn
    s.ellipse(20, 8, 6, 6, hair)
    for y in range(8, 33):
        half = 6 + (y - 8) // 4
        jag = (y * 3) % 2
        s.rect(20 - half - jag, y, 20 + half + (1 - jag), y, hair)
    for i, x in enumerate(range(13, 29, 2)):         # đuôi lọn tóc dài ngắn khác nhau
        s.rect(x, 33, x, 33 + (i * 5) % 4, hair)
    # khe mặt méo lộ qua tóc
    for y, (x0, x1) in zip(range(11, 22), [(19, 20), (18, 21), (18, 21), (18, 22), (18, 21),
                                           (19, 21), (19, 21), (18, 21), (19, 20), (19, 20), (19, 19)]):
        s.rect(x0, y, x1, y, skin)
        s.p(x1, y, dc.shade(skin, 0.75))
    s.p(19, 14, (232, 36, 36, 255))                   # một mắt đỏ
    s.rect(19, 18, 20, 19, (30, 14, 24, 255))         # miệng há
    s.p(15, 3, (64, 74, 96, 255)); s.p(16, 3, (64, 74, 96, 255)); s.p(14, 4, (64, 74, 96, 255))
    # nửa dưới tan thành nước: các dải sóng ngang
    for y in range(33, 40):
        half = 9 + (y - 33) * 2
        for x in range(20 - half, 20 + half + 1):
            wave = (x + (y // 2) * 3) % 6
            s.p(x, y, water_hi if wave < 2 and y % 2 == 0 else water)
    for x in range(4, 37, 4):
        s.p(x, 33 + (x // 4) % 2, foam)
    for x, y in ((8, 27), (32, 28), (5, 30), (35, 31), (24, 37), (13, 38)):
        s.p(x, y, foam)
    s.shade_right([skin[:3], dress[:3]], 23)
    s.outline()
    s.img.save(os.path.join(OUT, "ma_nuoc.png"))
    return s.img


def ma_nhen():
    # Ma nhện: thân tròn đen, mặt người tái trên lưng, tám chân gập khúc
    s = E()
    body = (44, 38, 52, 255)
    leg = (70, 60, 78, 255)
    face = (196, 196, 184, 255)
    legs = [  # (gốc, khớp, mũi) mỗi bên 4 chân
        ((14, 20), (7, 12), (2, 22)), ((14, 23), (5, 18), (1, 30)),
        ((15, 26), (6, 26), (3, 36)), ((16, 28), (10, 31), (8, 38)),
    ]
    for (a, b, c) in legs:
        s.line([a, b, c], leg, 2)
        s.line([(40 - a[0], a[1]), (40 - b[0], b[1]), (40 - c[0], c[1])], leg, 2)
        s.p(b[0], b[1] - 1, shade_l(leg, 1.4)); s.p(40 - b[0], b[1] - 1, shade_l(leg, 1.4))
    s.ellipse(20, 24, 8, 7, body)                     # thân
    s.ellipse(20, 14, 5, 4, shade_l(body, 1.2))       # đầu ngực
    for x, y in ((17, 12), (19, 11), (21, 11), (23, 12)):   # cụm mắt nhện
        s.p(x, y, (230, 60, 60, 255))
    s.ellipse(20, 25, 5, 5, face)                     # mặt người trên lưng
    s.rect(15, 20, 25, 21, (20, 18, 24, 255))         # tóc mái đen
    s.p(15, 22, (20, 18, 24, 255)); s.p(25, 22, (20, 18, 24, 255))
    s.rect(17, 24, 18, 25, (16, 12, 16, 255)); s.rect(22, 24, 23, 25, (16, 12, 16, 255))
    s.p(17, 24, (240, 50, 50, 255)); s.p(23, 24, (240, 50, 50, 255))
    s.rect(19, 28, 21, 29, (60, 14, 20, 255))         # miệng
    s.line([(20, 31), (20, 36)], (220, 220, 230, 255))   # sợi tơ rủ xuống
    s.shade_right([body[:3], face[:3]], 23)
    s.outline()
    s.img.save(os.path.join(OUT, "ma_nhen.png"))
    return s.img


def shade_l(c, f):
    return dc.shade(c, f) if f <= 1 else (min(255, int(c[0] * f)), min(255, int(c[1] * f)), min(255, int(c[2] * f)), 255)


if __name__ == "__main__":
    imgs = [ma_doi(), ma_nuoc(), ma_nhen()]
    scale, pad = 8, 24
    cw = W * scale
    sheet = Image.new("RGBA", (len(imgs) * (cw + pad) + pad, H * scale + 80), (30, 30, 40, 255))
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
    except OSError:
        font = ImageFont.load_default()
    for i, (im, n) in enumerate(zip(imgs, ["Ma đói", "Ma nước", "Ma nhện"])):
        x = pad + i * (cw + pad)
        sheet.alpha_composite(im.resize((cw, H * scale), Image.NEAREST), (x, 20))
        tw = d.textlength(n, font=font)
        d.text((x + (cw - tw) / 2, H * scale + 32), n, fill=(240, 230, 210), font=font)
    sheet.save(os.path.join(OUT, "_enemies_preview.png"))
    print("done")
