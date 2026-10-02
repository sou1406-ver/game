"""Sprite đi lại 16x32 (khổ người lớn kiểu Stardew) cho 5 người chơi được và 3 NPC (Phong, Hải, Ông cụ).
Dùng cả ngoài làng lẫn trong trận. Vẽ tay bằng lưới chữ: khung người theo hướng + lớp tóc, trang phục riêng,
đổ bóng 3 tông, viền màu theo chất liệu bên cạnh.
Chạy: python draw_walkers.py → Assets/Resources/Walk/<tên>_<hướng>_<khung>.png
  hướng: down, up, left, right · khung: 0 đứng, 1 bước trái, 2 bước phải · thêm right_atk, right_hurt (trận)."""
from PIL import Image
import os

W, H = 16, 32
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


# ---------- Khung người ----------
# S da, s da tối, E mắt, M miệng, N tay, n tay tối, T áo, t áo tối, A tay áo sáng, a tay áo tối,
# k thắt lưng, P quần, p quần tối, F giày, f giày tối

B_DOWN = [
    "................",
    "................",
    ".....SSSSSS.....",
    "....SSSSSSSS....",
    "....SSSSSSSS....",
    "....SSSSSSSs....",
    "...SSSESSESSs...",
    "...SSSESSESSs...",
    "....SSSSsSSs....",
    ".....SSMMSs.....",
    "......sSSs......",
    ".......ss.......",
    "...TTTTTTTTTt...",
    "..AaTTTTTTTtaa..",
    "..AaTTTTTTTtaa..",
    "..AaTTTTTTTtaa..",
    "..AaTTTTTTTtaa..",
    "..AaTTTTTTTtaa..",
    "..AaTTTTTTTtaa..",
    "..AaTTTTTTTtaa..",
    "..AaTTTTTTTtaa..",
    "..NNkkkkkkkknn..",
    "....PPPPPPPp....",
    "....PPPpPPPp....",
    "....PPPpPPPp....",
    "....PPPpPPPp....",
    "....PPPpPPPp....",
    "....PPPpPPPp....",
    "....PPPpPPPp....",
    "....PPP..PPp....",
    "...FFFf..FFFf...",
    "................",
]
D_STEP = {
    1: {20: "..NNTTTTTTTtaa..", 21: "....kkkkkkkknn..", 28: "...FFFf.PPPp....", 29: "........PPPp....",
        30: ".........FFFf..."},
    2: {20: "..AaTTTTTTTtnn..", 21: "..NNkkkkkkkk....", 28: "....PPPp.FFFf...", 29: "....PPPp........",
        30: "...FFFf........."},
}

B_LEFT = [
    "................",
    "................",
    ".....SSSSSS.....",
    "....SSSSSSSS....",
    "....SSSSSSSS....",
    "....SSSSSSSs....",
    "....SESSsSSs....",
    "....SESSsSSs....",
    "...SSSSSSSSs....",
    "....SMSSSSs.....",
    ".....sSSSs......",
    ".......ss.......",
    ".....TTTTTt.....",
    ".....TTaaTt.....",
    ".....TTaaTt.....",
    ".....TTaaTt.....",
    ".....TTaaTt.....",
    ".....TTaaTt.....",
    ".....TTaaTt.....",
    ".....TTaaTt.....",
    ".....TTaaTt.....",
    ".....kkNNkk.....",
    "......PPPp......",
    "......PPPp......",
    "......PPPp......",
    "......PPPp......",
    "......PPPp......",
    "......PPPp......",
    "......PPPp......",
    "......PPPp......",
    ".....FFFFf......",
    "................",
]
ARM_FWD = {13: ".....TTaaTt.....", 14: ".....TaaTTt.....", 15: ".....aaTTTt.....", 16: "....aaTTTTt.....",
           17: "....aTTTTTt.....", 18: "...aaTTTTTt.....", 19: "...NNTTTTTt.....", 20: ".....TTTTTt.....",
           21: ".....kkkkkk....."}
ARM_BACK = {13: ".....TTaaTt.....", 14: ".....TTTaaT.....", 15: ".....TTTTaa.....", 16: ".....TTTTTaa....",
            17: ".....TTTTTta....", 18: ".....TTTTTtaa...", 19: ".....TTTTTtNN...", 20: ".....TTTTTt.....",
            21: ".....kkkkkk....."}
