"""Đồ họa trận: nền đêm Điện Thoải phủ và icon (ma lấy từ ảnh tham chiếu bằng extract_ref.py).
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
            im2 = Image.open(p)
            view.alpha_composite(im2, (x - im2.width // 2, y - im2.height + 1))
    for i, n in enumerate(("ma_doi", "ma_nuoc")):  # ma lấy từ extract_ref.py
        p = os.path.join(OUT, n + "_0.png")
        x, y = cx + 48 + i * 46, gy + (i % 2) * 8
        if os.path.exists(p):
            im = Image.open(p)
            view.alpha_composite(im, (x - im.width // 2, y - im.height + 1))
    view.resize((vw * 5, vh * 5), Image.NEAREST).save(os.path.join(PREVIEW, "_battle_preview.png"))
    print("done →", OUT)
