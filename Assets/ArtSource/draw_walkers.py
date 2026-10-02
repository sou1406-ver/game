"""Sprite đi lại 16x24 (kiểu Stardew/Earthbound) cho 5 người chơi được. Dùng cả ngoài làng lẫn trong trận.
Vẽ tay bằng lưới chữ: khung người theo hướng + lớp tóc và trang phục riêng từng người, đổ bóng 3 tông, viền màu.
Chạy: python draw_walkers.py → Assets/Resources/Walk/<tên>_<hướng>_<khung>.png
  hướng: down, up, left, right · khung: 0 đứng, 1 bước trái, 2 bước phải · thêm right_atk, right_hurt (trận)."""
from PIL import Image
import os

W, H = 16, 24
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
ASSETS = PARENT if os.path.basename(PARENT) == "Assets" else os.path.join(PARENT, "Assets")
OUT = os.path.join(ASSETS, "Resources", "Walk")
PREVIEW = os.path.join(HERE, "sprites")
os.makedirs(OUT, exist_ok=True)
os.makedirs(PREVIEW, exist_ok=True)


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c[:3])


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ---------- Khung người (mã: S da, s da tối, E mắt, B má, M miệng, N tay, n tay tối,
#            T áo, t áo tối, A tay áo sáng, a tay áo tối, P quần, p quần tối, F giày, f giày tối) ----------

B_DOWN = [
    "................",
    "................",
    ".....SSSSSS.....",
    "....SSSSSSSS....",
    "...SSSSSSSSSs...",
    "...SSSSSSSSSs...",
    "...SSSSSSSSSs...",
    "...SSESSSSESs...",
    "...SSESSSSESs...",
    "...SBSSSSSSBs...",
    "...SSSSMMSSSs...",
    "....SSSSSSSs....",
    ".....sSSSSs.....",
    ".....TTTTTt.....",
    "...ATTTTTTtta...",
    "..AATTTTTTttaa..",
    "..AATTTTTTttaa..",
    "..AATTTTTTttaa..",
    "..NNTTTTTTttnn..",
    "....PPPPPPpp....",
    "....PPp..PPp....",
    "....PPp..PPp....",
    "...FFFf..FFFf...",
    "................",
]
D_STEP = {
    1: {17: "..NNTTTTTTttaa..", 18: "....TTTTTTttnn..", 20: "....PPp..PPp....",
        21: "...FFFf..PPp....", 22: ".........FFFf..."},
    2: {17: "..AATTTTTTttnn..", 18: "..NNTTTTTTtt....", 20: "....PPp..PPp....",
        21: "....PPp..FFFf...", 22: "...FFFf........."},
}

B_LEFT = [
    "................",
    "................",
    ".....SSSSSS.....",
    "....SSSSSSSS....",
    "...SSSSSSSSSs...",
    "...SSSSSSSSSs...",
    "...SSSSSSSSSs...",
    "...SESSSSSSSs...",
    "...SESSSSSSSs...",
    "..SSBSSSSSSSs...",
    "...SMSSSSSSs....",
    "....SSSSSSSs....",
    ".....sSSSSs.....",
    ".....TTTTtt.....",
    ".....TTaaTt.....",
    ".....TTaaTt.....",
    ".....TTaaTt.....",
    ".....TTaaTt.....",
    ".....TTNNTt.....",
    "......PPPp......",
    "......PPPp......",
    "......PPPp......",
    ".....FFFFf......",
    "................",
]
L_STEP = {
    1: {14: ".....aaTTTt.....", 15: "....aaTTTTt.....", 16: "...aaTTTTTt.....", 17: "...NNTTTTTt.....",
        18: ".....TTTTTt.....", 19: "......PPPPp.....", 20: ".....PPP.pp.....", 21: "....PPp...pp....",
        22: "...FFFf...ff...."},
    2: {14: ".....TTTTaa.....", 15: ".....TTTTTaa....", 16: ".....TTTTTtaa...", 17: ".....TTTTTtnn...",
        18: ".....TTTTTt.....", 19: "......PPPPp.....", 20: ".....pp.PPP.....", 21: "....pp...PPp....",
        22: "...ff...FFFf...."},
    "atk": {14: ".....TTTTTt.....", 15: ".NNaaaTTTTt.....", 16: ".....TTTTTt.....", 17: ".....TTTTTt.....",
            18: ".....TTTTTt.....", 19: "......PPPPp.....", 20: ".....PPP..pp....", 21: "....PPp....pp...",
            22: "...FFFf....fff.."},
}

# ---------- Tóc, mũ, đồ riêng từng người: (dòng, chuỗi 16 ký tự); '.' = giữ nguyên ----------
# H tóc, h tóc tối, L tóc sáng, R điểm nhấn (dây buộc), X Y x nón lá, G gọng kính

HAIR = {
    "minh": {
        "down": [(0, "......H..H......"), (1, "....HHHHHHHH...."), (2, "...HHLLHHHHHH..."), (3, "..HHLHHHHHHHHh.."),
                 (4, "..HHHHHHHHHHHh.."), (5, "..HHHHHHHHHHhh.."), (6, "...HHH.HHH.Hh..."), (7, "...H........h..."),
                 (8, "...H........h...")],
        "up": [(0, "......H..H......"), (1, "....HHHHHHHH...."), (2, "...HHHLLHHHHH..."), (3, "..HHHLHHHHHHHh..")]
              + [(r, "..HHHHHHHHHHHh..") for r in range(4, 10)] + [(10, "...hHHHHHHHHh..."), (11, "....hhhhhhhh....")],
        "left": [(0, ".......H..H....."), (1, ".....HHHHHHH...."), (2, "....HHLLHHHHH..."), (3, "...HHLHHHHHHHh.."),
                 (4, "..HHHHHHHHHHHh.."), (5, "..HH.HHHHHHHHh.."), (6, "...H...HHHHHHh.."), (7, ".......HHHHHhh.."),
                 (8, "........HHHHh..."), (9, "........HHHh...."), (10, ".........hh.....")],
    },
    "vy": {
        "down": [(1, ".....HHHHHH....."), (2, "....HLLHHHHH...."), (3, "...HLHHHHHHHh..."), (4, "..HHHHHHHHHHHh.."),
                 (5, "..HHHHHHHHHHHhR."), (6, "..HHHHHHHHHHHh..")]
                + [(r, "..HH........hh..") for r in range(7, 11)] + [(11, "..hh........hh..")],
        "up": [(1, ".....HHHHHH....."), (2, "....HHHLLHHH...."), (3, "...HHHLHHHHHh..."), (4, "..HHHHHHHHHHHh.."),
               (5, "..HHHHHHHHHHHhR.")] + [(r, "..HHHHHHHHHHHh..") for r in range(6, 11)]
              + [(11, "..hHHHHHHHHHhh.."), (12, "...hhhhhhhhhh...")],
        "left": [(1, ".....HHHHHH....."), (2, "....HLLHHHHH...."), (3, "...HLHHHHHHHh..."), (4, "..HHHHHHHHHHHh.."),
                 (5, "..HHHHHHHHHHHh.."), (6, "..HHH..HHHHHHhR."), (7, "..H....HHHHHHh.."), (8, ".......HHHHHHh.."),
                 (9, ".......HHHHHHh.."), (10, ".......HHHHHhh.."), (11, "........hhhhh...")],
    },
    "lan": {
        "down": [(0, ".......XY......."), (1, "......XYXX......"), (2, ".....XYXXXx....."), (3, "...XXYXXXXXxx..."),
                 (4, ".XXXXXXXXXXXXXx."), (5, ".xxxxxxxxxxxxxx."), (6, "...HHHHHHHHHh..."), (7, "...H........h..."),
                 (8, "...H........h..."), (9, "...H........h...")]
                + [(r, "...........H....") for r in (11, 12, 13, 15)] + [(14, "...........h...."), (16, "...........h...."),
                                                                      (17, "...........R....")],
        "up": [(0, ".......XY......."), (1, "......XYXX......"), (2, ".....XYXXXx....."), (3, "...XXYXXXXXxx..."),
               (4, ".XXXXXXXXXXXXXx."), (5, ".xxxxxxxxxxxxxx.")]
              + [(r, "...HHHHHHHHHh...") for r in range(6, 12)] + [(12, ".......HH.......")]
              + [(r, ".......Hh.......") for r in range(13, 18)] + [(18, ".......RR.......")],
        "left": [(0, "........XY......"), (1, ".......XYXX....."), (2, "......XYXXXx...."), (3, "....XXYXXXXXxx.."),
                 (4, "..XXXXXXXXXXXXx."), (5, "..xxxxxxxxxxxxx."), (6, "......HHHHHHh..."), (7, "......HHHHHHh..."),
                 (8, ".......HHHHHh..."), (9, ".........HHh....")]
                + [(r, "..........Hh....") for r in range(10, 17)] + [(17, "..........RR....")],
    },
    "tuan": {
        "down": [(1, ".....HHHHHHH...."), (2, "....HHHHHLLH...."), (3, "...HHHHHLLHHh..."), (4, "..HHHHHHHHHHHh.."),
                 (5, "..HHHHHHHHHHHh.."), (6, "...HHHHH....hh.."), (7, "...H.........h..")],
        "up": [(1, ".....HHHHHHH...."), (2, "....HHHHHLLH...."), (3, "...HHHHHLLHHh...")]
              + [(r, "..HHHHHHHHHHHh..") for r in range(4, 10)] + [(10, "...HHHHHHHHHh..."), (11, "....hhhhhhhh....")],
        "left": [(1, ".....HHHHHHH...."), (2, "....HHHHHLLHH..."), (3, "...HHHHLLHHHHh.."), (4, "..HHHHHHHHHHHh.."),
                 (5, "..HHHH.HHHHHHh.."), (6, ".......HHHHHh..."), (7, "........HHHHh..."), (8, ".........HHh....")],
    },
    "khoa": {
        "down": [(1, ".....HHHHHH....."), (2, "....HHLLHHHH...."), (3, "...HHLHHHHHHh..."), (4, "..HHHHHHHHHHHh.."),
                 (5, "..HHHHHHHHHHHh.."), (6, "...HHHHHHHHHh..."),
                 (7, "....GgGGGGgG...."), (8, "...hG.G..G.Gh..."), (9, "....GGG..GGG....")],
        "up": [(1, ".....HHHHHH....."), (2, "....HHHLLHHH...."), (3, "...HHHLHHHHHh...")]
              + [(r, "..HHHHHHHHHHHh..") for r in range(4, 10)] + [(10, "...hHHHHHHHHh..."), (11, "....hhhhhhhh....")],
        "left": [(1, ".....HHHHHH....."), (2, "....HHLLHHHH...."), (3, "...HHLHHHHHHh..."), (4, "..HHHHHHHHHHHh.."),
                 (5, "..HHHHHHHHHHHh.."), (6, "...HH..HHHHHh..."), (7, "...GgGGGGHHh...."), (8, "...G.G..HHh....."),
                 (9, "...GGG..........")],
    },
}

# Trang phục: đè lên thân theo hướng. I áo trong, z đường may/khoá, K cà vạt, k thắt lưng, D d balo
OUTFIT = {
    "minh": {"down": [(r, ".......II.......") for r in range(13, 18)],
             "left": [(r, ".....I..........") for r in range(13, 18)]},
    "vy": {"down": [(19, "....TTTTTTtt...."), (20, "....TTTTTTtt....")] + [(r, ".......z........") for r in range(13, 21)],
           "up": [(19, "....TTTTTTtt...."), (20, "....TTTTTTtt....")],
           "left": [(19, ".....TTTTTt....."), (20, ".....TTTTTt.....")]},
    "lan": {"down": [(14, "........z......."), (16, "........z......."), (18, "....TTTTTTtt....")],
            "up": [(18, "....TTTTTTtt....")],
            "left": [(18, ".....TTTTTt.....")]},
    "tuan": {"down": [(13, ".......KK......."), (14, ".......K........"), (15, ".......K........"), (16, ".......K........"),
                      (18, "....kkkkkkkk....")],
             "up": [(18, "....kkkkkkkk....")],
             "left": [(13, ".....K.........."), (14, ".....K.........."), (15, ".....K.........."), (18, ".....kkkkkk.....")]},
    "khoa": {"down": [(r, ".....d....d.....") for r in range(13, 19)],
             "up": [(13, "....dDDDDDDd...."), (14, "....DDDDDDDd...."), (15, "....DDddDDDd...."), (16, "....DDDDDDDd...."),
                    (17, "....DDDDDDDd...."), (18, "....dddddddd....")],
             "left": [(13, "..........Dd...."), (14, "..........DDd..."), (15, "..........DDd..."), (16, "..........DDd..."),
                      (17, "..........DDd..."), (18, "..........dd....")]},
}

SKIN, SKIN_SH = (238, 196, 158), (208, 150, 116)
COMMON = {"S": SKIN, "s": SKIN_SH, "N": SKIN, "n": SKIN_SH, "E": (36, 26, 32), "B": (238, 152, 132),
          "M": (176, 94, 84), "G": (34, 34, 42), "g": (186, 220, 236)}

CHARS = {
    "minh": dict(H=(30, 28, 40), L=(92, 96, 128), T=(48, 68, 124), I=(236, 236, 242), P=(54, 60, 84), F=(34, 32, 38)),
    "vy": dict(H=(96, 56, 40), L=(156, 100, 66), T=(238, 188, 58), z=(196, 146, 40), P=(52, 46, 62), F=(240, 240, 238),
               R=(228, 62, 58)),
    "lan": dict(H=(26, 24, 32), L=(72, 74, 100), T=(66, 126, 90), z=(36, 70, 50), P=(36, 36, 44), F=(112, 76, 52),
                R=(214, 60, 60), X=(226, 206, 150)),
    "tuan": dict(H=(46, 34, 30), L=(118, 92, 76), T=(238, 238, 244), K=(164, 36, 48), k=(46, 40, 46), P=(90, 94, 108),
                 F=(26, 24, 28)),
    "khoa": dict(H=(32, 30, 36), L=(92, 92, 114), T=(142, 132, 86), P=(74, 80, 64), F=(100, 66, 42), D=(104, 82, 58)),
}


def palette(c):
    p = dict(COMMON)
    p.update({"H": c["H"], "h": shade(c["H"], 0.68), "L": c["L"],
              "T": c["T"], "t": shade(c["T"], 0.78), "A": shade(c["T"], 0.94), "a": shade(c["T"], 0.72),
              "U": mix(c["T"], (255, 250, 235), 0.22),
              "P": c["P"], "p": shade(c["P"], 0.74), "F": c["F"], "f": shade(c["F"], 0.7)})
    for key in ("I", "z", "R", "K", "k"):
        if key in c:
            p[key] = c[key]
    if "X" in c:
        p.update({"X": c["X"], "x": shade(c["X"], 0.76), "Y": mix(c["X"], (255, 250, 230), 0.4)})
    if "D" in c:
        p.update({"D": c["D"], "d": shade(c["D"], 0.7)})
    return p


def grid_apply(g, rows):
    for r, line in rows:
        assert len(line) == W, (r, line, len(line))
        row = list(g[r])
        for x, ch in enumerate(line):
            if ch != ".":
                row[x] = ch
        g[r] = "".join(row)


def shift_rows(g, r0, r1, dx):
    for r in range(r0, r1 + 1):
        line = g[r]
        g[r] = ("." * dx + line[:W - dx]) if dx > 0 else (line[-dx:] + "." * (-dx))


def compose(name, direction, frame):
    """direction: down / up / left; frame: 0, 1, 2, 'atk', 'hurt'"""
    base = list(B_LEFT if direction == "left" else B_DOWN)
    for line in base:
        assert len(line) == W
    if direction == "up":  # sau lưng: không có mặt
        base = [l.replace("E", "S").replace("B", "S").replace("M", "S") for l in base]
    steps = L_STEP if direction == "left" else D_STEP
    if frame in steps:
        grid_apply(base, sorted(steps[frame].items()))
    grid_apply(base, OUTFIT[name].get(direction, []))
    grid_apply(base, HAIR[name][direction])
    if frame == "atk":
        shift_rows(base, 0, 12, -1)  # ngả người về trước
    elif frame == "hurt":
        shift_rows(base, 0, 12, 1)  # bật đầu ra sau
        shift_rows(base, 13, 18, 1)
        base = [l.replace("E", "S") for l in base]
        row = list(base[8])
        for x in range(W):  # mắt nhắm: một vạch
            if base[7][x] == "S" and row[x] == "S" and 3 <= x <= 5 and B_LEFT[7][x - 1 if x > 0 else 0] == "E":
                row[x] = "E"
        base[8] = "".join(row)
    return base


def render(g, pal):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = img.load()
    for y in range(H):
        first_t = None
        for x in range(W):
            ch = g[y][x]
            if ch == ".":
                continue
            if ch == "T" and first_t is None:  # mép sáng của áo (sáng từ trái)
                first_t = x
                c = pal["U"]
            else:
                c = pal.get(ch, (255, 0, 255))
            px[x, y] = c + (255,)
    # viền màu: lấy màu tối của chất liệu ngay cạnh
    src = img.copy().load()
    for y in range(H):
        for x in range(W):
            if src[x, y][3]:
                continue
            nb = [src[x + dx, y + dy] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                  if 0 <= x + dx < W and 0 <= y + dy < H and src[x + dx, y + dy][3]]
            if nb:
                darkest = min(nb, key=lambda c: c[0] + c[1] + c[2])
                px[x, y] = mix(shade(darkest, 0.42), (26, 18, 26), 0.45) + (255,)
    return img


def make(name, direction, frame):
    return render(compose(name, direction, frame), palette(CHARS[name]))


def main():
    rows = []
    for name in CHARS:
        row = []
        for d in ("down", "up", "left"):
            for f in (0, 1, 2):
                im = make(name, d, f)
                im.save(os.path.join(OUT, "%s_%s_%d.png" % (name, d, f)))
                row.append(im)
                if d == "left":
                    right = im.transpose(Image.FLIP_LEFT_RIGHT)
                    right.save(os.path.join(OUT, "%s_right_%d.png" % (name, f)))
        for pose in ("atk", "hurt"):
            im = make(name, "left", pose).transpose(Image.FLIP_LEFT_RIGHT)
            im.save(os.path.join(OUT, "%s_right_%s.png" % (name, pose)))
            row.append(im)
        rows.append(row)
    sc = 7
    sheet = Image.new("RGBA", (len(rows[0]) * (W * sc + 10) + 10, len(rows) * (H * sc + 10) + 10), (72, 98, 60, 255))
    for j, row in enumerate(rows):
        for i, im in enumerate(row):
            sheet.alpha_composite(im.resize((W * sc, H * sc), Image.NEAREST), (10 + i * (W * sc + 10), 10 + j * (H * sc + 10)))
    sheet.save(os.path.join(PREVIEW, "_walkers_preview.png"))


if __name__ == "__main__":
    main()
    print("done →", OUT)