LEGS_A = {22: "......PPPp......", 23: ".....PPPPpp.....", 24: ".....PPP.pp.....", 25: "....PPP...pp....",
          26: "....PPP...pp....", 27: "...PPP....pp....", 28: "...PPP.....pp...", 29: "..PPP......pp...",
          30: ".FFFf......ff..."}
LEGS_B = {22: "......PPPp......", 23: ".....ppPPPP.....", 24: ".....pp.PPP.....", 25: "....pp...PPP....",
          26: "....pp...PPP....", 27: "...pp....PPP....", 28: "...pp.....PPP...", 29: "..pp......PPP...",
          30: ".ff......FFFf..."}
L_STEP = {
    1: {**ARM_FWD, **LEGS_A},
    2: {**ARM_BACK, **LEGS_B},
    "atk": {13: ".....TTTTTt.....", 14: ".....TTTTTt.....", 15: ".NNaaaTTTTt.....", 16: ".....TTTTTt.....",
            17: ".....TTTTTt.....", 18: ".....TTTTTt.....", 19: ".....TTTTTt.....", 20: ".....TTTTTt.....",
            21: ".....kkkkkk.....", **LEGS_A},
}

# ---------- Tóc, mũ (dòng, chuỗi 16 ký tự; '.' = giữ nguyên) ----------
# H tóc, h tóc tối, L tóc sáng, R điểm nhấn, X Y x nón lá, G gọng kính, g tròng kính


def rows(r0, r1, line):
    return [(r, line) for r in range(r0, r1 + 1)]


