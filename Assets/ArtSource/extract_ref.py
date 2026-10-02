"""Cắt sprite, chân dung, ma từ ảnh tham chiếu (ArtSource/reference/) và đưa về lưới pixel cho game.
Chạy: python extract_ref.py → ghi đè Assets/Resources/Walk, Portraits, Battle (ma).
Toạ độ là pixel trong ảnh gốc; sửa CELLS/PORTRAITS/ENEMIES nếu muốn lấy hình khác."""
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from collections import deque
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
ASSETS = PARENT if os.path.basename(PARENT) == "Assets" else os.path.join(PARENT, "Assets")
REF = os.path.join(HERE, "reference")
RES = os.path.join(ASSETS, "Resources")
PREVIEW = os.path.join(HERE, "sprites")
os.makedirs(PREVIEW, exist_ok=True)

SHEETS = {}


def sheet(name):
    if name not in SHEETS:
        SHEETS[name] = Image.open(os.path.join(REF, name)).convert("RGB")
    return SHEETS[name]


def dist(a, b):
    return sum((a[i] - b[i]) ** 2 for i in range(3)) ** 0.5


def cut(src, box, tol=26):
    """Cắt vùng box, xoá nền bằng loang màu từ mép vào. Trả về RGBA đã thu gọn sát hình."""
    img = sheet(src).crop(box)
    w, h = img.size
    px = img.load()
    border = [px[x, 0] for x in range(w)] + [px[x, h - 1] for x in range(w)] + \
             [px[0, y] for y in range(h)] + [px[w - 1, y] for y in range(h)]
    bg = tuple(sorted(c[i] for c in border)[len(border) // 2] for i in range(3))
    seen = [[False] * w for _ in range(h)]
    q = deque()
    for x in range(w):
        q.append((x, 0)); q.append((x, h - 1))
    for y in range(h):
        q.append((0, y)); q.append((w - 1, y))
    while q:
        x, y = q.popleft()
        if not (0 <= x < w and 0 <= y < h) or seen[y][x]:
            continue
        if dist(px[x, y], bg) > tol:
            continue
        seen[y][x] = True
        q.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    out = img.convert("RGBA")
    op = out.load()
    for y in range(h):
        for x in range(w):
            if seen[y][x]:
                op[x, y] = (0, 0, 0, 0)
    keep_main(out)
    bbox = out.getbbox()
    return out.crop(bbox) if bbox else out


def keep_main(img, near=4, min_frac=0.02):
    """Chỉ giữ khối hình lớn nhất và các mảnh nhỏ nằm sát nó; bỏ mảnh hình bên cạnh, đường kẻ, chữ."""
    w, h = img.size
    px = img.load()
    label = [[-1] * w for _ in range(h)]
    comps = []
    for y in range(h):
        for x in range(w):
            if px[x, y][3] and label[y][x] < 0:
                pts, q = [], deque([(x, y)])
                label[y][x] = len(comps)
                while q:
                    cx, cy = q.popleft()
                    pts.append((cx, cy))
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < w and 0 <= ny < h and px[nx, ny][3] and label[ny][nx] < 0:
                            label[ny][nx] = len(comps)
                            q.append((nx, ny))
                comps.append(pts)
    if not comps:
        return
    main = max(comps, key=len)
    xs = [p[0] for p in main]
    ys = [p[1] for p in main]
    bx0, bx1, by0, by1 = min(xs) - near, max(xs) + near, min(ys) - near, max(ys) + near
    for c in comps:
        if c is main:
            continue
        cx = sum(p[0] for p in c) / len(c)
        cy = sum(p[1] for p in c) / len(c)
        tall_thin = (max(p[1] for p in c) - min(p[1] for p in c)) > 3 * (max(p[0] for p in c) - min(p[0] for p in c) + 1)
        inside = bx0 <= cx <= bx1 and by0 <= cy <= by1
        if not inside or len(c) < len(main) * min_frac or tall_thin:
            for x, y in c:
                px[x, y] = (0, 0, 0, 0)


def pixelize(img, height, colors=24, outline=True):
    """Thu về chiều cao `height` pixel, alpha cứng, gom màu, viền tối ở mép."""
    w = max(1, round(img.width * height / img.height))
    sharp = img.filter(ImageFilter.UnsharpMask(radius=1.2, percent=80, threshold=2))
    rgb = sharp.convert("RGB").resize((w, height), Image.LANCZOS)
    alpha = img.split()[3].resize((w, height), Image.BOX)
    q = rgb.quantize(colors=colors, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE).convert("RGB")
    out = Image.new("RGBA", (w, height), (0, 0, 0, 0))
    o, qp, ap = out.load(), q.load(), alpha.load()
    for y in range(height):
        for x in range(w):
            if ap[x, y] >= 110:
                o[x, y] = qp[x, y] + (255,)
    if outline:  # mép ngoài sẫm lại thành viền
        src = out.copy().load()
        for y in range(height):
            for x in range(w):
                if not src[x, y][3]:
                    continue
                edge = any(not (0 <= x + dx < w and 0 <= y + dy < height) or not src[x + dx, y + dy][3]
                           for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                if edge:
                    r, g, b, a = src[x, y]
                    o[x, y] = (int(r * 0.45 + 12), int(g * 0.4 + 8), int(b * 0.45 + 14), 255)
    return out


def canvas(img, cw, ch):
    """Đặt sprite vào khung cố định, chân sát đáy, căn giữa ngang."""
    c = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    c.alpha_composite(img, ((cw - img.width) // 2, ch - img.height))
    return c


def mirror(img):
    return img.transpose(Image.FLIP_LEFT_RIGHT)


# ---------- Sprite đi lại ----------
# Ảnh A (sheet_a.png): hàng = nhân vật, cột tâm x: 60,120,180,232,285,337,400,450,500
COLX = {1: 60, 2: 120, 3: 180, 4: 232, 5: 285, 6: 337, 7: 400, 8: 450, 9: 500}
ROWY = {"minh": (50, 110), "vy": (108, 170), "lan": (170, 240), "tuan": (240, 308), "khoa": (308, 380),
        "row6": (380, 452), "hai": (464, 532)}


def a_cell(row, col, half=27):
    y0, y1 = ROWY[row]
    return ("sheet_a.png", (COLX[col] - half, y0, COLX[col] + half, y1))


# Ảnh B (sheet_b.png): cột "Side Walk Cycle" (x ~547..667) và cột nhìn ngang ở bảng trái
B_SIDE = {"tuan": (40, 105), "khoa": (108, 172), "phong": (175, 242), "hai": (248, 314)}
B_SIDE_X = [(540, 586), (588, 630), (630, 672)]
B_LEFT_ROWS = {"minh": (50, 110), "vy": (110, 170), "lan": (172, 238)}
B_LEFT_X = [(140, 190), (192, 238)]

# mỗi người: down (đứng, bước), up (đứng, bước, bước), side (khung nhìn ngang, quay trái hay phải)
WALK = {
    "minh": dict(down=[a_cell("minh", 1), a_cell("minh", 7)], up=[a_cell("minh", 2), a_cell("minh", 8), a_cell("minh", 9)],
                 side=[("sheet_b.png", (B_LEFT_X[1][0], 50, B_LEFT_X[1][1], 110))]),
    "vy": dict(down=[a_cell("vy", 1), a_cell("vy", 7)], up=[a_cell("vy", 2), a_cell("vy", 8), a_cell("vy", 9)],
               side=[("sheet_b.png", (B_LEFT_X[1][0], 110, B_LEFT_X[1][1], 170))]),
    "lan": dict(down=[a_cell("lan", 3), a_cell("lan", 7)], up=[a_cell("lan", 2), a_cell("lan", 8), a_cell("lan", 9)],
                side=[("sheet_b.png", (B_LEFT_X[1][0], 172, B_LEFT_X[1][1], 238))]),
    "tuan": dict(down=[a_cell("tuan", 4), a_cell("tuan", 7)], up=[a_cell("tuan", 6), a_cell("tuan", 8), a_cell("tuan", 9)],
                 side=[("sheet_b.png", (x0, B_SIDE["tuan"][0], x1, B_SIDE["tuan"][1])) for x0, x1 in B_SIDE_X]),
    "khoa": dict(down=[a_cell("khoa", 1), a_cell("khoa", 7)], up=[a_cell("khoa", 2), a_cell("khoa", 8)],
                 side=[("sheet_b.png", (x0, B_SIDE["khoa"][0], x1, B_SIDE["khoa"][1])) for x0, x1 in B_SIDE_X]),
    "phong": dict(down=[a_cell("row6", 4), a_cell("row6", 5)], up=[a_cell("row6", 6)],
                  side=[("sheet_b.png", (x0, B_SIDE["phong"][0], x1, B_SIDE["phong"][1])) for x0, x1 in B_SIDE_X]),
    "ong_cu": dict(down=[a_cell("row6", 1), a_cell("row6", 3)], up=[a_cell("row6", 2)],
                   side=[a_cell("row6", 1)]),
    "hai": dict(down=[a_cell("hai", 1), a_cell("hai", 3)], up=[a_cell("hai", 2)],
                side=[("sheet_b.png", (x0, B_SIDE["hai"][0], x1, B_SIDE["hai"][1])) for x0, x1 in B_SIDE_X[:2]]),
}
# hướng mặt của khung nhìn ngang trong ảnh gốc ("left"/"right"); kiểm bằng ảnh xem trước
SIDE_FACING = {"minh": "left", "vy": "left", "lan": "left", "tuan": "right", "khoa": "right", "phong": "right",
               "ong_cu": "front", "hai": "right"}

WALK_H, WALK_CW, WALK_CH = 34, 24, 36  # cao nhân vật, khung ảnh


def walk_frames(spec):
    return [canvas(pixelize(cut(src, box), WALK_H), WALK_CW, WALK_CH) for src, box in spec]


def build_walk():
    out_dir = os.path.join(RES, "Walk")
    rows = []
    for name, spec in WALK.items():
        down = walk_frames(spec["down"])
        up = walk_frames(spec["up"])
        side = walk_frames(spec["side"])
        # bước: khung đi + bản soi gương (nhìn thẳng thì soi gương là đổi chân)
        d = [down[0], down[1] if len(down) > 1 else down[0], mirror(down[1] if len(down) > 1 else down[0])]
        u = [up[0], up[1] if len(up) > 1 else up[0], up[2] if len(up) > 2 else mirror(up[1] if len(up) > 1 else up[0])]
        facing = SIDE_FACING[name]
        left = [mirror(f) if facing == "right" else f for f in side]
        lf = [left[0], left[1 % len(left)], left[2 % len(left)]]
        for i in range(3):
            d[i].save(os.path.join(out_dir, "%s_down_%d.png" % (name, i)))
            u[i].save(os.path.join(out_dir, "%s_up_%d.png" % (name, i)))
            lf[i].save(os.path.join(out_dir, "%s_left_%d.png" % (name, i)))
            mirror(lf[i]).save(os.path.join(out_dir, "%s_right_%d.png" % (name, i)))
        # trận: tạm lấy khung bước làm tư thế đánh, khung đứng làm tư thế trúng đòn (chờ ảnh tư thế chiến đấu)
        mirror(lf[1]).save(os.path.join(out_dir, "%s_right_atk.png" % name))
        mirror(lf[0]).save(os.path.join(out_dir, "%s_right_hurt.png" % name))
        rows.append(d + u + lf)
    return rows


# ---------- Chân dung (48x48) ----------
# ô trong bảng "BÌNH THƯỜNG" ở ảnh B; cắt phía trong khung viền
GX = {0: 836, 1: 899, 2: 962}
GY = {0: 54, 1: 120, 2: 186, 3: 261, 4: 333}


def grid(col, row, size=41):
    return ("sheet_b.png", (GX[col], GY[row], GX[col] + size, GY[row] + size))


PORTRAITS = {
    "minh": grid(0, 0), "vy": grid(1, 0), "lan": grid(2, 1), "tuan": grid(0, 1), "khoa": grid(1, 1),
    "ong_cu": grid(0, 3), "phong": grid(1, 3), "hai_tha_hoa": grid(2, 3),
    "hai": ("sheet_a.png", (383, 483, 420, 523)),
}


def build_portraits():
    out = []
    for name, (src, box) in PORTRAITS.items():
        img = sheet(src).crop(box).filter(ImageFilter.UnsharpMask(radius=1, percent=60, threshold=2))
        img = img.resize((48, 48), Image.LANCZOS)
        img = img.quantize(colors=40, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE).convert("RGBA")
        img.save(os.path.join(RES, "Portraits", name + ".png"))
        out.append(img)
    return out


# ---------- Ma trong trận ----------
ENEMIES = {
    "ma_doi": (("sheet_b.png", (238, 448, 332, 537)), 46),
    "ma_nuoc": (("sheet_b.png", (32, 452, 84, 540)), 48),
    "ma_nhen": (("sheet_a.png", (312, 466, 370, 530)), 38),
}


def build_enemies():
    out = []
    for name, ((src, box), h) in ENEMIES.items():
        img = pixelize(cut(src, box, tol=24), h, colors=28)
        f0 = canvas(img, img.width + 2, h + 2)
        f1 = Image.new("RGBA", f0.size, (0, 0, 0, 0))  # khung 2: hạ 1 pixel (lơ lửng)
        f1.alpha_composite(f0.crop((0, 0, f0.width, f0.height - 1)), (0, 1))
        f0.save(os.path.join(RES, "Battle", name + "_0.png"))
        f1.save(os.path.join(RES, "Battle", name + "_1.png"))
        out.append(f0)
    return out


# ---------- Sprite sheet nền magenta tạo bằng AI (Docs/PROMPT_ART.md) ----------

def magenta_cut(img):
    """Xoá nền magenta và viền pha hồng ở mép, chỉ giữ khối hình chính, thu gọn sát hình."""
    out = img.convert("RGBA")
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            pink = min(r, b) - g  # độ "magenta"
            if pink > 90 and abs(r - b) < 90:
                px[x, y] = (0, 0, 0, 0)
            elif pink > 40 and abs(r - b) < 90:  # viền pha hồng: khử màu hồng
                px[x, y] = (min(r, g + 30), g, min(b, g + 30), 255)
    keep_main(out)
    bbox = out.getbbox()
    return out.crop(bbox) if bbox else out


def sheet_cells(path, cols, rows, inset=8):
    """Chia ảnh thành lưới cols x rows, lùi vào mỗi ô `inset` pixel để bỏ đường kẻ giữa ô."""
    img = Image.open(path).convert("RGB")
    cw, ch = img.width / cols, img.height / rows
    cells = []
    for r in range(rows):
        for c in range(cols):
            box = (int(c * cw + inset), int(r * ch + inset), int((c + 1) * cw - inset), int((r + 1) * ch - inset))
            cells.append(magenta_cut(img.crop(box)))
    return cells


BATTLE_H = 56   # chiều cao người trong trận (pixel trận)
BATTLE_POSES = ["0", "1", "atk", "hurt"]  # 4 ô của prompt B: thủ thế, thở, đánh, trúng đòn


def build_battle_sheets():
    """reference/<tên>_battle.png (lưới 2x2) → Resources/Battle/<tên>_0, _1, _atk, _hurt.png"""
    out = []
    for f in sorted(os.listdir(REF)):
        if not f.endswith("_battle.png"):
            continue
        name = f[:-len("_battle.png")]
        cells = sheet_cells(os.path.join(REF, f), 2, 2)
        # cùng một tỉ lệ thu cho cả 4 ô (theo ô thủ thế) để người không to nhỏ khác nhau
        scale = BATTLE_H / cells[0].height
        frames = [pixelize(c, max(8, round(c.height * scale)), colors=32) for c in cells]
        cw = max(fr.width for fr in frames) + 2
        ch = max(fr.height for fr in frames) + 1
        for pose, fr in zip(BATTLE_POSES, frames):
            canvas(fr, cw, ch).save(os.path.join(RES, "Battle", "%s_%s.png" % (name, pose)))
        out.append((name, [canvas(fr, cw, ch) for fr in frames]))
    return out


# reference/<tên>_walk.png: AI không luôn ra đúng lưới xin, nên khai báo từng bảng:
# cols, rows; mỗi hướng là 3 ô (hàng, cột) cho khung 0 (đứng), 1, 2 (bước); side_faces = hướng của hàng nhìn ngang.
WALK_SHEETS = {
    "khoa": dict(cols=6, rows=3, down=[(0, 0), (0, 1), (0, 3)], side=[(1, 0), (1, 2), (1, 4)], side_faces="right",
                 up=[(2, 0), (2, 1), (2, 3)]),
}


def build_walk_sheets():
    out_dir = os.path.join(RES, "Walk")
    rows_out = []
    for name, spec in WALK_SHEETS.items():
        path = os.path.join(REF, name + "_walk.png")
        if not os.path.exists(path):
            continue
        cells = sheet_cells(path, spec["cols"], spec["rows"], inset=6)
        cell = lambda rc: cells[rc[0] * spec["cols"] + rc[1]]
        scale = WALK_H / cell(spec["down"][0]).height  # cùng tỉ lệ cho mọi khung
        def frames(key):
            return [canvas(pixelize(cell(rc), max(8, round(cell(rc).height * scale))), WALK_CW, WALK_CH) for rc in spec[key]]
        down, up, side = frames("down"), frames("up"), frames("side")
        left = [mirror(f) for f in side] if spec["side_faces"] == "right" else side
        for i in range(3):
            down[i].save(os.path.join(out_dir, "%s_down_%d.png" % (name, i)))
            up[i].save(os.path.join(out_dir, "%s_up_%d.png" % (name, i)))
            left[i].save(os.path.join(out_dir, "%s_left_%d.png" % (name, i)))
            mirror(left[i]).save(os.path.join(out_dir, "%s_right_%d.png" % (name, i)))
        rows_out.append(down + up + left)
    return rows_out


def preview(walk_rows, portraits, enemies):
    sc = 5
    W = max(len(r) for r in walk_rows) * (WALK_CW * sc + 6) + 20
    H = len(walk_rows) * (WALK_CH * sc + 6) + 48 * sc + 70 * sc
    img = Image.new("RGBA", (W, H), (54, 58, 70, 255))
    y = 10
    for r in walk_rows:
        for i, f in enumerate(r):
            img.alpha_composite(f.resize((f.width * sc, f.height * sc), Image.NEAREST), (10 + i * (WALK_CW * sc + 6), y))
        y += WALK_CH * sc + 6
    for i, p in enumerate(portraits):
        img.alpha_composite(p.resize((48 * 4, 48 * 4), Image.NEAREST), (10 + i * (48 * 4 + 8), y + 10))
    y += 48 * 4 + 30
    x = 10
    for e in enemies:
        img.alpha_composite(e.resize((e.width * sc, e.height * sc), Image.NEAREST), (x, y))
        x += e.width * sc + 20
    img.save(os.path.join(PREVIEW, "_extract_preview.png"))


if __name__ == "__main__":
    w = build_walk()
    w += build_walk_sheets()  # bảng đi lại mới ghi đè bản cắt từ ảnh tham chiếu cũ
    p = build_portraits()
    e = build_enemies()
    preview(w, p, e)
    b = build_battle_sheets()
    if b:
        sc = 5
        W_ = sum(max(f.width for f in fr) * sc * 4 + 40 for _, fr in b) + 20
        H_ = max(fr[0].height for _, fr in b) * sc + 20
        img = Image.new("RGBA", (W_, H_), (40, 40, 56, 255))
        x = 10
        for _, frames in b:
            for fr in frames:
                img.alpha_composite(fr.resize((fr.width * sc, fr.height * sc), Image.NEAREST), (x, 10))
                x += fr.width * sc + 10
            x += 30
        img.save(os.path.join(PREVIEW, "_battle_sheets_preview.png"))
    print("done")
