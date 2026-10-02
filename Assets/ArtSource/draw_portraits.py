"""Chân dung 48x48 (nửa người, mặt người lớn) cho thẻ trận, bảng chọn người, hội thoại sau này.
Chạy: python draw_portraits.py → ghi thẳng vào Assets/Resources/Portraits/<tên>.png
Mặt dựng bằng hình học + chi tiết vẽ tay (mắt, mày, mũi, miệng); tóc, áo riêng từng người."""
from PIL import Image, ImageDraw, ImageFont
import math
import os
import random

N = 48
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
ASSETS = PARENT if os.path.basename(PARENT) == "Assets" else os.path.join(PARENT, "Assets")
OUT = os.path.join(ASSETS, "Resources", "Portraits")
PREVIEW = os.path.join(HERE, "sprites")
os.makedirs(OUT, exist_ok=True)
os.makedirs(PREVIEW, exist_ok=True)

SKIN = (236, 192, 156)
WHITE = (244, 240, 234)


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c[:3])


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# nửa bề rộng mặt theo từng dòng (mặt chiếm dòng 9..34, tâm x = 23.5)
FACE_HW = {9: 7, 10: 9, 11: 10, 12: 10.5, 25: 10.5, 26: 10, 27: 9.5, 28: 9, 29: 8.5, 30: 7.5, 31: 6.5, 32: 5.5,
           33: 4.5, 34: 3}
for _y in range(13, 25):
    FACE_HW[_y] = 11


class P:
    def __init__(self, skin=SKIN):
        self.img = Image.new("RGBA", (N, N), (0, 0, 0, 0))
        self.px = self.img.load()
        self.skin = skin
        self.sh = shade(skin, 0.84)
        self.sh2 = shade(skin, 0.72)

    def p(self, x, y, c, a=255):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < N and 0 <= y < N:
            self.px[x, y] = tuple(c[:3]) + (a,)

    def get(self, x, y):
        return self.px[x, y] if 0 <= x < N and 0 <= y < N else (0, 0, 0, 0)

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.p(x, y, c)

    def fill(self, test, colorf):
        for y in range(N):
            for x in range(N):
                if test(x, y):
                    c = colorf(x, y)
                    if c is not None:
                        self.p(x, y, c)

    def outline(self, col=(28, 20, 26)):
        src = self.img.copy().load()
        for y in range(N):
            for x in range(N):
                if src[x, y][3]:
                    continue
                nb = [src[x + dx, y + dy] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                      if 0 <= x + dx < N and 0 <= y + dy < N and src[x + dx, y + dy][3]]
                if nb:
                    d = min(nb, key=lambda c: c[0] + c[1] + c[2])
                    self.px[x, y] = mix(shade(d, 0.4), col, 0.5) + (255,)


def in_face(x, y):
    hw = FACE_HW.get(y)
    return hw is not None and 23.5 - hw <= x + 0.5 <= 23.5 + hw


# ---------- Các phần chung ----------

def body(p, cloth, collar=None, wide=0):
    """Vai và áo: hình thang từ dòng 38 xuống đáy."""
    for y in range(37, N):
        t = (y - 37) / 10.0
        half = 11 + wide + t * 11
        for x in range(N):
            if abs(x + 0.5 - 24) <= half:
                c = cloth
                if x > 24 + half * 0.35:
                    c = shade(cloth, 0.8)
                if y == 37 or (abs(x + 0.5 - 24) > half - 1.5 and y < 40):
                    c = shade(cloth, 1.1) if x < 24 else shade(cloth, 0.75)
                p.p(x, y, c)
    if collar:
        collar(p)


def neck(p):
    for y in range(32, 40):
        for x in range(19, 29):
            c = p.skin if x < 25 else p.sh
            if y <= 35:
                c = p.sh2 if y <= 34 else p.sh  # bóng dưới cằm
            p.p(x, y, c)