HAIR = {
    "minh": {
        "down": [(0, "......H.HH......"), (1, ".....HHHHHHH...."), (2, "....HHLLHHHHH..."), (3, "...HHLHHHHHHHh.."),
                 (4, "...HHHHHHHHHHh.."), (5, "...HH.HHH.HHhh.."), (6, "....H......h....")],
        "up": [(0, "......H.HH......"), (1, ".....HHHHHHH...."), (2, "....HHHLLHHHH..."), (3, "...HHHLHHHHHHh..")]
              + rows(4, 8, "...HHHHHHHHHHh..") + [(9, "....HHHHHHHHh..."), (10, ".....hhhhhh.....")],
        "left": [(0, ".......H.HH....."), (1, "......HHHHHHH..."), (2, ".....HHLLHHHHH.."), (3, "....HHLHHHHHHh.."),
                 (4, "...HHHHHHHHHHh.."), (5, "...HH.HHHHHHHh.."), (6, "....H....HHHh..."), (7, ".........HHHh..."),
                 (8, ".........HHh....")],
    },
    "vy": {
        "down": [(1, ".....HHHHHH....."), (2, "....HLLHHHHH...."), (3, "...HLHHHHHHHh..."), (4, "...HHHHHHHHHHh.."),
                 (5, "...HHHHHHHHHhh.."), (6, "...HH......hhR..")] + rows(7, 9, "...HH......hh...")
                + [(10, "...HH.......hh.."), (11, "...hh.......hh.."), (12, "...h.........h..")],
        "up": [(1, ".....HHHHHH....."), (2, "....HHHLLHHH...."), (3, "...HHHLHHHHHh..."), (4, "...HHHHHHHHHHh.."),
               (5, "...HHHHHHHHHHhR.")] + rows(6, 10, "...HHHHHHHHHHh..")
              + [(11, "...hHHHHHHHHhh.."), (12, "...hhhhhhhhhhh..")],
        "left": [(1, ".....HHHHHH....."), (2, "....HLLHHHHH...."), (3, "...HLHHHHHHHh..."), (4, "...HHHHHHHHHh..."),
                 (5, "...HHHHHHHHHh..."), (6, "...HH...HHHHhR.."), (7, "...H....HHHHh...")]
                + rows(8, 9, "........HHHHh...") + [(10, "........HHHHhh.."), (11, ".........hhhhh.."),
                                                    (12, "..........hh....")],
    },
    "lan": {
        "down": [(0, ".......XY......."), (1, "......XYXx......"), (2, ".....XYXXXx....."), (3, "....XYXXXXXx...."),
                 (4, "..XXXXXXXXXXxx.."), (5, ".xxxxxxxxxxxxxx."), (6, "...HH......hh..."), (7, "...H........h...")]
                + [(r, "...........H...." if r % 2 else "...........h....") for r in range(11, 20)]
                + [(20, "...........R....")],
        "up": [(0, ".......XY......."), (1, "......XYXx......"), (2, ".....XYXXXx....."), (3, "....XYXXXXXx...."),
               (4, "..XXXXXXXXXXxx.."), (5, ".xxxxxxxxxxxxxx.")] + rows(6, 10, "...HHHHHHHHHh...")
              + rows(11, 21, ".......Hh.......") + [(22, ".......RR.......")],
        "left": [(0, "........XY......"), (1, ".......XYXx....."), (2, "......XYXXXx...."), (3, ".....XYXXXXXx..."),
                 (4, "...XXXXXXXXXXxx."), (5, "..xxxxxxxxxxxxx."), (6, "........HHHHh..."), (7, "........HHHHh..."),
                 (8, ".........HHHh...")] + rows(9, 19, "..........Hh....") + [(20, "..........RR....")],
    },
    "tuan": {
        "down": [(1, ".....HHHHHHH...."), (2, "....HHHHHLLHh..."), (3, "...HHHHHLLHHHh.."), (4, "...HHHHHHHHHHh.."),
                 (5, "...HHHHH....hh.."), (6, "...H.........h..")],
        "up": [(1, ".....HHHHHHH...."), (2, "....HHHHHLLHh..."), (3, "...HHHHHLLHHHh..")]
              + rows(4, 8, "...HHHHHHHHHHh..") + [(9, "....HHHHHHHHh..."), (10, ".....hhhhhh.....")],
        "left": [(1, ".....HHHHHHH...."), (2, "....HHHHHLLHH..."), (3, "...HHHHLLHHHHh.."), (4, "...HHHHHHHHHHh.."),
                 (5, "...HHH..HHHHHh.."), (6, ".........HHHh..."), (7, ".........HHh....")],
    },
    "khoa": {
        "down": [(1, ".....HHHHHH....."), (2, "....HHLLHHHH...."), (3, "...HHLHHHHHHh..."), (4, "...HHHHHHHHHHh.."),
                 (5, ".....GGGGGG....."), (6, ".....G.GG.G....."), (7, ".....GgGGgG....."), (8, "......G..G......")],
        "up": [(1, ".....HHHHHH....."), (2, "....HHHLLHHH...."), (3, "...HHHLHHHHHh...")]
              + rows(4, 8, "...HHHHHHHHHHh..") + [(9, "....hHHHHHHhh..."), (10, ".....hhhhhh.....")],
        "left": [(1, ".....HHHHHH....."), (2, "....HHLLHHHH...."), (3, "...HHLHHHHHHh..."), (4, "...HHHHHHHHHh..."),
                 (5, "...HGGGHHHHHh..."), (6, "....G.GGGHHh...."), (7, "....G.G..HHh...."), (8, "....GGG.........")],
    },
    "phong": {  # tóc dài rối, che một bên mắt
        "down": [(1, ".....HHHHHH....."), (2, "....HLHHHHHHH..."), (3, "...HLHHHHHHHHh.."), (4, "...HHHHHHHHHHh.."),
                 (5, "...HHHH.HHHHHh.."), (6, "...HH...HHHHhh.."), (7, "...HH....HHHh..."), (8, "...H.....HHh...."),
                 (9, "...h......h....."), (10, "...h............")],
        "up": [(1, ".....HHHHHH....."), (2, "....HHHLHHHHH..."), (3, "...HHHLHHHHHHh..")]
              + rows(4, 10, "...HHHHHHHHHHh..") + [(11, "....hHHHHHHh...."), (12, ".....hhhhhh.....")],
        "left": [(1, ".....HHHHHH....."), (2, "....HLHHHHHHH..."), (3, "...HLHHHHHHHHh.."), (4, "...HHHHHHHHHHh.."),
                 (5, "...HHHHHHHHHHh.."), (6, "...HH...HHHHh..."), (7, "...H.....HHHh...")]
                + rows(8, 10, "........HHHHh...") + [(11, ".........hhh....")],
    },
    "hai": {  # tóc ướt bết thành sợi
        "down": [(1, ".....HHHHHH....."), (2, "....HHHHHHHH...."), (3, "...HHHHHHHHHh..."), (4, "...HHHHHHHHHHh.."),
                 (5, "...HH.H.HH.Hh..."), (6, "...H..H..H..h..."), (7, "...H........h...")],
        "up": [(1, ".....HHHHHH....."), (2, "....HHHHHHHH...."), (3, "...HHHHHHHHHh...")]
              + rows(4, 8, "...HHHHHHHHHHh..") + [(9, "....H.HH.HHh...."), (10, ".....h..h.h.....")],
        "left": [(1, ".....HHHHHH....."), (2, "....HHHHHHHH...."), (3, "...HHHHHHHHHh..."), (4, "...HHHHHHHHHh..."),
                 (5, "...H.H.HHHHHh..."), (6, "...H....HHHHh..."), (7, ".........HHHh..."), (8, ".........H.h....")],
    },
    "ong_cu": {  # tóc bạc thưa, trán hói, râu
        "down": [(2, ".....I....I....."), (3, "....HI....IH...."), (4, "...HH......Hh..."), (5, "...HH......Hh..."),
                 (6, "...H........h..."), (9, ".....IIIII......"), (10, "......IIII......"), (11, ".......II.......")],
        "up": [(2, ".....SSSSSS....."), (3, "....HSSSSSSH...."), (4, "...HHHSSSSHHh...")]
              + rows(5, 8, "...HHHHHHHHHHh..") + [(9, "....HHHHHHHHh...")],
        "left": [(3, ".........IH....."), (4, "........HHHh...."), (5, "........HHHHh..."), (6, ".........HHHh..."),
                 (7, ".........HHh...."), (9, "....IIII........"), (10, ".....III........"), (11, "......I.........")],
    },
}

