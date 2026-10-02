"""Đồ họa trận nhìn ngang: ma quay trái (cùng độ to pixel với sprite đi 16x24), nền đêm Điện Thoải phủ, icon.
Chạy: python draw_battle.py → Assets/Resources/Battle/
  ma_<tên>_0/1.png (2 khung lơ lửng) · backdrop.png 512x288 · icon_*.png"""
from PIL import Image, ImageDraw
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
ASSETS = PARENT if os.path.basename(PARENT) == "Assets" else os.path.join(PARENT, "Assets")
OUT = os.path.join(ASSETS, "Resources", "Battle")
PREVIEW = os.path.join(HERE, "sprites")
os.makedirs(OUT, exist_ok=True)
os.makedirs(PREVIEW, exist_ok=True)
OUTL = (24, 16, 22)


def shade(c, f):
    return (max(0, min(255, int(c[0] * f))), max(0, min(255, int(c[1] * f))), max(0, min(255, int(c[2] * f))))


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


class S:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        self.px = self.img.load()

    def p(self, x, y, c, a=255):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[x, y] = tuple(c[:3]) + (a,)

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.p(x, y, c)

    def ellipse(self, cx, cy, rx, ry, c):
        for y in range(int(cy - ry - 1), int(cy + ry + 2)):
            for x in range(int(cx - rx - 1), int(cx + rx + 2)):
                if ((x - cx) / (rx + 0.4)) ** 2 + ((y - cy) / (ry + 0.4)) ** 2 <= 1:
                    self.p(x, y, c)

    def line(self, x0, y0, x1, y1, c):
        n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
        for i in range(n + 1):
            t = i / max(1, n)
            self.p(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, c)

    def outline(self, col=OUTL):
        src = self.img.copy().load()
        for y in range(self.h):
            for x in range(self.w):
                if src[x, y][3] == 0:
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.w and 0 <= ny < self.h and src[nx, ny][3] == 255:
                            self.px[x, y] = col + (255,)
                            break

    def save(self, name):
        self.img.save(os.path.join(OUT, name + ".png"))
        return self.img


# ---------- Ma (quay trái) ----------

def blob(s, cx, cy, rx, ry, base, light=1.18, dark=0.7, tones=4):
    """Elip đổ bóng theo hướng sáng trên-trái, chia bậc màu rõ (kiểu pixel art)."""
    for y in range(int(cy - ry - 1), int(cy + ry + 2)):
        for x in range(int(cx - rx - 1), int(cx + rx + 2)):
            dx, dy = (x - cx) / (rx + 0.4), (y - cy) / (ry + 0.4)
            if dx * dx + dy * dy <= 1:
                t = (dx + dy * 1.2) * 0.5 + 0.5  # 0 = sáng, 1 = tối
                step = min(tones - 1, int(t * tones))
                f = light + (dark - light) * step / (tones - 1)
                s.p(x, y, shade(base, f))


def thick_line(s, x0, y0, x1, y1, c, w=1, c2=None):
    n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
    for i in range(n + 1):
        t = i / max(1, n)
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        for k in range(w):
            s.p(x, y + k, c if k == 0 or c2 is None else c2)


