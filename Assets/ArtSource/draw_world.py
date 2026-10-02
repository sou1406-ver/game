"""Làng ban ngày kiểu Stardew: map 960x640 lớn hơn màn hình, đi lại bằng WASD.
Chạy: python draw_world.py → ghi thẳng vào Assets/Resources/World/
  ground.png     nền (cỏ, đất, nước, ruộng, bóng đổ)
  objects.png    atlas nhà, cây, đồ vật; vẽ theo thứ tự đáy (y) cùng người chơi
  water_0..2.png khung lấp lánh mặt nước
  world.json     vùng tương tác, cửa, ô ruộng, khói, bạn bè, chỗ thức dậy, vật thể, lưới va chạm
  crop_*, sun, lock, fog, cloud
Muốn dời một địa điểm: sửa SPOTS (vị trí sprite) và cửa (dx, dy) rồi chạy lại."""
from PIL import Image, ImageDraw, ImageFont
import json
import math
import os
import random

W, H = 960, 640
CELL = 4  # ô lưới va chạm
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
ASSETS = PARENT if os.path.basename(PARENT) == "Assets" else os.path.join(PARENT, "Assets")
OUT = os.path.join(ASSETS, "Resources", "World")
PREVIEW = os.path.join(HERE, "sprites")
os.makedirs(OUT, exist_ok=True)
os.makedirs(PREVIEW, exist_ok=True)

# ---------- Địa điểm (x y rộng cao = khung sprite; dx dy = chỗ đứng trước cửa để bấm E) ----------
# kind: home · field · dinh · npc · shrine (đi đêm) · locked (điện chưa mở)
SPOTS = [
    dict(id="nha", name="Nhà", kind="home", x=96, y=392, w=88, h=68, dx=152, dy=470),
    dict(id="ruong", name="Ruộng", kind="field", x=214, y=404, w=186, h=122, dx=307, dy=465),
    dict(id="dinh", name="Đình làng", kind="dinh", x=330, y=136, w=140, h=96, dx=400, dy=244),
    dict(id="ong_lang", name="Nhà Ông lang", kind="npc", npc="Ông lang", x=80, y=150, w=76, h=62, dx=118, dy=222),
    dict(id="ba_dong", name="Nhà Bà đồng", kind="npc", npc="Bà đồng", x=530, y=236, w=76, h=62, dx=568, dy=308),
    dict(id="thay_cung", name="Nhà Thầy cúng", kind="npc", npc="Thầy cúng", x=468, y=396, w=76, h=62, dx=506, dy=468),
    dict(id="quan_nuoc", name="Quán nước", kind="npc", npc="Cô hàng nước", x=640, y=362, w=70, h=48, dx=675, dy=420),
    dict(id="dien_thoai", name="Điện Thoải phủ", kind="shrine", x=600, y=120, w=96, h=78, dx=648, dy=212),
    dict(id="dien_nhac", name="Điện Nhạc phủ", kind="locked", x=330, y=6, w=96, h=78, dx=378, dy=114),
    dict(id="dien_thien", name="Điện Thiên phủ", kind="locked", x=840, y=24, w=96, h=78, dx=880, dy=184),
    dict(id="dien_dia", name="Điện Địa phủ", kind="locked", x=830, y=470, w=96, h=78, dx=868, dy=410),
]
SPOT = {s["id"]: s for s in SPOTS}

PLOTS = [dict(x=220, y=410, w=84, h=52), dict(x=310, y=410, w=84, h=52),
         dict(x=220, y=468, w=84, h=52), dict(x=310, y=468, w=84, h=52)]
SMOKE = [dict(x=106, y=400)]
SPAWN = dict(x=152, y=482)
# Chỗ 5 người đứng ở sân nhà khi không đi cùng (người đang dẫn thì không đứng đây). Vị trí tự đặt.
FRIENDS = [dict(name="Minh", x=72, y=478), dict(name="Vy", x=104, y=500), dict(name="Lan", x=196, y=500),
           dict(name="Tuấn", x=132, y=516), dict(name="Khoa", x=176, y=478)]

RIVER = [(810, -16, 16), (790, 60, 17), (772, 150, 18), (770, 250, 18), (786, 336, 19), (760, 430, 20),
         (712, 520, 20), (690, 600, 21), (684, 664, 21)]
ROAD_Y = 340

# ---------- Bảng màu ----------
OUTL = (34, 26, 28)
G = [(58, 84, 46), (76, 106, 54), (98, 128, 62), (128, 152, 74)]
D = [(108, 80, 56), (146, 114, 78), (174, 142, 98), (200, 172, 122)]
WT = [(38, 70, 96), (52, 94, 120), (72, 124, 146), (146, 194, 204), (204, 230, 228)]
R = [(84, 36, 32), (126, 52, 40), (160, 72, 50), (192, 102, 66)]
P = [(140, 116, 88), (186, 162, 122), (212, 192, 150)]
K = [(56, 36, 26), (90, 58, 38), (124, 84, 54)]
ST = [(86, 84, 82), (126, 122, 114), (166, 162, 150)]
L = [(34, 56, 38), (52, 82, 46), (76, 110, 56), (108, 140, 68)]
LD = [(28, 46, 34), (42, 68, 42), (62, 94, 50), (88, 120, 60)]
BB = [(94, 112, 54), (134, 152, 72), (170, 184, 98)]
GOLD = (214, 176, 72)
LACQ = [(112, 30, 30), (148, 42, 38)]
LEAF_OUT = (26, 40, 28)


def c4(c, a=255):
    return (c[0], c[1], c[2], a)


def shade(c, f):
    return (max(0, min(255, int(c[0] * f))), max(0, min(255, int(c[1] * f))), max(0, min(255, int(c[2] * f))))


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def make_noise(cell, seed):
    r = random.Random(seed)
    gw, gh = W // cell + 3, H // cell + 3
    g = [[r.random() for _ in range(gw)] for _ in range(gh)]

    def f(x, y):
        gx, gy = x / cell, y / cell
        x0, y0 = int(math.floor(gx)), int(math.floor(gy))
        tx, ty = gx - x0, gy - y0
        tx, ty = tx * tx * (3 - 2 * tx), ty * ty * (3 - 2 * ty)
        x0 = max(0, min(gw - 2, x0))
        y0 = max(0, min(gh - 2, y0))
        a = g[y0][x0] + (g[y0][x0 + 1] - g[y0][x0]) * tx
        b = g[y0 + 1][x0] + (g[y0 + 1][x0 + 1] - g[y0 + 1][x0]) * tx
        return a + (b - a) * ty
    return f


rng = random.Random(11)


class Map:
    def __init__(self):
        self.img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
        self.px = self.img.load()

    def ok(self, x, y):
        return 0 <= x < W and 0 <= y < H

    def p(self, x, y, c):
        if self.ok(x, y):
            self.px[x, y] = c4(c)

    def get(self, x, y):
        return self.px[x, y][:3] if self.ok(x, y) else None

    def blend(self, x, y, c, a):
        if self.ok(x, y):
            self.px[x, y] = c4(mix(self.px[x, y][:3], c, a))


M = Map()
GRASS_SET = set(G)

# ---------- Lưới va chạm ----------
GW, GH = W // CELL, H // CELL
SOLID = [[False] * GW for _ in range(GH)]
FREE = [[False] * GW for _ in range(GH)]  # ép đi được (cầu)