# ---------- Trang phục (đè lên thân) ----------
# O viền áo, I áo trong / râu, K cà vạt, z túi / cúc, D d balo, V vết tha hoá, w W lửa ma
OUTFIT = {
    "minh": {"down": rows(12, 20, ".......OO.......") + [(12, "...TTTTOOTTTt...")] + [(21, "..NNTTTOOTTtnn..")]
                     + rows(22, 24, "....TTTOOTTt....") + [(24, "....OOOOOOOO....")],
             "up": [(21, "..NNTTTTTTTtnn..")] + rows(22, 23, "....TTTTTTTt....") + [(24, "....OOOOOOOO....")],
             "left": rows(12, 20, ".....O..........") + [(21, ".....OTNNTt.....")] + rows(22, 23, ".....OTTTTt.....")
                     + [(24, ".....OOOOOO.....")]},
    "vy": {"down": [(12, "...TTTTIITTTt...")],
           "left": [(12, ".....ITTTTt.....")]},
    "lan": {"down": [(14, "........z......."), (17, "........z......."), (20, "........z......."), (21, "..NNTTTTTTTtnn..")]
                    + rows(22, 23, "....TTTTTTTt....") + [(24, "....TT....Tt....")],
            "up": [(21, "..NNTTTTTTTtnn..")] + rows(22, 23, "....TTTTTTTt....") + [(24, "....TT....Tt....")],
            "left": [(21, ".....TTNNTt.....")] + rows(22, 24, ".....TTTTTt.....")},
    "tuan": {"down": [(12, "...TTTIKKITTt..."), (13, "..AaTTIKKITtaa.."), (14, "..AaTTIKKITtaa..")]
                     + rows(15, 18, "..AaTTTKKTTtaa..") + [(19, "..AaTTTKTTTtaa..")],
             "left": rows(12, 19, ".....I..........") + rows(12, 17, "......K.........")},
    "khoa": {"down": rows(12, 20, ".....d....d.....") + [(16, "....zz....zz...."), (17, "....zz....zz....")],
             "up": [(12, "....dDDDDDDd....")] + rows(13, 19, "....DDDDDDDd....") + [(15, "....DDddDDDd...."),
                                                                                  (20, "....dddddddd....")],
             "left": [(12, "..........Dd....")] + rows(13, 19, "..........DDd...") + [(20, "..........dd...."),
                                                                                    (16, ".....z..........")]},
    "phong": {"down": [(10, "......sSsV......"), (11, ".......sV......."), (12, "...TTTTTTTTVt..."),
                       (21, "..NNkkkkkkkkVn..")],
              "left": [(10, ".....sSSVs......"), (11, ".......sV......."), (12, ".....TTTTVt.....")]},
    "hai": {"down": [(1, "..w..........w.."), (9, "...............W"), (14, "W..............."),
                     (22, "....PPPPPPPp....")] + rows(23, 25, "....PPPpPPPp....") + rows(26, 29, "....SSS..SSs....")
                    + [(30, "...SSSs..SSSs...")] + rows(13, 19, "..SsTTTTTTTtss..") + [(20, "..NNTTTTTTTtnn..")],
            "up": rows(23, 25, "....PPPpPPPp....") + rows(26, 29, "....SSS..SSs....") + [(30, "...SSSs..SSSs...")]
                  + rows(13, 19, "..SsTTTTTTTtss..") + [(20, "..NNTTTTTTTtnn..")] + [(2, ".w............w.")],
            "left": rows(26, 29, "......SSSs......") + [(30, ".....SSSSs......")] + [(1, ".w.........w...."),
                                                                                    (16, "..............w.")]},
    "ong_cu": {"down": [(21, "..NNTTTTTTTtnn..")] + rows(22, 23, "....TTTTTTTt....") + rows(14, 20, ".......z........"),
               "up": [(21, "..NNTTTTTTTtnn..")] + rows(22, 23, "....TTTTTTTt...."),
               "left": [(21, ".....TTNNTt.....")] + rows(22, 23, ".....TTTTTt.....")},
}