def ma_doi(f):
    """Ma đói (quay trái): đầu to hói, miệng há răng lởm chởm, xương sườn lộ, bụng ỏng, tay chân khẳng khiu."""
    s = S(36, 44)
    skin = (122, 142, 100)
    dk, belly, bone = shade(skin, 0.68), (156, 170, 128), (226, 220, 196)
    y = f
    # chân gập, bàn chân to
    thick_line(s, 20, 30 + y, 16, 36, dk, 2)
    thick_line(s, 16, 36, 18, 41, dk, 2)
    s.rect(13, 41, 19, 42, dk)
    thick_line(s, 24, 30 + y, 27, 36, shade(dk, 0.85), 2)
    thick_line(s, 27, 36, 25, 41, shade(dk, 0.85), 2)
    s.rect(23, 41, 29, 42, shade(dk, 0.85))
    # tay sau
    thick_line(s, 22, 17 + y, 28, 24 + y, shade(dk, 0.85), 2)
    # thân gầy + bụng ỏng
    blob(s, 22, 20 + y, 5, 5, skin)
    blob(s, 21, 27 + y, 8, 7, skin)
    blob(s, 19, 28 + y, 4, 4, belly, 1.1, 0.9, 2)
    for k in range(3):  # xương sườn
        for x in range(18, 25):
            if (x + k) % 2 == 0:
                s.p(x, 17 + k * 2 + y, dk)
    s.rect(15, 32 + y, 27, 34 + y, (170, 160, 130))  # khố rách
    for x in range(15, 28, 3):
        s.p(x, 35 + y, (150, 140, 110))
    # đầu to
    blob(s, 15, 10 + y, 10, 9, skin)
    s.p(24, 6 + y, dk); s.p(25, 7 + y, dk)  # tai nhọn
    s.p(25, 6 + y, skin)
    for x, h in ((13, 3), (17, 2), (20, 3)):  # vài sợi tóc lơ thơ
        for k in range(h):
            s.p(x + k // 2, 1 - k + y + 2, (40, 44, 36))
    s.rect(8, 6 + y, 12, 8 + y, (24, 20, 20))  # hốc mắt
    s.p(9, 7 + y, (250, 220, 70)); s.p(10, 7 + y, (200, 160, 40))
    s.rect(4, 11 + y, 14, 17 + y, (74, 18, 24))  # miệng há
    s.rect(5, 15 + y, 13, 17 + y, (110, 30, 36))
    for x in range(5, 14, 2):  # răng
        s.p(x, 11 + y, bone); s.p(x, 12 + y, bone)
        s.p(x + 1, 17 + y, bone); s.p(x + 1, 16 + y, bone)
    s.p(3, 10 + y, skin)
    # tay trước vươn ra, móng dài
    ay = 22 + y + (1 if f else -1)
    thick_line(s, 18, 18 + y, 9, ay, skin, 2, dk)
    thick_line(s, 9, ay, 3, ay - 2, skin, 2, dk)
    for k in range(3):
        s.p(1, ay - 3 + k * 2, bone)
        s.p(2, ay - 3 + k * 2, bone)
    s.outline()
    return s


def ma_nuoc(f):
    """Ma nước (quay trái): hồn nữ tóc đen dài ướt, váy trắng, lơ lửng, tay tái vươn ra, chân tan thành sương."""
    s = S(34, 48)
    hair, hair_dk = (18, 22, 30), (34, 42, 56)
    skin = (214, 222, 226)
    dress, dress_dk = (226, 232, 236), (164, 178, 192)
    y = -f
    # váy trắng loe, rách gấu
    for yy in range(18, 44):
        t = (yy - 18) / 26.0
        half = 5 + t * 6
        cx = 18 + t * 1.5
        for x in range(int(cx - half), int(cx + half) + 1):
            c = dress if x < cx + half * 0.2 else dress_dk
            if (x * 3 + yy) % 7 == 0:
                c = shade(c, 0.92)
            a = 255 if yy < 36 else int(255 * (1 - (yy - 36) / 9.0))  # tan dần
            if yy >= 40 and (x + yy) % 3 == 0:
                continue
            s.p(x, yy + y, c, max(40, a))
    # tóc dài trùm lưng
    for yy in range(4, 38):
        t = (yy - 4) / 34.0
        x0 = 15 + int(t * 3)
        x1 = 26 + int(math.sin(yy * 0.4 + f) * 1.5)
        for x in range(x0, x1):
            s.p(x, yy + y, hair if (x + yy // 2) % 4 else hair_dk)
    blob(s, 17, 9 + y, 7, 6, hair, 1.4, 0.8, 3)
    # mặt nghiêng tái, tóc mái rủ che nửa
    blob(s, 12, 12 + y, 4, 5, skin, 1.0, 0.82, 3)
    s.p(8, 13 + y, skin)
    s.p(10, 11 + y, (20, 16, 24)); s.p(10, 12 + y, (190, 30, 34))  # mắt
    s.rect(10, 15 + y, 11, 15 + y, (70, 40, 50))
    for x in (13, 14, 16):
        for k in range(8 + (x % 3) * 2):
            s.p(x, 6 + k + y, hair)
    # tay tái vươn ra
    thick_line(s, 15, 21 + y, 7, 25 + y, skin, 2, shade(skin, 0.82))
    thick_line(s, 7, 25 + y, 2, 24 + y, skin, 1)
    for k in range(3):
        s.p(1, 23 + k + y, skin)
    # giọt nước
    for x, yy in ((5, 29), (22, 40), (12, 34), (27, 30)):
        s.p(x, yy + y + f, (140, 200, 230), 200)
    s.outline()
    for yy in range(36, 48):  # viền sương cũng mờ dần
        for x in range(34):
            r, g, b, a = s.px[x, yy]
            if a and (r, g, b) == OUTL:
                s.px[x, yy] = (r, g, b, int(a * max(0.0, 1 - (yy - 36) / 8.0)))
    return s


def ma_nhen(f):
    """Ma nhện (quay trái): bụng nhện lớn hoa văn đỏ, đầu là mặt người trắng bệch tóc rủ, tám chân gập."""
    s = S(46, 36)
    body, leg, leg_hl = (54, 44, 64), (92, 76, 110), (140, 122, 160)
    y = f
    legs = [(14, 6, 1), (18, 12, 5), (26, 34, 40), (30, 39, 45)]
    for i, (bx, kx, fx) in enumerate(legs):  # chân sau (tối) vẽ trước
        lift = 2 if (i + f) % 2 else 0
        thick_line(s, bx + 2, 16 + y, kx + 2, 5 + y + lift, shade(leg, 0.62), 2)
        thick_line(s, kx + 2, 5 + y + lift, fx + 1, 32, shade(leg, 0.62), 2)
    blob(s, 30, 15 + y, 12, 9, body)  # bụng
    for (x, yy) in ((28, 12), (29, 13), (30, 14), (31, 13), (32, 12), (30, 15), (30, 16), (29, 17), (31, 17)):
        s.p(x, yy + y, (190, 36, 40))  # hoa văn đỏ
    blob(s, 17, 17 + y, 6, 5, shade(body, 1.1))  # ngực
    for i, (bx, kx, fx) in enumerate(legs):  # chân trước
        lift = 0 if (i + f) % 2 else 2
        thick_line(s, bx, 18 + y, kx, 7 + y + lift, leg_hl, 2, leg)
        thick_line(s, kx, 7 + y + lift, fx, 33, leg_hl, 2, leg)
        s.rect(kx - 1, 6 + y + lift, kx + 1, 8 + y + lift, leg_hl)  # khớp gối
        s.p(fx, 34, shade(leg, 0.6))
    # mặt người + tóc rủ
    blob(s, 9, 19 + y, 6, 6, (214, 210, 200), 1.05, 0.8, 3)
    for x in range(4, 16):
        for k in range(2 + (x * 7) % 4):
            s.p(x, 13 + k + y, (16, 14, 20))
    s.p(6, 19 + y, (20, 16, 20)); s.p(7, 19 + y, (200, 30, 34))
    s.p(10, 19 + y, (20, 16, 20)); s.p(11, 19 + y, (200, 30, 34))
    s.rect(7, 22 + y, 10, 23 + y, (60, 18, 24))
    s.p(8, 22 + y, (220, 214, 200))
    s.p(3, 20 + y, (214, 210, 200))
    thick_line(s, 9, 25 + y, 9, 34, (220, 222, 232), 1)  # sợi tơ
    s.outline()
    return s


# ---------- Nền trận: đêm ở Điện Thoải phủ ----------

GROUND = 118  # dòng bờ đất; BattleController.BackdropGround phải bằng số này


def backdrop():
    W, H = 448, 200
    img = Image.new("RGBA", (W, H))
    px = img.load()
    bay = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
    sky = [(16, 18, 34), (24, 26, 48), (34, 36, 62), (48, 46, 76)]
    for y in range(H):
        for x in range(W):
            t = y / 96.0 + (bay[y & 3][x & 3] / 16.0 - 0.5) * 0.25
            px[x, y] = sky[max(0, min(3, int(t * 4)))] + (255,)
    r = random.Random(3)
    for _ in range(80):  # sao
        x, y = r.randrange(W), r.randrange(70)
        px[x, y] = (200, 200, 220, 255) if r.random() < 0.3 else (120, 122, 150, 255)
    cx, cy = 340, 30  # trăng
    for y in range(cy - 16, cy + 17):
        for x in range(cx - 16, cx + 17):
            d = math.hypot(x - cx, y - cy)
            if d <= 13:
                px[x, y] = ((236, 232, 210) if (x - cx) + (y - cy) < 6 else (206, 202, 186)) + (255,)
            elif d <= 16 and (bay[y & 3][x & 3] / 16.0) < (16 - d) / 3.0:
                px[x, y] = mix(px[x, y][:3], (120, 120, 140), 0.6) + (255,)
    for x, y, rr in ((335, 27, 2), (344, 36, 3), (332, 37, 1)):
        for yy in range(y - rr, y + rr + 1):
            for xx in range(x - rr, x + rr + 1):
                if (xx - x) ** 2 + (yy - y) ** 2 <= rr * rr:
                    px[xx, yy] = (186, 182, 168, 255)

    def ridge(base, amp, col, seed, step):
        rr = random.Random(seed)
        h = base
        pts = []
        for x in range(0, W + step, step):
            h = max(base - amp, min(base + amp // 3, h + rr.randint(-amp // 2, amp // 2)))
            pts.append((x, h))
        for i in range(len(pts) - 1):
            (x0, h0), (x1, h1) = pts[i], pts[i + 1]
            for x in range(x0, min(W, x1)):
                top = int(h0 + (h1 - h0) * (x - x0) / (x1 - x0))
                for y in range(top, H):
                    px[x, y] = col + (255,)

    G0 = GROUND
    ridge(G0 - 46, 22, (34, 38, 60), 5, 20)   # núi xa
    ridge(G0 - 30, 14, (26, 30, 46), 6, 12)   # núi gần
    # sông
    for y in range(G0 - 22, G0):
        for x in range(W):
            c = (30, 44, 70) if (x + y * 3) % 23 else (70, 96, 130)
            if y in (G0 - 22, G0 - 21):
                c = (60, 78, 104)
            px[x, y] = c + (255,)
    for _ in range(60):
        x, y = r.randrange(W), r.randrange(G0 - 19, G0 - 1)
        for i in range(r.randint(2, 5)):
            if x + i < W:
                px[x + i, y] = (110, 140, 170, 255)
    for x in range(316, 370):  # trăng in bóng nước
        y = G0 - 18 + (x * 7) % 14
        if (x // 3) % 2 == 0:
            px[x, y] = (200, 198, 176, 255)
    # bờ đất
    for y in range(G0, H):
        for x in range(W):
            t = (y - G0) / float(H - G0)
            base = mix((40, 36, 40), (58, 50, 50), t)
            if (x * 3 + y * 7) % 29 == 0:
                base = shade(base, 1.25)
            if (bay[y & 3][x & 3] / 16.0) < 0.12:
                base = shade(base, 0.85)
            px[x, y] = base + (255,)
    for y in range(G0, G0 + 5):
        for x in range(W):
            if (x + y) % 3:
                px[x, y] = (36, 52, 44, 255)
    # điện Thoải phủ ở xa, cắt bóng, cửa hắt ánh tím
    d = ImageDraw.Draw(img)
    ex, ey = 30, G0 - 70
    d.polygon([(ex - 10, ey + 22), (ex + 8, ey + 4), (ex + 92, ey + 4), (ex + 110, ey + 22)], fill=(20, 18, 28))
    d.polygon([(ex - 14, ey + 22), (ex - 10, ey + 16), (ex - 6, ey + 22)], fill=(20, 18, 28))
    d.polygon([(ex + 106, ey + 22), (ex + 110, ey + 16), (ex + 114, ey + 22)], fill=(20, 18, 28))
    d.rectangle((ex, ey + 22, ex + 100, ey + 46), fill=(28, 26, 36))
    d.rectangle((ex + 42, ey + 28, ex + 58, ey + 46), fill=(110, 70, 150))
    d.rectangle((ex + 45, ey + 31, ex + 55, ey + 46), fill=(150, 100, 190))
    for x in (ex + 8, ex + 28, ex + 70, ex + 90):
        d.rectangle((x, ey + 24, x + 2, ey + 46), fill=(70, 22, 26))
    d.rectangle((ex - 8, ey + 46, ex + 108, ey + 50), fill=(36, 34, 44))
    # cây chết hai bên
    for tx, h, sd in ((14, 56, 1), (200, 42, 2), (432, 60, 3)):
        rr = random.Random(sd)
        d.line((tx, G0 + 6, tx, G0 + 6 - h), fill=(18, 16, 22), width=3)
        for k in range(5):
            y0 = G0 + 6 - h + k * 9
            dx = rr.choice((-1, 1)) * rr.randint(8, 16)
            d.line((tx, y0, tx + dx, y0 - rr.randint(4, 10)), fill=(18, 16, 22), width=1)
    # sương tím trôi là là mặt đất
    nz = random.Random(9)
    for _ in range(24):
        cx2, cy2 = nz.randrange(W), nz.randrange(G0 - 6, G0 + 26)
        rx, ry = nz.randint(20, 46), nz.randint(3, 6)
        for y in range(cy2 - ry, cy2 + ry + 1):
            for x in range(cx2 - rx, cx2 + rx + 1):
                if 0 <= x < W and 0 <= y < H and ((x - cx2) / rx) ** 2 + ((y - cy2) / ry) ** 2 <= 1:
                    if (bay[y & 3][x & 3] / 16.0) < 0.5:
                        px[x, y] = mix(px[x, y][:3], (120, 104, 150), 0.35) + (255,)
    # cỏ bờ
    for _ in range(220):
        x, y = r.randrange(W), r.randrange(G0 + 6, H)
        for k in range(r.randint(2, 4)):
            if y - k >= 0:
                px[x, y - k] = (40, 62, 48, 255) if k else (30, 44, 36, 255)
    img.save(os.path.join(OUT, "backdrop.png"))
    return img


# ---------- Icon 9x9 ----------

def icons():
    def ic(name, pts, col, dark=None):
        s = S(9, 9)
        for (x, y) in pts:
            s.p(x, y, col)
        if dark:
            for (x, y) in dark:
                s.p(x, y, shade(col, 0.7))
        s.outline((20, 14, 16))
        s.save("icon_" + name)

    # kiếm: đánh 1 người
    ic("single", [(7, 0), (8, 0), (6, 1), (7, 1), (5, 2), (6, 2), (4, 3), (5, 3), (3, 4), (4, 4), (1, 5), (2, 5), (3, 5),
                  (2, 6), (1, 7), (2, 3)], (226, 226, 236), dark=[(2, 6), (1, 7)])
    # sóng: đánh cả đội
    ic("all", [(0, 4), (1, 3), (2, 3), (3, 4), (4, 5), (5, 5), (6, 4), (7, 3), (8, 3), (0, 7), (1, 6), (2, 6), (3, 7),
               (4, 8), (5, 8), (6, 7), (7, 6), (8, 6), (1, 1), (2, 0), (3, 1)], (120, 190, 230))
    # mặt ma: dọa (Âm khí)
    ic("terrify", [(x, y) for y in range(1, 8) for x in range(1, 8) if (x - 4) ** 2 + (y - 4) ** 2 <= 10 and not
                   ((x, y) in ((3, 3), (5, 3), (3, 4), (5, 4), (4, 6)))], (190, 150, 230))
    ic("heart", [(1, 1), (2, 1), (5, 1), (6, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2),
                 (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4),
                 (6, 4), (2, 5), (3, 5), (4, 5), (5, 5), (3, 6), (4, 6)], (220, 60, 60), dark=[(5, 4), (6, 3), (4, 5)])
    ic("mana", [(4, 0), (3, 1), (4, 1), (3, 2), (4, 2), (5, 2), (2, 3), (3, 3), (4, 3), (5, 3), (2, 4), (3, 4), (4, 4),
                (5, 4), (6, 4), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (3, 6), (4, 6), (5, 6)], (90, 150, 240),
       dark=[(5, 5), (6, 4), (5, 6)])
    ic("rage", [(4, 0), (3, 1), (4, 1), (2, 2), (3, 2), (4, 2), (6, 2), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (1, 4),
                (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (2, 6), (3, 6),
                (4, 6), (5, 6)], (240, 140, 40), dark=[(5, 5), (5, 6), (6, 5)])
    ic("amkhi", [(3, 1), (4, 1), (5, 1), (2, 2), (6, 2), (2, 3), (4, 3), (5, 3), (6, 3), (2, 4), (4, 4), (6, 5), (3, 5),
                 (4, 6), (5, 6), (2, 6), (6, 4)], (170, 110, 220))
    ic("shield", [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2),
                  (7, 2), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4),
                  (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (3, 6), (4, 6), (5, 6), (4, 7)], (150, 180, 210),
       dark=[(5, 4), (6, 3), (5, 5), (6, 4), (5, 6), (7, 2), (7, 3)])


if __name__ == "__main__":
    sheet = []
    for name, fn in (("ma_doi", ma_doi), ("ma_nuoc", ma_nuoc), ("ma_nhen", ma_nhen)):
        for f in (0, 1):
            sheet.append(fn(f).save("%s_%d" % (name, f)))
    bd = backdrop()
    icons()
    # xem trước đúng bố cục trong game ở 1920x1080: khung 384x216, mỗi pixel x5 (khớp BattleController.SlotPos)
    vw, vh = 384, 216
    gy = round(vh * 0.64)
    view = Image.new("RGBA", (vw, vh), (18, 18, 30, 255))
    view.alpha_composite(bd, ((vw - bd.width) // 2, gy - 10 - GROUND))
    walk = os.path.join(ASSETS, "Resources", "Walk")
    cx = vw // 2
    for i, n in enumerate(("vy", "tuan", "khoa")):
        p = os.path.join(walk, n + "_right_0.png")
        back = 2 - i
        x, y = cx - 42 - back * 30, gy + (back % 2) * 8
        if os.path.exists(p):
            im2 = Image.open(p); view.alpha_composite(im2, (x - im2.width // 2, y - im2.height + 1))
    for i, im in enumerate(sheet[::2][:2]):
        x, y = cx + 42 + i * 36, gy + (i % 2) * 8
        view.alpha_composite(im, (x - im.width // 2, y - im.height + 1))
    view.resize((vw * 5, vh * 5), Image.NEAREST).save(os.path.join(PREVIEW, "_battle_preview.png"))
    print("done →", OUT)