def block(x0, y0, x1, y1, free=False):
    grid = FREE if free else SOLID
    for gy in range(max(0, int(y0) // CELL), min(GH, int(y1) // CELL + 1)):
        for gx in range(max(0, int(x0) // CELL), min(GW, int(x1) // CELL + 1)):
            grid[gy][gx] = True


class S:
    """Sprite có lề 3px để viền và để đầu đao, lá chìa ra ngoài."""
    PAD = 3

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.img = Image.new("RGBA", (w + 2 * self.PAD, h + 2 * self.PAD), (0, 0, 0, 0))
        self.px = self.img.load()

    def p(self, x, y, c):
        x, y = int(x) + self.PAD, int(y) + self.PAD
        if 0 <= x < self.img.width and 0 <= y < self.img.height:
            self.px[x, y] = c4(c) if len(c) == 3 else c

    def get(self, x, y):
        x, y = int(x) + self.PAD, int(y) + self.PAD
        if 0 <= x < self.img.width and 0 <= y < self.img.height:
            return self.px[x, y]
        return (0, 0, 0, 0)

    def rect(self, x0, y0, x1, y1, c):
        for y in range(int(y0), int(y1) + 1):
            for x in range(int(x0), int(x1) + 1):
                self.p(x, y, c)

    def darken(self, x0, y0, x1, y1, f):
        for y in range(int(y0), int(y1) + 1):
            for x in range(int(x0), int(x1) + 1):
                c = self.get(x, y)
                if c[3]:
                    self.p(x, y, shade(c, f))

    def ellipse(self, cx, cy, rx, ry, c):
        for y in range(int(cy - ry - 1), int(cy + ry + 2)):
            for x in range(int(cx - rx - 1), int(cx + rx + 2)):
                if ((x - cx) / (rx + 0.4)) ** 2 + ((y - cy) / (ry + 0.4)) ** 2 <= 1:
                    self.p(x, y, c)

    def outline(self, col=OUTL):
        src = self.img.copy().load()
        w, h = self.img.size
        for y in range(h):
            for x in range(w):
                if src[x, y][3] == 0:
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h and src[nx, ny][3] > 0:
                            self.px[x, y] = c4(col)
                            break


def ground_shadow(cx, cy, rx, ry, a=0.32):
    for y in range(int(cy - ry - 1), int(cy + ry + 2)):
        for x in range(int(cx - rx - 1), int(cx + rx + 2)):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1:
                M.blend(x, y, (18, 24, 18), a)


def cast_shadow(s, x, y):
    sp = s.img.load()
    ox, oy = x - S.PAD, y - S.PAD
    for yy in range(s.img.height):
        for xx in range(s.img.width):
            if sp[xx, yy][3]:
                M.blend(ox + xx + 4, oy + yy + 3, (18, 24, 18), 0.22)


def catmull(pts, steps=24):
    out = []
    p = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(p) - 2):
        for s in range(steps):
            t = s / steps
            q = []
            for k in range(len(pts[0])):
                a, b, c, d = p[i - 1][k], p[i][k], p[i + 1][k], p[i + 2][k]
                q.append(0.5 * (2 * b + (-a + c) * t + (2 * a - 5 * b + 4 * c - d) * t * t
                                + (-a + 3 * b - 3 * c + d) * t * t * t))
            out.append(q)
    out.append(list(pts[-1]))
    return out


# ---------- Mặt đất ----------

def ground():
    n1, n2 = make_noise(52, 1), make_noise(14, 2)
    for y in range(H):
        for x in range(W):
            v = 0.65 * n1(x, y) + 0.35 * n2(x, y)
            M.px[x, y] = c4(G[2] if v > 0.62 else G[0] if v < 0.34 else G[1])


TUFTS = [[(0, 0), (-1, 1), (1, 1)], [(0, 0), (0, 1), (2, 0), (2, 1), (-1, 1)], [(0, 0), (1, -1), (2, 0)],
         [(0, 0), (0, -1), (1, 0)]]


def tufts_and_flowers():
    for _ in range(4200):
        x, y = rng.randrange(W), rng.randrange(H)
        base = M.get(x, y)
        if base not in GRASS_SET:
            continue
        i = G.index(base)
        c = G[min(3, i + 1)] if rng.random() < 0.7 or i == 0 else G[i - 1]
        for dx, dy in rng.choice(TUFTS):
            if M.get(x + dx, y + dy) in GRASS_SET:
                M.p(x + dx, y + dy, c)
    flowers = [(232, 226, 206), (226, 196, 84), (218, 150, 170), (176, 160, 214)]
    for _ in range(200):
        x, y = rng.randrange(W), rng.randrange(110, H)
        col = rng.choice(flowers)
        for _ in range(rng.randint(3, 6)):
            fx, fy = x + rng.randint(-4, 4), y + rng.randint(-3, 3)
            if M.get(fx, fy) in GRASS_SET:
                M.p(fx, fy, col)
                if M.get(fx, fy + 1) in GRASS_SET:
                    M.p(fx, fy + 1, G[0])


DIRT = [[0.0] * W for _ in range(H)]


def soft(cx, cy, rx, ry, val=1.0):
    for y in range(int(cy - ry * 1.4) - 1, int(cy + ry * 1.4) + 2):
        if not 0 <= y < H:
            continue
        row = DIRT[y]
        for x in range(int(cx - rx * 1.4) - 1, int(cx + rx * 1.4) + 2):
            if 0 <= x < W:
                d = math.sqrt(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2)
                v = val * (1 - d * 0.5)
                if v > row[x]:
                    row[x] = v


def road(pts, r):
    for x, y in catmull(pts, 16):
        soft(x, y, r, r)


def render_dirt():
    nz, nz2 = make_noise(5, 9), make_noise(17, 10)
    mask = [[False] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            mask[y][x] = DIRT[y][x] + (nz(x, y) - 0.5) * 0.24 > 0.5
    for y in range(H):
        for x in range(W):
            if not mask[y][x]:
                continue
            edge = any(not (0 <= x + dx < W and 0 <= y + dy < H and mask[y + dy][x + dx])
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if edge:
                c = D[0]
            elif DIRT[y][x] > 0.8 and nz2(x, y) > 0.45:
                c = D[2]
            else:
                c = D[1] if nz2(x, y) < 0.62 else D[2]
            M.p(x, y, c)
    for _ in range(2600):
        x, y = rng.randrange(W), rng.randrange(H)
        if mask[y][x] and M.get(x, y) != D[0]:
            M.p(x, y, D[3] if rng.random() < 0.6 else ST[1])
            if rng.random() < 0.4:
                M.p(x, y + 1, D[0])
    for _ in range(1400):
        x, y = rng.randrange(W), rng.randrange(H)
        if M.get(x, y) == D[0]:
            for dx, dy in rng.choice(TUFTS):
                M.p(x + dx, y + dy, G[2])


# ---------- Nước ----------

def water_depth_river():
    depth = {}
    for x, y, r in catmull(RIVER):
        for py in range(int(y - r - 1), int(y + r + 2)):
            for px in range(int(x - r - 1), int(x + r + 2)):
                d = r - math.hypot(px - x, py - y)
                if d >= 0 and depth.get((px, py), -1) < d:
                    depth[(px, py)] = d
    return depth


def water_depth_pond(cx, cy, rx, ry):
    depth = {}
    for y in range(cy - ry - 1, cy + ry + 2):
        for x in range(cx - rx - 1, cx + rx + 2):
            e = ((x - cx) / (rx + 0.4)) ** 2 + ((y - cy) / (ry + 0.4)) ** 2
            if e <= 1:
                depth[(x, y)] = (1 - math.sqrt(e)) * ry
    return depth


def render_water(depth, bank_w, rocky):
    bank = set()
    for (x, y) in depth:
        for dy in range(-bank_w, bank_w + 1):
            for dx in range(-bank_w, bank_w + 1):
                q = (x + dx, y + dy)
                if q not in depth and dx * dx + dy * dy <= bank_w * bank_w:
                    bank.add(q)
    for (x, y) in bank:
        M.p(x, y, D[0] if (x * 3 + y * 5) % 7 else shade(D[0], 0.85))
    for q in list(bank):
        if rng.random() < rocky:
            x, y = q
            M.p(x, y, ST[2]); M.p(x + 1, y, ST[1]); M.p(x, y + 1, ST[0]); M.p(x + 1, y + 1, ST[0])
    for (x, y), d in depth.items():
        if M.ok(x, y):
            M.p(x, y, WT[2] if d < 1.3 else WT[1] if d < 5 else WT[0])
            if d >= 0:
                block(x, y, x, y)
    for (x, y), d in depth.items():
        if d < 1.3 and (x, y - 1) not in depth and (x + y) % 3:
            M.p(x, y, WT[4])
    items = list(depth.items())
    for _ in range(len(depth) // 90):
        (x, y), d = rng.choice(items)
        if d > 3:
            for i in range(rng.randint(2, 5)):
                if depth.get((x + i, y), 0) > 2:
                    M.p(x + i, y, WT[2] if i == 0 else WT[3])
    return bank


def reeds(bank, n, avoid):
    pts = list(bank)
    for _ in range(n):
        x, y = rng.choice(pts)
        if any(a <= x <= b and c <= y <= d for a, b, c, d in avoid):
            continue
        for i in range(rng.randint(2, 4)):
            rx = x + i * 2 - 2
            hgt = rng.randint(3, 6)
            for k in range(hgt):
                M.p(rx + (1 if k == hgt - 1 and i % 2 else 0), y - k, L[2] if k < hgt - 1 else (196, 178, 120))
            M.p(rx, y, L[1])


def water_frames(depths):
    allw = [(q, d) for dep in depths for q, d in dep.items() if d > 1.5 and M.ok(*q)]
    for f in range(3):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        px = img.load()
        r = random.Random(500 + f)
        for _ in range(len(allw) // 55):
            (x, y), d = r.choice(allw)
            ln = r.randint(1, 3)
            for i in range(ln):
                if 0 <= x + i < W:
                    px[x + i, y] = c4(WT[4] if i == ln // 2 else WT[3], 230)
        img.save(os.path.join(OUT, "water_%d.png" % f))


# ---------- Núi, sương ----------

def mountains():
    layers = [
        ([(150, 164, 166), (128, 144, 150), (108, 124, 134)],
         [(830, 92, 70, 80), (930, 86, 80, 84), (880, 70, 60, 60)]),
        ([(110, 128, 104), (90, 110, 88), (70, 90, 74)],
         [(816, 150, 60, 70), (888, 150, 170, 58), (956, 160, 70, 80)]),
    ]
    nz = make_noise(4, 21)
    for pal, peaks in layers:
        for cx, base, wid, hgt in peaks:
            half = wid / 2
            flat = cx == 888 and base == 150
            for x in range(int(cx - half), int(cx + half) + 1):
                t = (x - cx) / half
                if abs(t) > 1 or not 0 <= x < W:
                    continue
                tt = 0.5 if flat and abs(t) < 0.5 else abs(t)
                top = base - hgt * (1 - tt ** 2.2) ** 0.6
                for y in range(int(top), base + 30):
                    if not 0 <= y < H:
                        continue
                    c = pal[0] if t < -0.35 else pal[1] if t < 0.3 else pal[2]
                    if int(y - top) in (9, 21) or (int(y - top) % 13 == 5 and (x // 3) % 2):
                        c = shade(c, 0.86)
                    if y - top < 1.5:
                        c = shade(c, 1.12)
                    g = (y - top) / (base + 30 - top)
                    if nz(x, y) > 0.78 - g * 0.5:
                        c = L[1] if nz(x + 40, y) > 0.5 else L[2]
                    M.p(x, y, c)
                    block(x, y, x, y)


def mist_band(x0, x1, yc, thick, a, seed):
    nz = make_noise(9, seed)
    for y in range(int(yc - thick * 2), int(yc + thick * 2)):
        for x in range(x0, x1):
            v = 1 - abs(y - yc) / thick + (nz(x, y) - 0.5) * 1.3
            if v > 0.55:
                M.blend(x, y, (226, 232, 234), a)
            elif v > 0.3:
                M.blend(x, y, (226, 232, 234), a * 0.45)


# ---------- Cây cối ----------

def canopy(s, cx, cy, r, lr, pal):
    clumps = [(cx, cy, r * 0.62)]
    n = 8 if r < 12 else 16
    for i in range(n):
        a = 2 * math.pi * i / n + lr.uniform(-0.3, 0.3)
        dist = r * lr.uniform(0.42, 0.66)
        clumps.append((cx + math.cos(a) * dist, cy + math.sin(a) * dist * 0.85, r * lr.uniform(0.3, 0.42)))
    clumps.sort(key=lambda c: c[1])
    for x0, y0, rr in clumps:
        for y in range(int(y0 - rr - 1), int(y0 + rr + 2)):
            for x in range(int(x0 - rr - 1), int(x0 + rr + 2)):
                dx, dy = x - x0, y - y0
                if dx * dx + dy * dy <= rr * rr:
                    t = (dx + dy * 1.2) / rr
                    c = pal[3] if t < -0.95 else pal[2] if t < -0.15 else pal[1] if t < 0.8 else pal[0]
                    if y - cy > r * 0.5 and c in (pal[2], pal[3]):
                        c = pal[1]
                    s.p(x, y, c)
    for _ in range(int(r * 1.5)):
        x, y = cx + lr.uniform(-r * 0.7, r * 0.4), cy + lr.uniform(-r * 0.8, 0)
        if s.get(x, y)[3] and s.get(x, y)[:3] == pal[2]:
            s.p(x, y, pal[3])


def tree(r, seed, pal=L, trunk=True):
    lr = random.Random(seed)
    th = max(6, r // 2 + 4)  # thân lộ dưới tán
    s = S(2 * r + 2, 2 * r + th)
    if trunk:
        tx = r + 1
        s.rect(tx - 1, int(r * 1.4), tx + 1, 2 * r + th - 1, c4(K[1]))
        s.rect(tx + 1, int(r * 1.4), tx + 1, 2 * r + th - 1, c4(K[0]))
        s.p(tx - 2, 2 * r + th - 1, K[1]); s.p(tx + 2, 2 * r + th - 1, K[0])
    canopy(s, r + 1, r + 1, r + 1, lr, pal)
    return s


def banyan():
    lr = random.Random(5)
    s = S(60, 64)
    s.rect(25, 30, 34, 63, c4(K[1])); s.rect(31, 30, 34, 63, c4(K[0])); s.rect(26, 30, 26, 63, c4(K[2]))
    for x in (19, 22, 38, 41):
        for y in range(34, 60):
            if (x * 7 + y) % 6:
                s.p(x, y, K[0] if x > 28 else K[1])
    s.rect(19, 61, 40, 63, c4(K[1]))
    canopy(s, 30, 24, 28, lr, [(32, 54, 38), (46, 76, 44), (68, 102, 52), (98, 132, 64)])
    return s


def banana(seed):
    lr = random.Random(seed)
    s = S(28, 30)
    s.rect(13, 13, 14, 29, (112, 128, 70)); s.rect(14, 13, 14, 29, (90, 104, 58))
    for ang in (-100, -135, -60, -165, -15, -150, -35):
        a = math.radians(ang + lr.uniform(-6, 6))
        ln = lr.randint(11, 13)
        for i in range(ln):
            px, py = 14 + math.cos(a) * i, 12 + math.sin(a) * i + (i * i) / 13.0
            wdt = 2.6 * math.sin(math.pi * (i + 1.5) / (ln + 1.5))
            nx, ny = -math.sin(a), math.cos(a)
            for k in range(-int(wdt + 0.5), int(wdt + 0.5) + 1):
                if not (i > 3 and (i + k) % 4 == 0 and abs(k) >= 2):
                    s.p(px + nx * k, py + ny * k, L[3] if k < 0 else L[2] if k < 2 else L[1])
            s.p(px, py, (156, 176, 96))
    return s


def areca(seed):
    s = S(15, 36)
    for y in range(7, 36):
        s.p(7, y, (160, 146, 112) if y % 4 else (120, 108, 84)); s.p(8, y, (128, 116, 90))
    for dx, dy in ((-7, 4), (-6, 1), (-4, -2), (-1, -3), (2, -3), (5, -1), (7, 2), (7, 5), (-7, 6)):
        steps = max(abs(dx), abs(dy))
        for i in range(steps + 1):
            x, y = 7 + round(dx * i / steps), 6 + round(dy * i / steps) + (1 if i > steps * 0.7 else 0)
            s.p(x, y, L[3] if dx < 0 else L[2])
            if i > 1 and i % 2 == 0:
                s.p(x, y + 1, L[1])
    s.p(6, 8, (210, 130, 50)); s.p(8, 8, (190, 108, 40)); s.p(7, 9, (190, 108, 40))
    return s


def bamboo(seed, h=42):
    lr = random.Random(seed)
    w = 28
    s = S(w, h)
    bx = w // 2
    stalks = []
    for i in range(8):
        lean = (i - 3.5) * lr.uniform(1.6, 2.6)
        top = lr.randint(1, 10)
        stalks.append((lean, top))
        for y in range(h - 1, top - 1, -1):
            t = (h - 1 - y) / (h - 1 - top)
            x = bx + (i - 3.5) * 1.6 + lean * t * t
            s.p(x, y, BB[0] if (h - y) % 6 == 0 else BB[1] if lean < 0 else shade(BB[1], 0.82))
    for lean, top in stalks:
        for y in range(top, int(top + (h - top) * 0.86)):
            t = (h - 1 - y) / (h - 1 - top)
            x = bx + lean * t * t
            for _ in range(3):
                dirx = 1 if lr.random() < 0.5 + lean * 0.06 else -1
                up = (y - top) / (h - top)
                c = L[3] if (dirx < 0 and up < 0.4 and lr.random() < 0.6) else lr.choice([L[1], L[2], L[2], L[1], L[0]])
                for k in range(lr.randint(2, 4)):
                    s.p(x + dirx * (k + 1), y + k // 2 + 1, c)
    return s


# ---------- Nhà cửa ----------

def tile_roof(s, x0, x1, y0, y1, inset, pal=R, curl=False, ridge=True):
    h = y1 - y0 + 1
    for yy in range(h):
        t = yy / max(1, h - 1)
        ins = round((1 - t) * inset)
        a, b = x0 + ins, x1 - ins
        row = yy % 3
        for x in range(a, b + 1):
            if row == 2:
                c = pal[0] if x % 3 == 0 else pal[1]
            elif row == 0:
                c = pal[3] if x % 3 == 1 else pal[2]
            else:
                c = pal[1] if x % 3 == 0 else pal[2]
            if x > a + (b - a) * 0.66:
                c = shade(c, 0.84)
            s.p(x, y0 + yy, c)
        s.p(a, y0 + yy, pal[3]); s.p(b, y0 + yy, pal[0])
    s.rect(x0, y1 + 1, x1, y1 + 1, pal[0])
    if ridge:
        s.rect(x0 + inset - 1, y0 - 2, x1 - inset + 1, y0 - 2, shade(pal[0], 0.9))
        s.rect(x0 + inset - 1, y0 - 1, x1 - inset + 1, y0 - 1, pal[1])
        for ex, d in ((x0 + inset - 1, -1), (x1 - inset + 1, 1)):
            s.p(ex + d, y0 - 2, pal[1]); s.p(ex + d, y0 - 3, pal[0])
    if curl:
        for dx, dy in ((-1, 0), (-2, -1), (-3, -2), (-3, -3), (-2, -4)):
            s.p(x0 + dx, y1 + 1 + dy, pal[0]); s.p(x1 - dx, y1 + 1 + dy, pal[0])
        s.p(x0 - 1, y1 - 3, pal[2]); s.p(x1 + 1, y1 - 3, pal[1])


def roof_damage(s, x0, x1, y0, y1, n, seed):
    lr = random.Random(seed)
    for _ in range(n):
        hx, hy = lr.randint(x0 + 4, x1 - 8), lr.randint(y0 + 2, y1 - 4)
        w = lr.randint(2, 4)
        s.rect(hx, hy, hx + w, hy + 1, K[0]); s.p(hx + 1, hy + 1, K[1])
        for k in range(lr.randint(2, 4)):
            s.p(hx + lr.randint(-2, w + 2), hy + lr.randint(-1, 3), lr.choice([L[1], L[2]]))
    for _ in range(n * 2):
        s.p(lr.randint(x0 + 2, x1 - 2), y1 - lr.randint(0, 2), L[2])


def facade(s, x0, x1, y0, y1, pal=P, cols=10, door_w=10, lacquer=False, windows=True):
    s.rect(x0, y0, x1, y1, pal[1])
    s.darken(x0 + round((x1 - x0) * 0.66), y0, x1, y1, 0.86)
    colc = LACQ if lacquer else (K[1], K[2])
    for x in range(x0, x1 + 1, cols):
        s.rect(x, y0, x + 1, y1, colc[0]); s.rect(x, y0 + 1, x, y1, colc[1])
    cx = (x0 + x1) // 2
    s.rect(cx - door_w // 2, y0 + 2, cx + door_w // 2 - 1, y1, K[2])
    for x in range(cx - door_w // 2, cx + door_w // 2, 2):
        s.rect(x, y0 + 2, x, y1, K[1])
    s.rect(cx - 2, y0 + 3, cx + 1, y1, K[0])
    if windows:
        for wx in (x0 + 3, x1 - 9):
            if abs(wx - cx) > door_w // 2 + 4:
                s.rect(wx, y0 + 4, wx + 6, y0 + 8, K[0])
                for k in range(wx, wx + 7, 2):
                    s.rect(k, y0 + 4, k, y0 + 8, K[2])
    s.darken(x0, y0, x1, y0 + 1, 0.6)


def plinth(s, x0, x1, y0, steps=True):
    s.rect(x0, y0, x1, y0 + 1, ST[1]); s.rect(x0, y0 + 2, x1, y0 + 2, ST[0])
    if steps:
        cx = (x0 + x1) // 2
        s.rect(cx - 6, y0 + 2, cx + 5, y0 + 3, ST[2]); s.rect(cx - 6, y0 + 4, cx + 5, y0 + 4, ST[0])


def house(w, h, pal=R, wall=P):
    s = S(w, h)
    rh = round(h * 0.56)
    tile_roof(s, 0, w - 1, 3, rh, 6, pal)
    facade(s, 3, w - 4, rh + 2, h - 6, wall, cols=12, door_w=12)
    plinth(s, 2, w - 3, h - 5)
    return s


def jar(s, x, y, big=False):
    rx, ry = (3, 3) if big else (2, 2)
    s.ellipse(x, y, rx, ry, (150, 104, 66)); s.ellipse(x - 1, y - 1, rx - 1, ry - 1, (176, 126, 80))
    s.rect(x - rx + 1, y - ry - 1, x + rx - 1, y - ry - 1, (100, 70, 46))


def nha(w, h):
    s = S(w, h)
    kw = 20
    rh = round(h * 0.56)
    tile_roof(s, kw - 4, w - 1, 3, rh, 6)
    facade(s, kw - 1, w - 4, rh + 2, h - 6, cols=12, door_w=12)
    plinth(s, kw - 2, w - 3, h - 5)
    for yy in range(rh - 12):  # gian bếp mái rạ
        ins = round((1 - yy / (rh - 13)) * 3)
        for x in range(ins, kw - ins):
            c = (186, 152, 88) if (x * 2 + yy) % 4 else (150, 118, 64)
            s.p(x, 14 + yy, shade(c, 0.86) if x > kw - 7 else c)
    s.rect(0, rh + 1, kw - 1, rh + 1, (120, 92, 54))
    s.rect(1, rh + 2, kw - 2, h - 5, (120, 96, 66))
    s.rect(5, rh + 7, 12, h - 5, (40, 30, 26))
    s.p(8, h - 9, (220, 120, 50)); s.p(7, h - 8, (200, 80, 40)); s.p(9, h - 8, (240, 160, 60))
    jar(s, w - 6, h - 3, True); jar(s, w - 13, h - 2)
    return s


def nha_thay_cung(w, h):
    s = house(w, h, pal=[(76, 32, 30), (114, 46, 38), (146, 62, 46), (176, 90, 60)])
    rh = round(h * 0.56)
    for x in (15, w - 17):
        s.rect(x, rh + 6, x + 1, rh + 14, GOLD); s.p(x, rh + 8, (190, 40, 40)); s.p(x + 1, rh + 11, (190, 40, 40))
    s.rect(w // 2 - 3, h - 4, w // 2 + 2, h - 2, (120, 96, 60))
    s.p(w // 2 - 1, h - 5, (220, 210, 190)); s.p(w // 2, h - 7, (200, 200, 190))
    return s


def nha_ba_dong(w, h):
    s = house(w, h)
    rh = round(h * 0.56)
    for x in range(6, w - 6):
        s.p(x, rh + 2, (196, 44, 44) if (x // 3) % 2 else GOLD)
    for x in (8, w - 10):
        s.rect(x, rh + 3, x + 1, rh + 11, (196, 44, 44))
    s.ellipse(w - 6, h - 4, 2, 2, (230, 200, 220)); s.p(w - 6, h - 5, (210, 80, 120))
    return s


def nha_ong_lang(w, h):
    s = house(w, h)
    for cx in (5, w - 6):
        s.ellipse(cx, h - 4, 5, 3, (178, 146, 92)); s.ellipse(cx, h - 4, 3, 2, (104, 126, 64))
        s.p(cx - 1, h - 5, (140, 160, 80))
    s.rect(w // 2 + 10, h - 4, w // 2 + 13, h - 2, (110, 100, 90)); s.p(w // 2 + 11, h - 5, (140, 130, 120))
    return s


def quan_nuoc(w, h):
    s = S(w, h)
    straw = [(140, 106, 56), (172, 138, 74), (200, 168, 100)]
    th = round(h * 0.46)
    for yy in range(th):
        ins = round((1 - yy / (th - 1)) * 6)
        for x in range(ins, w - ins):
            c = straw[2] if (x + yy // 2) % 4 == 0 else straw[1]
            if yy % 4 == 3:
                c = straw[0]
            if x > w * 0.66:
                c = shade(c, 0.85)
            s.p(x, 2 + yy, c)
    s.rect(0, th + 2, w - 1, th + 2, straw[0])
    s.rect(5, th + 3, w - 6, h - 7, (54, 42, 34))
    for x in (5, w - 6):
        s.rect(x, th + 3, x, h - 2, BB[1])
    by = h - 10
    s.rect(11, by, w - 12, by + 1, (138, 100, 62))
    s.rect(11, by + 2, 11, h - 4, K[1]); s.rect(w - 12, by + 2, w - 12, h - 4, K[1])
    cx = w // 2
    s.rect(cx - 2, by - 3, cx + 1, by - 1, (200, 200, 190)); s.p(cx + 2, by - 2, (200, 200, 190)); s.p(cx - 1, by - 4, (160, 160, 150))
    for x in (16, cx + 8, cx + 12):
        s.rect(x, by - 2, x + 1, by - 1, (228, 226, 214))
    s.rect(w - 16, th + 3, w - 12, th + 7, (222, 196, 72)); s.rect(w - 15, th + 8, w - 13, th + 8, (190, 160, 60))
    jar(s, w - 4, h - 3)
    return s


def dinh(w, h):
    s = S(w, h)
    pal = [(78, 36, 32), (116, 52, 40), (146, 68, 48), (176, 96, 64)]
    tile_roof(s, 30, w - 31, 4, 26, 6, pal, curl=True)
    s.rect(w // 2 - 2, 0, w // 2 + 1, 2, GOLD); s.p(w // 2 - 3, 1, GOLD); s.p(w // 2 + 2, 1, GOLD)
    s.rect(30, 28, w - 31, 29, (40, 28, 26))
    tile_roof(s, 2, w - 3, 30, 58, 14, pal, curl=True, ridge=False)
    roof_damage(s, 2, w - 3, 30, 58, 7, 12)
    roof_damage(s, 30, w - 31, 4, 26, 3, 13)
    s.rect(6, 60, w - 7, 80, (38, 28, 26))
    s.rect(w // 2 - 8, 66, w // 2 + 7, 72, (120, 30, 30)); s.rect(w // 2 - 6, 65, w // 2 + 5, 65, GOLD)
    s.p(w // 2 - 1, 64, GOLD)
    for i, x in enumerate(range(7, w - 6, 12)):
        faded = i in (2, 8)
        c0, c1 = ((112, 92, 78), (140, 118, 100)) if faded else LACQ
        s.rect(x, 60, x + 1, 80, c0); s.rect(x, 60, x, 80, c1)
    s.darken(6, 60, w - 7, 61, 0.6)
    s.rect(0, 81, w - 1, 85, ST[1]); s.rect(0, 85, w - 1, 85, ST[0])
    for k, half in enumerate((20, 17, 14)):
        y = 86 + k * 3
        s.rect(w // 2 - half, y, w // 2 + half - 1, y + 1, ST[2]); s.rect(w // 2 - half, y + 2, w // 2 + half - 1, y + 2, ST[0])
    for x in (14, 52, 96, 124):
        s.p(x, 82, L[2]); s.p(x + 1, 81, L[3])
    return s


def courtyard(x0, y0, x1, y1):
    nz = make_noise(6, 33)
    for y in range(y0, y1):
        for x in range(x0, x1):
            row = (y - y0) // 3
            if (y - y0) % 3 == 2 or (x - x0 + (row % 2) * 3) % 6 == 0:
                c = (118, 78, 62)
            else:
                c = (166, 108, 82) if (x // 6 + row) % 3 else (152, 98, 76)
            if nz(x, y) > 0.7:
                c = G[1] if nz(x, y) > 0.78 else (128, 92, 72)
            M.p(x, y, c)
    for x in range(x0 - 1, x1 + 1):
        M.p(x, y0 - 1, ST[1]); M.p(x, y1, ST[0])
    for y in range(y0, y1):
        M.p(x0 - 1, y, ST[1]); M.p(x1, y, ST[0])


def pillar():
    s = S(6, 26)
    s.rect(1, 4, 4, 25, ST[2]); s.rect(4, 4, 4, 25, ST[1])
    s.rect(0, 2, 5, 3, ST[1]); s.rect(1, 0, 4, 1, ST[2]); s.rect(0, 23, 5, 25, ST[1])
    s.p(2, 9, (120, 110, 100)); s.p(2, 14, (120, 110, 100))
    return s


def dien(w, h, accent, wall, pal, seed, corrupt=False):
    s = S(w, h)
    tile_roof(s, 2, w - 3, 4, 32, 9, pal, curl=True)
    s.rect(w // 2 - 1, 0, w // 2, 2, accent)
    roof_damage(s, 2, w - 3, 4, 32, 4, seed)
    facade(s, 7, w - 8, 34, 54, [shade(wall, 0.8), wall, shade(wall, 1.1)], cols=14, door_w=16, lacquer=True)
    s.rect(w // 2 - 7, 34, w // 2 + 6, 35, accent); s.p(w // 2 - 8, 35, accent); s.p(w // 2 + 7, 35, accent)
    plinth(s, 5, w - 6, 55, steps=False)
    s.rect(0, 63, w - 1, 69, shade(wall, 0.92)); s.rect(0, 63, w - 1, 63, shade(wall, 1.1)); s.rect(0, 69, w - 1, 69, shade(wall, 0.7))
    s.rect(w // 2 - 9, 62, w // 2 + 8, 70, (0, 0, 0, 0))
    for x in (w // 2 - 11, w // 2 + 9):
        s.rect(x, 58, x + 2, 72, shade(wall, 0.85)); s.rect(x - 1, 57, x + 3, 57, pal[1])
    s.rect(w // 2 - 3, 59, w // 2 + 2, 62, (150, 112, 60)); s.rect(w // 2 - 4, 59, w // 2 + 3, 59, (176, 136, 76))
    lr = random.Random(seed)
    for _ in range(14):
        x, y = lr.randint(1, w - 2), lr.randint(58, 70)
        if s.get(x, y)[3]:
            s.p(x, y, lr.choice([L[2], L[3]]))
    if corrupt:
        vine, glow = (30, 22, 36), (140, 80, 170)
        for sx, top, drift, thick in ((4, 8, 1, 2), (18, 2, -1, 1), (70, 4, 1, 1), (90, 12, -1, 2), (40, 16, 1, 1),
                                      (58, 22, -1, 1)):
            x = sx
            for y in range(72, top, -1):
                if lr.random() < 0.35:
                    x += drift if lr.random() < 0.7 else -drift
                for k in range(thick):
                    s.p(x + k, y, vine)
                if lr.random() < 0.1:
                    s.p(x + lr.choice((-2, -1, 2, 3)), y, vine)
        for x, y in ((20, 8), (66, 13), (42, 25), (12, 44), (82, 40), (54, 60)):
            s.p(x, y, glow)
        for y in range(37, 52):
            s.p(26 + (y % 3 == 0), y, shade(wall, 0.55))
    return s


def dead_tree():
    s = S(18, 30)
    c, c2 = (70, 58, 54), (52, 42, 40)
    s.rect(8, 8, 9, 29, c); s.rect(9, 8, 9, 29, c2)
    for x0, y0, dx in ((8, 14, -1), (9, 10, 1), (8, 7, -1), (9, 17, 1), (8, 4, 1)):
        x, y = x0, y0
        for i in range(6):
            x += dx
            y -= 1 if i % 2 else 0
            s.p(x, y, c)
    s.rect(6, 28, 11, 29, c2)
    return s


def boat():
    s = S(24, 10)
    s.rect(2, 6, 21, 8, K[1]); s.rect(2, 6, 21, 6, K[2]); s.rect(0, 4, 1, 6, K[1]); s.rect(22, 4, 23, 6, K[1])
    s.rect(8, 0, 15, 5, (64, 58, 48)); s.rect(8, 0, 15, 0, (96, 88, 70))
    return s


def gate():
    s = S(30, 34)
    tile_roof(s, 0, 29, 3, 11, 2, curl=True)
    s.rect(2, 13, 7, 33, ST[2]); s.rect(6, 13, 7, 33, ST[1]); s.rect(22, 13, 27, 33, ST[1])
    s.rect(2, 13, 27, 15, ST[2]); s.rect(2, 16, 27, 16, ST[0]); s.rect(10, 13, 19, 14, (120, 30, 30))
    return s


def haystack():
    s = S(18, 18)
    for y in range(18):
        half = int(8 * math.sin(math.pi * min(1, (y + 3) / 20.0)))
        for x in range(9 - half, 9 + half + 1):
            c = (206, 176, 96) if x < 10 else (172, 142, 74)
            if (x + y * 2) % 5 == 0:
                c = shade(c, 0.85)
            s.p(x, y, c)
    s.rect(8, 0, 9, 2, K[1])
    return s


def well():
    s = S(16, 14)
    s.ellipse(8, 7, 7, 5, ST[1]); s.ellipse(8, 7, 5, 3, WT[0]); s.p(6, 6, WT[2])
    s.rect(1, 10, 15, 13, ST[1]); s.rect(1, 13, 15, 13, ST[0])
    return s


def firewood():
    s = S(14, 7)
    for y in range(0, 7, 2):
        s.rect(y // 2, y, 13 - y // 2, y + 1, K[2])
        for x in range(y // 2, 14 - y // 2, 3):
            s.p(x, y, (190, 150, 100))
    return s


def scarecrow():
    s = S(14, 22)
    s.rect(6, 5, 7, 21, K[1]); s.rect(0, 9, 13, 10, (150, 120, 70)); s.rect(3, 9, 10, 15, (110, 120, 150))
    s.ellipse(6.5, 4, 4, 2, (220, 200, 130)); s.rect(1, 5, 12, 5, (200, 176, 110))
    return s


def fence(length):
    s = S(length, 7)
    for x in range(0, length, 2):
        s.rect(x, 0, x, 6, BB[1] if x % 4 else BB[0])
    s.rect(0, 2, length - 1, 2, K[2])
    return s


# ---------- Ruộng ----------

def field():
    s = SPOT["ruong"]
    for y in range(s["y"], s["y"] + s["h"]):
        for x in range(s["x"], s["x"] + s["w"]):
            M.p(x, y, G[2] if (x * 7 + y * 3) % 11 else G[3])
    for pl in PLOTS:
        for y in range(pl["y"], pl["y"] + pl["h"]):
            for x in range(pl["x"], pl["x"] + pl["w"]):
                r = (y - pl["y"]) % 4
                M.p(x, y, (132, 98, 66) if r == 0 else (112, 82, 56) if r == 1 else (96, 70, 48) if r == 2 else (78, 56, 40))
        for x in range(pl["x"] - 1, pl["x"] + pl["w"] + 1):
            M.p(x, pl["y"] - 1, (66, 48, 34)); M.p(x, pl["y"] + pl["h"], G[1])


def paddies():
    polys = [
        [(806, 196), (870, 190), (874, 236), (810, 242)],
        [(876, 190), (946, 186), (950, 230), (878, 236)],
        [(812, 248), (874, 242), (878, 290), (816, 296)],
        [(880, 242), (950, 236), (954, 284), (882, 290)],
    ]
    ripe = {1, 2}
    for i, poly in enumerate(polys):
        img = Image.new("L", (W, H), 0)
        ImageDraw.Draw(img).polygon(poly, fill=255)
        mp = img.load()
        xs, ys = [p[0] for p in poly], [p[1] for p in poly]
        for y in range(min(ys), max(ys) + 1):
            for x in range(min(xs), max(xs) + 1):
                if not mp[x, y]:
                    continue
                inner = mp[x - 2, y] and mp[x + 2, y] and mp[x, y - 2] and mp[x, y + 2]
                if not inner:
                    c = (120, 132, 74) if mp[x, y - 2] else (140, 150, 86)
                elif i in ripe:
                    c = (206, 178, 92) if (y % 3 == 0 and x % 2 == 0) else (176, 150, 72) if y % 3 != 2 else (140, 118, 58)
                else:
                    c = (110, 146, 70) if (y % 3 == 0 and x % 2 == 0) else (80, 116, 60) if y % 3 != 2 else (70, 104, 92)
                    if y % 3 == 2 and (x * 5 + y) % 9 == 0:
                        c = (150, 186, 180)
                M.p(x, y, c)
                if inner:
                    block(x, y, x, y)  # ruộng nước: không lội vào


# ---------- Atlas vật thể ----------

OBJS = []  # dict(sprite, x, y, fade)


def add(sp, x, y, outline=OUTL, solid=None, fade=True, shadow=None, cast=True):
    """x, y: góc trên trái phần nội dung. solid: (x0, y0, x1, y1) toạ độ map, chặn đi qua."""
    if outline:
        sp.outline(outline)
    if shadow:
        ground_shadow(*shadow)
    if cast:
        cast_shadow(sp, x, y)
    if solid:
        block(*solid)
    OBJS.append(dict(sp=sp, x=x, y=y, fade=fade))


def add_tree(cx, base_y, r, seed, pal=L, trunk=True, solid=True):
    sp = tree(r, seed, pal, trunk)
    add(sp, int(cx - r - 1), int(base_y - sp.h), outline=LEAF_OUT, cast=False,
        shadow=(cx + 3, base_y, r * 0.9, r * 0.35), solid=(cx - 3, base_y - 4, cx + 3, base_y) if solid else None)


def add_building(sp, x, y, solid_from=0.5, bottom_trim=0):
    add(sp, x, y, solid=(x + 2, y + sp.h * solid_from, x + sp.w - 3, y + sp.h - 1 - bottom_trim))


def pack_atlas():
    items = sorted(range(len(OBJS)), key=lambda i: -OBJS[i]["sp"].img.height)
    AW = 1024
    x = y = row_h = 0
    pos = {}
    for i in items:
        im = OBJS[i]["sp"].img
        if x + im.width > AW:
            x, y, row_h = 0, y + row_h + 1, 0
        pos[i] = (x, y)
        x += im.width + 1
        row_h = max(row_h, im.height)
    AH = y + row_h + 1
    atlas = Image.new("RGBA", (AW, AH), (0, 0, 0, 0))
    out = []
    for i, o in enumerate(OBJS):
        im = o["sp"].img
        ax, ay = pos[i]
        atlas.alpha_composite(im, (ax, ay))
        out.append(dict(ax=ax, ay=ay, w=im.width, h=im.height, x=o["x"] - S.PAD, y=o["y"] - S.PAD,
                        b=o["y"] + o["sp"].h, fade=o["fade"]))
    assert AH <= 2048, "atlas quá cao"
    atlas.save(os.path.join(OUT, "objects.png"))
    return out, atlas


# ---------- Ghép ----------

def build():
    ground()
    mountains()
    mist_band(780, W, 40, 9, 0.45, 41)
    mist_band(790, W, 128, 7, 0.4, 43)
    paddies()

    s = SPOT
    road([(-10, ROAD_Y + 4), (100, ROAD_Y + 2), (300, ROAD_Y), (500, ROAD_Y - 2), (700, ROAD_Y - 4),
          (790, ROAD_Y - 4), (840, ROAD_Y + 10), (868, 396)], 8)
    road([(150, ROAD_Y + 2), (152, 470)], 5)
    road([(307, ROAD_Y), (307, 404)], 5)
    road([(118, ROAD_Y + 2), (118, 222)], 5)
    road([(400, ROAD_Y), (400, 300)], 6)
    road([(568, ROAD_Y - 2), (568, 306)], 5)
    road([(506, ROAD_Y - 2), (506, 466)], 5)
    road([(675, ROAD_Y - 4), (675, 418)], 5)
    road([(700, ROAD_Y - 4), (708, 270), (686, 222), (648, 210)], 5)
    road([(300, ROAD_Y), (302, 250), (316, 150), (360, 120), (378, 112)], 4)
    for sp, rx, ry in (("nha", 52, 20), ("ong_lang", 40, 14), ("ba_dong", 40, 14), ("thay_cung", 40, 14),
                       ("quan_nuoc", 44, 18), ("dien_thoai", 50, 16), ("dien_dia", 50, 14)):
        q = s[sp]
        soft(q["x"] + q["w"] / 2, q["y"] + q["h"] + 6, rx, ry)
    soft(592, 446, 34, 18)
    render_dirt()
    courtyard(360, 236, 440, 300)
    field()

    river = water_depth_river()
    rbank = render_water(river, 3, 0.05)
    pond_d = water_depth_pond(240, 270, 34, 16)
    render_water(pond_d, 2, 0.25)
    for lx, ly in ((224, 266), (246, 276), (258, 262), (232, 278)):
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (1, 1), (-1, 1), (0, -1)):
            M.p(lx + dx, ly + dy, L[2])
        M.p(lx + 1, ly - 1, L[3]); M.p(lx, ly + 1, L[1])
    M.p(247, 275, (236, 170, 190)); M.p(259, 261, (236, 170, 190))
    tufts_and_flowers()
    reeds(rbank, 160, [(750, 830, ROAD_Y - 22, ROAD_Y + 10)])

    # cầu tre
    by = ROAD_Y - 4
    xs = [x for (x, y) in river if y == by]
    bx0, bx1 = min(xs) - 8, max(xs) + 8
    for x in range(bx0, bx1 + 1):
        for y in range(by - 9, by + 7):
            M.p(x, y, (150, 116, 74) if x % 3 else (116, 88, 56))
        M.p(x, by - 10, K[0]); M.p(x, by - 11, K[2]); M.p(x, by + 7, K[0])
    for x in range(bx0, bx1 + 1, 6):
        for k in range(8, 11):
            M.p(x, by + k, K[0])
        M.p(x, by - 12, K[1])
    block(bx0, by - 8, bx1, by + 6, free=True)

    # rừng phía bắc: chặn cả dải, trừ khoảng trống quanh Điện Nhạc phủ
    block(0, 0, W - 1, 100)
    for i in range(520):
        x, y = rng.randint(-10, 800), rng.randint(-14, 96)
        if 312 <= x <= 446 and y > -6:
            continue
        r = rng.randint(9, 14)
        add_tree(x, y + r * 2, r, 1000 + i, LD if y < 40 else L, trunk=y > 60)
    for i in range(46):
        x = rng.randint(0, 790)
        if 350 <= x <= 406:
            continue
        add(bamboo(300 + i), x, rng.randint(60, 72), outline=LEAF_OUT, cast=False,
            solid=(x + 6, 100, x + 22, 114))

    # lũy tre: mé trái và mé dưới
    for y in range(90, 610, 13):
        add(bamboo(400 + y, rng.randint(38, 46)), rng.randint(-12, -4), y, outline=LEAF_OUT, cast=False,
            solid=(0, y, 14, y + 46))
    for x in range(-4, 676, 15):
        add(bamboo(600 + x, rng.randint(36, 44)), x + rng.randint(-2, 2), 596 + rng.randint(-2, 3),
            outline=LEAF_OUT, cast=False, solid=(x, 616, x + 28, 639))
    add(gate(), 2, ROAD_Y - 36, solid=(2, ROAD_Y - 6, 31, ROAD_Y + 2))
    block(0, ROAD_Y - 8, 6, ROAD_Y + 12)  # cổng làng: ra ngoài là hết map

    # bên kia sông
    for x, y, r in ((826, 330, 10), (940, 330, 12), (920, 400, 11), (812, 440, 9), (950, 470, 12),
                    (800, 580, 11), (870, 610, 12), (940, 600, 11), (760, 620, 10), (920, 180, 10)):
        add_tree(x, y + r * 2, r, x * 7 + y)
    for i, (x, y) in enumerate(((900, 360), (820, 380), (940, 520))):
        add(bamboo(700 + i), x, y, outline=LEAF_OUT, cast=False, solid=(x + 6, y + 34, x + 22, y + 42))

    # cây trong làng
    for x, y, r in ((40, 120, 12), (200, 120, 11), (262, 200, 10), (480, 130, 12), (520, 190, 10),
                    (720, 150, 9), (60, 300, 10), (190, 230, 9), (460, 300, 10), (620, 300, 9),
                    (40, 560, 11), (200, 570, 10), (430, 560, 12), (560, 560, 11), (640, 500, 10),
                    (330, 560, 9), (500, 520, 9), (740, 230, 9), (420, 120, 0)):
        if r:
            add_tree(x, y + r * 2, r, x * 13 + y)
    ban = banyan()
    add(ban, 562, 382, outline=LEAF_OUT, cast=False, shadow=(596, 446, 28, 9), solid=(584, 440, 600, 446))
    for x, y, sd in ((196, 380, 1), (70, 400, 2), (620, 230, 3), (280, 300, 4), (24, 210, 5), (720, 440, 6)):
        add(areca(sd), x, y, outline=LEAF_OUT, solid=(x + 6, y + 32, x + 9, y + 36))
    for x, y, sd in ((190, 428, 7), (60, 440, 8), (460, 250, 9), (610, 420, 10), (552, 520, 11)):
        add(banana(sd), x, y, outline=LEAF_OUT, solid=(x + 12, y + 26, x + 16, y + 30))
    add(haystack(), 412, 500, solid=(414, 512, 428, 518))
    add(haystack(), 170, 548, solid=(172, 560, 186, 566))
    add(scarecrow(), 402, 450, solid=(408, 466, 411, 472), fade=False)
    add(well(), 204, 298, solid=(204, 304, 220, 312))
    add(firewood(), 72, 448, solid=(72, 448, 86, 455), fade=False)
    add(fence(30), 96, 466, solid=(96, 466, 126, 472), fade=False)
    add(fence(28), 160, 466, solid=(160, 466, 188, 472), fade=False)
    add(pillar(), 354, 276, solid=(354, 296, 360, 302))
    add(pillar(), 440, 276, solid=(440, 296, 446, 302))

    # nhà dân không vào được
    add_building(house(60, 48, pal=[(80, 38, 32), (122, 56, 42), (154, 76, 52), (184, 104, 68)]), 196, 140)
    add_building(house(60, 48), 576, 470)
    add_building(house(56, 46, pal=[(82, 40, 34), (124, 58, 42), (158, 80, 54), (188, 108, 70)]), 30, 520)

    # địa điểm
    q = s["nha"]; add_building(nha(q["w"], q["h"]), q["x"], q["y"])
    q = s["dinh"]; add_building(dinh(q["w"], q["h"]), q["x"], q["y"], solid_from=0.6)
    q = s["thay_cung"]; add_building(nha_thay_cung(q["w"], q["h"]), q["x"], q["y"])
    q = s["ba_dong"]; add_building(nha_ba_dong(q["w"], q["h"]), q["x"], q["y"])
    q = s["ong_lang"]; add_building(nha_ong_lang(q["w"], q["h"]), q["x"], q["y"])
    q = s["quan_nuoc"]; add_building(quan_nuoc(q["w"], q["h"]), q["x"], q["y"], solid_from=0.55)
    t = s["dien_thoai"]
    add_building(dien(t["w"], t["h"], (232, 232, 226), (176, 176, 174),
                      [(40, 38, 46), (58, 54, 64), (76, 72, 84), (98, 94, 108)], 31, corrupt=True), t["x"], t["y"])
    add(dead_tree(), t["x"] - 20, t["y"] + 46, solid=(t["x"] - 13, t["y"] + 72, t["x"] - 9, t["y"] + 76))
    for key, accent, wall, pal, sd in (
            ("dien_nhac", (70, 150, 84), (184, 176, 146), [(70, 40, 34), (104, 58, 44), (132, 78, 54), (160, 104, 70)], 32),
            ("dien_thien", (206, 56, 48), (190, 180, 160), [(84, 36, 32), (126, 52, 40), (160, 72, 50), (192, 102, 66)], 33),
            ("dien_dia", (222, 186, 72), (204, 180, 116), [(76, 46, 32), (112, 70, 44), (142, 94, 58), (172, 122, 76)], 34)):
        q = s[key]
        add(dien(q["w"], q["h"], accent, wall, pal, sd), q["x"], q["y"], solid=(q["x"], q["y"], q["x"] + q["w"], q["y"] + q["h"]))
    # sương chắn lối vào điện chưa mở (Unity vẽ sương lên)
    block(330, 84, 426, 108)                    # Nhạc phủ
    block(780, 150, 959, 178)                   # chân núi Thiên phủ
    block(812, 420, 944, 560)                   # Địa phủ

    bt = boat()
    bt.outline()
    M.img.alpha_composite(bt.img, (696 - S.PAD, 556 - S.PAD))

    # sương tím quanh điện Thoải phủ
    nz = make_noise(8, 42)
    for y in range(t["y"] - 16, t["y"] + t["h"] + 20):
        for x in range(t["x"] - 30, t["x"] + t["w"] + 24):
            e = min(x - (t["x"] - 30), t["x"] + t["w"] + 24 - x, y - (t["y"] - 16), t["y"] + t["h"] + 20 - y) / 12.0
            v = nz(x, y) * min(1.0, e)
            if v > 0.5:
                M.blend(x, y, (150, 130, 176), 0.28)
            elif v > 0.38:
                M.blend(x, y, (150, 130, 176), 0.12)

    for y in range(H):  # nắng ấm
        for x in range(W):
            c = M.px[x, y][:3]
            M.px[x, y] = c4((min(255, int(c[0] * 1.04 + 3)), c[1], int(c[2] * 0.94)))
    M.img.save(os.path.join(OUT, "ground.png"))
    water_frames([river, pond_d])

    # vùng ruộng đi được (đất cày), cầu đi được
    solid = []
    for gy in range(GH):
        row = []
        for gx in range(GW):
            row.append("1" if SOLID[gy][gx] and not FREE[gy][gx] else "0")
        solid.append("".join(row))
    return "".join(solid)


# ---------- Cây trồng, icon ----------

def crop_sprite(kind, stage):
    s = S(9, 11)
    g1, g2 = L[2], L[3]
    if stage == 0:
        s.rect(4, 7, 4, 10, g1); s.p(3, 7, g2); s.p(2, 6, g2); s.p(5, 7, g1); s.p(6, 6, g1)
        return s
    if kind == "lua_nep":
        stalk = (190, 166, 78) if stage == 2 else g1
        for x, top in ((2, 3), (4, 1), (6, 3)):
            s.rect(x, top, x, 10, stalk)
        s.p(3, 5, g2 if stage == 1 else (170, 150, 70))
        if stage == 2:
            for x, y in ((1, 2), (1, 3), (3, 0), (3, 1), (5, 2), (7, 2), (7, 3)):
                s.p(x, y, (230, 200, 100))
    elif kind == "trau":
        s.rect(4, 1, 4, 10, K[2])
        for y in range(2, 10, 2):
            s.p(3 if y % 4 else 5, y, g1); s.p(2 if y % 4 else 6, y, g2 if stage == 2 else g1)
            s.p(2 if y % 4 else 6, y + 1, L[1])
    elif kind == "cau":
        top = 1 if stage == 2 else 4
        s.rect(4, top + 2, 4, 10, (160, 146, 112))
        for dx in (-3, -2, -1, 1, 2, 3):
            s.p(4 + dx, top + (1 if abs(dx) == 3 else 0), g2 if dx < 0 else g1)
        if stage == 2:
            s.p(3, top + 2, (210, 130, 50)); s.p(5, top + 2, (196, 112, 42))
    elif kind == "ngai_cuu":
        c1, c2 = (128, 150, 120), (164, 186, 154)
        r = 3 if stage == 2 else 2
        for y in range(10 - 2 * r, 11):
            for x in range(4 - r, 5 + r):
                if (x + y) % 2 == 0 or stage == 2:
                    s.p(x, y, c2 if x < 4 else c1)
    elif kind == "hoa_hue":
        s.rect(4, 2, 4, 10, g1); s.p(3, 8, g2); s.p(5, 9, g1)
        if stage == 2:
            for x, y in ((3, 1), (5, 1), (4, 0), (3, 3), (5, 3), (4, 2)):
                s.p(x, y, (246, 246, 236))
    return s


def crops():
    for k in ("lua_nep", "trau", "cau", "ngai_cuu", "hoa_hue"):
        for st in range(3):
            sp = crop_sprite(k, st)
            sp.outline((40, 34, 26))
            sp.img.save(os.path.join(OUT, "crop_%s_%d.png" % (k, st)))


def bayer(x, y):
    m = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
    return (m[y & 3][x & 3] + 0.5) / 16.0


def icons():
    s = S(14, 14)
    for y in range(14):
        for x in range(14):
            d = math.hypot(x - 6.5, y - 6.5)
            if d <= 3.6:
                s.p(x, y, (250, 214, 90) if x + y < 13 else (234, 172, 54))
            elif d <= 6.6 and (round(math.degrees(math.atan2(y - 6.5, x - 6.5))) // 15) % 3 == 0:
                s.p(x, y, (250, 196, 70))
    s.outline((70, 44, 20))
    s.img.save(os.path.join(OUT, "sun.png"))

    s = S(7, 9)
    s.rect(1, 0, 5, 0, (180, 180, 186)); s.rect(1, 0, 1, 3, (180, 180, 186)); s.rect(5, 0, 5, 3, (150, 150, 156))
    s.rect(0, 4, 6, 8, (214, 180, 80)); s.rect(4, 4, 6, 8, (180, 144, 60)); s.p(3, 6, (60, 44, 30))
    s.outline()
    s.img.save(os.path.join(OUT, "lock.png"))

    fog = Image.new("RGBA", (64, 40), (0, 0, 0, 0))
    fp = fog.load()
    nz = make_noise(7, 77)
    for y in range(40):
        for x in range(64):
            e = min(x, 63 - x, y, 39 - y) / 9.0
            v = nz(x * 1.0, y * 1.0) * 0.6 + min(1.0, e) * 0.6
            if v + (bayer(x, y) - 0.5) * 0.3 > 0.72:
                fp[x, y] = (214, 218, 224, 205)
            elif v + (bayer(x, y) - 0.5) * 0.3 > 0.6:
                fp[x, y] = (190, 196, 204, 150)
    fog.save(os.path.join(OUT, "fog.png"))

    cloud = Image.new("RGBA", (96, 56), (0, 0, 0, 0))
    cp = cloud.load()
    nz = make_noise(9, 88)
    for y in range(56):
        for x in range(96):
            e = ((x - 48) / 48) ** 2 + ((y - 28) / 28) ** 2
            if (1 - e) * 0.9 + (nz(x * 1.0, y * 1.0) - 0.5) * 0.7 > 0.35:
                cp[x, y] = (255, 255, 255, 255)
    cloud.save(os.path.join(OUT, "cloud.png"))


def preview(objs, atlas):
    img = M.img.copy()
    for o in sorted(objs, key=lambda o: o["b"]):
        crop = atlas.crop((o["ax"], o["ay"], o["ax"] + o["w"], o["ay"] + o["h"]))
        if o["x"] < 0 or o["y"] < 0:  # vật thể chìa ra ngoài mép trái/trên
            crop = crop.crop((max(0, -o["x"]), max(0, -o["y"]), crop.width, crop.height))
        img.alpha_composite(crop, (max(0, o["x"]), max(0, o["y"])))
    img.save(os.path.join(PREVIEW, "_world_preview.png"))
    img.save(os.path.join(OUT, "minimap.png"))  # bản đồ nhỏ và bản đồ lớn (M) dùng ảnh ghép sẵn này
    sol = img.copy()
    d = ImageDraw.Draw(sol, "RGBA")
    for gy in range(GH):
        for gx in range(GW):
            if SOLID[gy][gx] and not FREE[gy][gx]:
                d.rectangle((gx * CELL, gy * CELL, gx * CELL + CELL - 1, gy * CELL + CELL - 1), fill=(255, 0, 0, 70))
    for sp in SPOTS:
        d.ellipse((sp["dx"] - 4, sp["dy"] - 4, sp["dx"] + 4, sp["dy"] + 4), fill=(255, 230, 0, 255))
    for f in FRIENDS:
        d.rectangle((f["x"] - 5, f["y"] - 20, f["x"] + 5, f["y"]), fill=(0, 200, 255, 200))
    sol.save(os.path.join(PREVIEW, "_world_collision.png"))


if __name__ == "__main__":
    solid = build()
    objs, atlas = pack_atlas()
    crops()
    icons()
    for sp in SPOTS:
        sp.setdefault("npc", "")
    data = dict(width=W, height=H, cell=CELL, cols=GW, rows=GH, solid=solid, spots=SPOTS, plots=PLOTS, smoke=SMOKE,
                friends=FRIENDS, spawn=SPAWN, objects=objs)
    with open(os.path.join(OUT, "world.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    preview(objs, atlas)
    print("done →", OUT, "| vật thể:", len(objs), "| atlas:", atlas.size)