SKIN, SKIN_SH = (236, 192, 156), (204, 146, 114)
COMMON = {"E": (34, 24, 32), "M": (172, 88, 80), "G": (30, 30, 38), "g": (196, 226, 240)}

CHARS = {
    "minh": dict(H=(28, 26, 38), L=(88, 92, 128), T=(86, 60, 128), O=(156, 126, 196), P=(40, 40, 52), F=(28, 26, 32)),
    "vy": dict(H=(196, 86, 46), L=(236, 140, 84), T=(234, 182, 52), I=(250, 236, 196), P=(44, 52, 84),
               F=(240, 240, 238), R=(70, 140, 210)),
    "lan": dict(H=(24, 22, 30), L=(70, 72, 98), T=(62, 124, 88), z=(196, 186, 140), P=(30, 30, 38), F=(112, 76, 52),
                R=(214, 60, 60), X=(226, 206, 150)),
    "tuan": dict(H=(48, 36, 30), L=(124, 96, 78), T=(62, 66, 84), I=(240, 240, 244), K=(170, 36, 48),
                 P=(92, 96, 110), F=(24, 22, 26), k=(30, 28, 32)),
    "khoa": dict(H=(30, 28, 34), L=(90, 92, 116), T=(120, 118, 70), z=(92, 90, 52), P=(80, 84, 64), F=(104, 70, 44),
                 D=(110, 84, 56), G=(120, 104, 88)),
    "phong": dict(H=(20, 18, 24), L=(66, 60, 86), T=(58, 46, 44), P=(34, 32, 38), F=(22, 20, 24), V=(112, 60, 148)),
    "hai": dict(H=(22, 28, 36), L=(64, 82, 104), T=(222, 230, 234), P=(40, 56, 98), F=(190, 200, 198),
                S=(198, 208, 204), E=(12, 12, 18), w=(120, 190, 236), W=(206, 238, 255), ghost=True),
    "ong_cu": dict(H=(186, 186, 192), L=(222, 222, 228), T=(86, 70, 58), z=(180, 160, 110), I=(222, 222, 226),
                   P=(60, 56, 52), F=(40, 34, 30), S=(222, 180, 144)),
}