def face(p):
    def col(x, y):
        hw = FACE_HW[y]
        right = x + 0.5 - 23.5
        c = p.skin
        if right > hw * 0.58:
            c = p.sh
        if right > hw * 0.9:
            c = p.sh2
        if y >= 31 and right > -hw * 0.3:
            c = p.sh
        if right < -hw * 0.75 and y > 14:
            c = mix(p.skin, p.sh, 0.4)
        return c
    p.fill(in_face, col)
    for y in range(19, 26):  # tai
        for x in (12, 13):
            p.p(x, y, p.skin if x == 13 else p.sh)
        for x in (34, 35):
            p.p(x, y, p.sh2)
    p.p(13, 22, p.sh2)
    p.p(34, 22, shade(p.sh2, 0.85))


def eyes(p, iris=(70, 52, 44), mood="normal", hollow=False, red=False):
    lash = (34, 24, 30)
    for ex in (16, 26):
        if hollow:
            p.rect(ex, 20, ex + 5, 22, (18, 18, 26))
            if red:
                p.p(ex + 2, 21, (230, 40, 40))
                p.p(ex + 3, 21, (150, 20, 24))
            continue
        p.rect(ex, 20, ex + 5, 20, lash)              # mi trên
        p.p(ex - (1 if ex == 16 else -6), 20, lash)   # đuôi mắt
        p.rect(ex + 1, 21, ex + 4, 22, WHITE)
        p.rect(ex + 2, 21, ex + 3, 22, iris)
        p.p(ex + 2, 21, mix(iris, (255, 255, 255), 0.55))  # chấm sáng
        p.p(ex + 3, 22, shade(iris, 0.6))
        p.rect(ex + 1, 23, ex + 4, 23, shade(p.skin, 0.88))  # mí dưới
    # lông mày
    bc = p.brow
    if mood == "angry":
        for i in range(6):
            p.p(15 + i, 17 + (i // 3), bc)
            p.p(32 - i, 17 + (i // 3), bc)
    elif mood == "sad":
        for i in range(6):
            p.p(15 + i, 18 - (i // 3), bc)
            p.p(32 - i, 18 - (i // 3), bc)
    else:
        for i in range(6):
            p.p(15 + i, 17 if 1 <= i <= 4 else 18, bc)
            p.p(32 - i, 17 if 1 <= i <= 4 else 18, bc)


def nose_mouth(p, mood="normal", open_mouth=False):
    for y in range(22, 27):
        p.p(25, y, p.sh)
    p.p(23, 23, mix(p.skin, (255, 255, 255), 0.25))
    p.p(23, 27, p.sh2)
    p.p(24, 27, p.sh)
    p.p(25, 27, p.sh2)
    lip = (166, 84, 80)
    if open_mouth:
        p.rect(20, 29, 27, 32, (40, 14, 18))
        for x in range(20, 28, 2):
            p.p(x, 29, (220, 214, 200))
            p.p(x + 1, 32, (220, 214, 200))
        return
    if mood == "sad":
        p.rect(21, 30, 26, 30, lip)
        p.p(20, 31, lip)
        p.p(27, 31, lip)
    else:
        p.rect(21, 30, 26, 30, lip)
        p.p(20, 29, shade(lip, 1.1))
        p.p(27, 29, shade(lip, 1.1))
        p.rect(22, 31, 25, 31, mix(p.skin, lip, 0.35))
    p.p(17, 26, mix(p.skin, (236, 140, 130), 0.4))  # má
    p.p(30, 26, mix(p.sh, (236, 140, 130), 0.3))


def hair_cap(p, hair, fringe, top=9, spread=14.5, side_to=24, highlight=True, seed=0):
    """Tóc phủ đỉnh đầu: trong elip sọ và trên đường mái fringe(x)."""
    hl = mix(hair, (190, 196, 230), 0.38) if sum(hair) < 200 else mix(hair, (255, 240, 210), 0.35)
    mid = shade(hair, 0.82)
    dk = shade(hair, 0.62)
    cells = set()
    for y in range(N):
        for x in range(N):
            e = ((x + 0.5 - 24) / spread) ** 2 + ((y + 0.5 - 20) / (20 - top + 3)) ** 2
            if e > 1 or y > side_to or y > fringe(x):
                continue
            cells.add((x, y))
            c = hair
            if x > 30 or y >= fringe(x) - 1:
                c = dk  # mép mái và bên phải tối
            elif x > 27 or y >= fringe(x) - 3:
                c = mid
            p.p(x, y, c)
    for x0 in range(13, 36, 4):  # sợi tóc chéo từ đỉnh xuống mái
        for k in range(12):
            q = (x0 - k // 3, top + 3 + k)
            if q in cells and q[1] < fringe(q[0]) - 1:
                p.p(q[0], q[1], dk if q[0] > 27 else mid)
    if highlight:  # vệt sáng cong trên đỉnh đầu
        for x in range(15, 28):
            y = top + 3 + round(((x - 21) / 6.5) ** 2 * 2)
            if (x, y) in cells and x % 4 != 3:
                p.p(x, y, hl)
                if 17 <= x <= 24 and (x, y + 1) in cells:
                    p.p(x, y + 1, mix(hl, hair, 0.5))


def back_hair(p, hair, y_end, half_top=15, half_bottom=17, part=False):
    dk = shade(hair, 0.62)
    for y in range(12, y_end + 1):
        t = (y - 12) / max(1, y_end - 12)
        half = half_top + (half_bottom - half_top) * t
        for x in range(N):
            if abs(x + 0.5 - 24) <= half:
                c = hair if x < 24 else dk
                if (x * 7 + y) % 9 == 0:
                    c = shade(hair, 0.8)
                p.p(x, y, c)


def glasses(p, frame=(48, 42, 44)):
    for ex in (15, 25):
        for x in range(ex, ex + 8):
            p.p(x, 19, frame)
            p.p(x, 24, frame)
        for y in range(19, 25):
            p.p(ex, y, frame)
            p.p(ex + 7, y, frame)
        p.p(ex + 1, 20, (226, 238, 248))
    p.p(23, 21, frame)
    p.p(24, 21, frame)


# ---------- Từng người ----------

def minh():
    p = P()
    p.brow = (28, 26, 38)
    neck(p)
    body(p, (86, 60, 128), collar=lambda q: [q.p(x, y, (156, 126, 196)) for y in range(38, 48) for x in (23 - (y - 38) // 2, 24 + (y - 38) // 2)]
         or [q.p(x, y, (40, 30, 60)) for y in range(39, 48) for x in range(24 - (y - 38) // 2 + 1, 24 + (y - 38) // 2)])
    face(p)
    eyes(p, iris=(56, 40, 36))
    nose_mouth(p)
    hair = (28, 26, 38)
    hair_cap(p, hair, lambda x: 15 + (0, 2, 3, 1, 0, 2)[x % 6] + (5 if x < 14 or x > 33 else 0), top=6, spread=15.5, side_to=25)
    for x, h in ((17, 3), (21, 2), (26, 3), (30, 2)):  # tóc dựng
        for k in range(h):
            p.p(x, 5 - k, hair)
            p.p(x + 1, 6 - k, hair)
    p.outline()
    return p.img


def vy():
    p = P()
    p.brow = (150, 64, 36)
    hair = (196, 86, 46)
    back_hair(p, hair, 42, 15, 18)
    neck(p)
    body(p, (234, 182, 52), collar=lambda q: [q.p(x, 38, (250, 236, 196)) for x in range(19, 29)])
    face(p)
    eyes(p, iris=(96, 64, 40))
    nose_mouth(p)
    hair_cap(p, hair, lambda x: (17 + (1 if x % 3 == 0 else 0)) if 14 <= x <= 33 else 34, top=7, spread=15.5, side_to=34)
    for y in range(17, 36):  # tóc hai bên mặt
        for x in (12, 13, 14):
            p.p(x, y, hair if x < 14 else shade(hair, 0.8))
        for x in (33, 34, 35):
            p.p(x, y, shade(hair, 0.62))
    p.rect(33, 13, 35, 14, (70, 140, 210))  # kẹp tóc
    p.outline()
    return p.img


def lan():
    p = P()
    p.brow = (24, 22, 30)
    hair = (24, 22, 30)
    back_hair(p, hair, 36, 14, 15)
    neck(p)
    body(p, (62, 124, 88), collar=lambda q: [q.p(x, 38, (40, 90, 60)) for x in range(18, 30)]
         + [q.p(24, y, (196, 186, 140)) for y in (41, 44)])
    face(p)
    eyes(p, iris=(40, 30, 30))
    nose_mouth(p)
    hair_cap(p, hair, lambda x: 14 + abs(x - 24) // 2 if 13 <= x <= 34 else 30, top=8, spread=15, side_to=30)
    for y in range(28, 46):  # bím tóc vắt trước vai phải
        x = 32 + (1 if y % 4 < 2 else 0)
        p.p(x, y, hair)
        p.p(x + 1, y, shade(hair, 0.7) if y % 2 else hair)
    p.rect(32, 44, 34, 45, (214, 60, 60))
    p.outline()
    return p.img


def tuan():
    p = P()
    p.brow = (48, 36, 30)
    neck(p)

    def suit(q):
        for y in range(37, 48):
            w = 2 + (y - 37) // 2
            for x in range(24 - w, 24 + w):
                q.p(x, y, (240, 240, 244))
        for y in range(38, 48):
            for x in (23, 24):
                q.p(x, y, (170, 36, 48) if y > 38 else (130, 26, 36))
        for y in range(38, 48):
            q.p(24 - 2 - (y - 37) // 2, y, (40, 42, 56))
            q.p(24 + 1 + (y - 37) // 2, y, (40, 42, 56))
    body(p, (62, 66, 84), collar=suit)
    face(p)
    eyes(p, iris=(60, 44, 36))
    nose_mouth(p)
    hair = (48, 36, 30)
    hair_cap(p, hair, lambda x: (15 if x < 26 else 13) + (4 if x < 14 or x > 33 else 0), top=7, spread=15, side_to=22, seed=4)
    for x in range(14, 27):  # đường rẽ ngôi, tóc vuốt
        p.p(x, 13 - (x - 14) // 5, mix(hair, (255, 230, 200), 0.3))
    p.outline()
    return p.img


def khoa():
    p = P()
    p.brow = (30, 28, 34)
    neck(p)
    body(p, (120, 118, 70), collar=lambda q: [q.p(x, y, (92, 90, 52)) for y in range(37, 41) for x in range(16 + (y - 37), 20 + (y - 37))]
         + [q.p(x, y, (92, 90, 52)) for y in range(37, 41) for x in range(28 - (y - 37), 32 - (y - 37))]
         + [q.p(x, y, (110, 84, 56)) for y in range(40, 48) for x in (12, 13, 34, 35)])
    face(p)
    eyes(p, iris=(50, 40, 34))
    nose_mouth(p)
    hair = (30, 28, 34)
    hair_cap(p, hair, lambda x: 16 + (4 if x < 14 or x > 33 else 0) + (1 if x % 3 == 0 else 0), top=7, spread=15, side_to=22, seed=5)
    glasses(p, (120, 104, 88))
    p.outline()
    return p.img


def phong():
    p = P((228, 190, 162))
    p.brow = (20, 18, 24)
    hair = (20, 18, 24)
    back_hair(p, hair, 38, 15, 16)
    neck(p)
    body(p, (58, 46, 44))
    face(p)
    eyes(p, iris=(40, 30, 34))
    for x in range(16, 22):  # quầng thâm
        p.p(x, 24, shade(p.skin, 0.8))
    nose_mouth(p, mood="sad")
    hair_cap(p, hair, lambda x: 16 if x < 23 else 27 - abs(x - 30) // 2, top=7, spread=15.5, side_to=30, seed=6)
    for (x, y) in ((27, 34), (28, 35), (27, 36), (26, 37), (28, 37), (29, 36), (25, 38), (30, 38)):  # vết tha hoá
        p.p(x, y, (112, 60, 148))
    p.outline()
    return p.img


def hai(corrupt=False):
    skin = (150, 164, 176) if corrupt else (198, 208, 204)
    p = P(skin)
    p.brow = (22, 28, 36)
    hair = (14, 16, 22) if corrupt else (22, 28, 36)
    if corrupt:
        back_hair(p, hair, 46, 16, 20)
    neck(p)
    body(p, (60, 66, 80) if corrupt else (222, 230, 234),
         collar=None if corrupt else (lambda q: [q.p(x, 38, (200, 208, 214)) for x in range(18, 30)]
                                      + [q.p(x, 41, (60, 90, 160)) for x in range(28, 32)] + [q.p(17, 42, (200, 40, 40))]))
    face(p)
    eyes(p, hollow=True, red=corrupt)
    nose_mouth(p, mood="sad", open_mouth=corrupt)
    hair_cap(p, hair, lambda x: 15, top=8, spread=15, side_to=33 if corrupt else 26, highlight=False, seed=7)
    for x in range(14, 34, 2):  # tóc bết thành sợi
        for y in range(15, 19 + (x * 7) % 5):
            p.p(x, y, hair)
    rnd = random.Random(1)
    for _ in range(8):  # giọt nước
        p.p(rnd.randint(12, 36), rnd.randint(24, 40), (140, 200, 230))
    if corrupt:
        for (x, y) in ((15, 25), (14, 27), (15, 29), (32, 26), (33, 28), (31, 30)):
            p.p(x, y, (112, 60, 148))
    p.outline()
    return p.img


def ong_cu():
    p = P((222, 180, 144))
    p.brow = (200, 200, 206)
    neck(p)
    body(p, (86, 70, 58), collar=lambda q: [q.p(x, 37, (110, 92, 76)) for x in range(17, 31)]
         + [q.p(24, y, (180, 160, 110)) for y in (41, 44, 47)])
    face(p)
    eyes(p, iris=(70, 56, 46))
    nose_mouth(p)
    for y in (12, 14):  # nếp nhăn trán
        for x in range(18, 30):
            if (x + y) % 3:
                p.p(x, y, p.sh)
    for x in (16, 31):
        p.p(x, 24, p.sh2)
    grey = (196, 196, 202)
    for y in range(13, 26):  # tóc bạc hai bên, đỉnh hói
        for x in (11, 12, 13, 14):
            p.p(x, y, grey if (x + y) % 3 else shade(grey, 0.8))
        for x in (33, 34, 35, 36):
            p.p(x, y, shade(grey, 0.82) if (x + y) % 3 else shade(grey, 0.68))
    beard = (226, 226, 230)
    for y in range(28, 40):  # râu
        half = 6 - max(0, y - 34)
        for x in range(24 - half, 24 + half):
            p.p(x, y, beard if x < 25 else shade(beard, 0.85))
    p.rect(19, 28, 28, 29, shade(beard, 0.92))  # ria
    p.outline()
    return p.img


PORTRAITS = [("minh", "Minh", minh), ("vy", "Vy", vy), ("lan", "Lan", lan), ("tuan", "Tuấn", tuan),
             ("khoa", "Khoa", khoa), ("phong", "Phong", phong), ("hai", "Hải", lambda: hai(False)),
             ("hai_tha_hoa", "Hải (tha hóa)", lambda: hai(True)), ("ong_cu", "Ông cụ", ong_cu)]


def main():
    imgs = []
    for key, label, fn in PORTRAITS:
        im = fn()
        im.save(os.path.join(OUT, key + ".png"))
        imgs.append((label, im))
    sc, pad = 5, 16
    cw = N * sc
    sheet = Image.new("RGBA", (5 * (cw + pad) + pad, 2 * (cw + 46) + pad), (30, 30, 40, 255))
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 20)
    except OSError:
        font = ImageFont.load_default()
    for i, (label, im) in enumerate(imgs):
        x, y = pad + (i % 5) * (cw + pad), pad + (i // 5) * (cw + 46)
        d.rectangle((x, y, x + cw, y + cw), fill=(52, 48, 64))
        sheet.alpha_composite(im.resize((cw, cw), Image.NEAREST), (x, y))
        tw = d.textlength(label, font=font)
        d.text((x + (cw - tw) / 2, y + cw + 8), label, fill=(240, 230, 210), font=font)
    sheet.save(os.path.join(PREVIEW, "_portraits_preview.png"))


if __name__ == "__main__":
    main()
    print("done →", OUT)