def palette(c):
    skin = c.get("S", SKIN)
    p = dict(COMMON)
    p.update({"S": skin, "s": shade(skin, 0.86), "N": skin, "n": shade(skin, 0.86),
              "H": c["H"], "h": shade(c["H"], 0.7), "L": c["L"],
              "T": c["T"], "t": shade(c["T"], 0.78), "A": shade(c["T"], 0.95), "a": shade(c["T"], 0.74),
              "U": mix(c["T"], (255, 250, 235), 0.2),
              "P": c["P"], "p": shade(c["P"], 0.74), "F": c["F"], "f": shade(c["F"], 0.7),
              "k": c.get("k", shade(c["P"], 0.6))})
    for key in ("I", "z", "R", "K", "O", "V", "w", "W", "E", "G"):
        if key in c:
            p[key] = c[key]
    if "X" in c:
        p.update({"X": c["X"], "x": shade(c["X"], 0.76), "Y": mix(c["X"], (255, 250, 230), 0.4)})
    if "D" in c:
        p.update({"D": c["D"], "d": shade(c["D"], 0.68)})
    return p


def grid_apply(g, rws):
    for r, line in rws:
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
    base = list(B_LEFT if direction == "left" else B_DOWN)
    assert len(base) == H and all(len(l) == W for l in base)
    if direction == "up":
        base = [l.replace("E", "S").replace("M", "S") for l in base]
    steps = L_STEP if direction == "left" else D_STEP
    if frame in steps:
        grid_apply(base, sorted(steps[frame].items()))
    grid_apply(base, OUTFIT.get(name, {}).get(direction, []))
    grid_apply(base, HAIR[name][direction])
    if frame == "atk":
        shift_rows(base, 0, 11, -1)
    elif frame == "hurt":
        eye_x = [x for x in range(W) if base[6][x] == "E"]
        shift_rows(base, 0, 11, 1)
        shift_rows(base, 12, 21, 1)
        for r in (6, 7):
            base[r] = base[r].replace("E", "S")
        for x in eye_x:  # mắt nhắm: vạch ngang
            row = list(base[7])
            for xx in (x, x + 1, x + 2):
                if 0 <= xx < W and row[xx] == "S":
                    row[xx] = "E"
            base[7] = "".join(row)
    return base


def render(g, pal, ghost=False):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = img.load()
    glow = set()
    for y in range(H):
        first_t = None
        for x in range(W):
            ch = g[y][x]
            if ch == ".":
                continue
            if ch in "wW":
                glow.add((x, y))
                continue
            if ch == "T" and first_t is None:
                first_t = x
                c = pal["U"]
            else:
                c = pal.get(ch, (255, 0, 255))
            px[x, y] = c + (255,)
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
    if ghost:  # hồn ma: hơi trong, lửa ma xanh toả sáng
        for y in range(H):
            for x in range(W):
                r, gg, b, a = px[x, y]
                if a:
                    px[x, y] = (r, gg, b, 225)
        for (x, y) in glow:
            px[x, y] = pal["W"] + (255,)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < W and 0 <= ny < H and px[nx, ny][3] == 0:
                    px[nx, ny] = pal["w"] + (170,)
            if 0 <= y - 2 < H and px[x, y - 2][3] == 0:
                px[x, y - 2] = pal["w"] + (110,)
    return img


def make(name, direction, frame):
    c = CHARS[name]
    return render(compose(name, direction, frame), palette(c), c.get("ghost", False))


def main():
    sheet_rows = []
    for name in CHARS:
        row = []
        for d in ("down", "up", "left"):
            for f in (0, 1, 2):
                im = make(name, d, f)
                im.save(os.path.join(OUT, "%s_%s_%d.png" % (name, d, f)))
                row.append(im)
                if d == "left":
                    im.transpose(Image.FLIP_LEFT_RIGHT).save(os.path.join(OUT, "%s_right_%d.png" % (name, f)))
        for pose in ("atk", "hurt"):
            im = make(name, "left", pose).transpose(Image.FLIP_LEFT_RIGHT)
            im.save(os.path.join(OUT, "%s_right_%s.png" % (name, pose)))
            row.append(im)
        sheet_rows.append(row)
    sc = 5
    sheet = Image.new("RGBA", (len(sheet_rows[0]) * (W * sc + 8) + 8, len(sheet_rows) * (H * sc + 8) + 8), (54, 58, 70, 255))
    for j, row in enumerate(sheet_rows):
        for i, im in enumerate(row):
            sheet.alpha_composite(im.resize((W * sc, H * sc), Image.NEAREST), (8 + i * (W * sc + 8), 8 + j * (H * sc + 8)))
    sheet.save(os.path.join(PREVIEW, "_walkers_preview.png"))


if __name__ == "__main__":
    main()
    print("done →", OUT)
