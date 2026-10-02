# Prompt tạo art trên ChatGPT

Theo quy tắc của agent-sprite-forge: nền magenta trơn để tách nền, lưới đều, cùng một nhân vật ở mọi ô, cùng cỡ, chân cùng một đường.

## Cách dùng

1. Mỗi nhân vật mở **một cuộc chat riêng**. Nếu nhân vật có ảnh concept trong `Assets/ArtSource/reference/concept/` (hiện có minh, vy, tuan, khoa), **tải ảnh concept lên kèm mọi prompt** và thêm câu: `Turn the character in the attached concept art into this sprite sheet. Keep the same face, hair, outfit and colors.`
   Tạo **ảnh trận (B)** trước. Với các ảnh sau (A, C), tải thêm ảnh B lên để giữ đúng nhân vật.
2. Mỗi lần chỉ tạo **một tấm**, đúng một prompt.
3. Nếu ảnh ra có chữ, có đường kẻ giữa các ô, nền không phải magenta trơn, hoặc nhân vật đổi mặt hay đổi quần áo giữa các ô thì tạo lại.
4. Lưu ảnh vào `Assets/ArtSource/reference/` theo tên ghi ở từng mục, ví dụ `vy_walk.png`, rồi báo mình xử lý.

## Khối chung

Dán khối này vào **cuối** mọi prompt bên dưới:

```
STYLE: crisp 2D pixel art for a top-down Vietnamese rural horror RPG (Stardew Valley proportions, adult characters ~2.5 heads tall), clean dark outline, limited palette, soft shading, visible square pixels, no anti-aliasing blur.
BACKGROUND: 100% solid flat magenta #FF00FF everywhere. No gradient, no floor, no shadow on the background, no text, no labels, no numbers, no grid lines, no borders between cells.
LAYOUT: equal cells, one pose per cell, the same character in every cell with the same face, outfit, colors and body scale, fully inside the cell with magenta margin on all sides, feet on the same baseline.
```

---

## Nhân vật (mô tả lấy từ GDD)

Mỗi nhân vật dùng một đoạn `CHARACTER:` trong 3 loại ảnh ở dưới.

- **minh** (có concept): `CHARACTER: Minh, Vietnamese young man, freelance tattoo artist, withdrawn and sleep-deprived, messy short black hair, dark circles under the eyes, frowning, long wooden prayer-bead necklace with a small bronze bell, dark navy button shirt with rolled sleeves, brown cloth sash belt with a leather pouch on the hip, dark trousers, worn dark shoes.`
- **vy** (có concept): `CHARACTER: Vy, Vietnamese young woman, motorbike mechanic, tough and hot-tempered, scowling, short bob hair dyed copper-orange with visible black roots, mustard yellow t-shirt, dark grey work trousers, a small brass bell hanging from her belt, worn grey sneakers.`
- **lan**: `CHARACTER: Lan, Vietnamese young woman, farmer who sells herbal medicine, tired and patient, long black hair tied back, green áo bà ba (traditional Vietnamese blouse), wide dark trousers, plastic sandals, small cloth herb pouch.`
- **tuan** (có concept): `CHARACTER: Tuấn, Vietnamese young man, unemployed office worker keeping up appearances, slim and tired, messy short black hair, charcoal knit sweater vest over a wrinkled white shirt, loosened dark red tie, old company ID badge on a blue lanyard, pens in the shirt pocket, grey dress trousers, brown leather shoes.`
- **khoa** (có concept): `CHARACTER: Khoa, Vietnamese young man, factory mechanic, muscular with grease stains on his arms, practical and blunt, short black hair, black rectangular glasses, a pencil tucked behind one ear, sage green tank top, dark olive work trousers with a brown belt, brown work boots.`
- **phong** (NPC): `CHARACTER: Phong, Vietnamese young man, keeper of an abandoned shrine, thin and gaunt, long messy black hair covering one eye, dark brown traditional shirt, wooden prayer beads, faint purple corruption veins on the neck, sandals.`
- **hai** (hồn ma): `CHARACTER: Hải, ghost of a drowned Vietnamese teenage boy, pale grey-blue skin, wet black hair stuck to the face, glowing blank eyes, torn white school shirt, dark shorts, barefoot, dripping water, faint blue ghost-fire wisps around him.`
- **ong_cu** (NPC): `CHARACTER: an old Vietnamese village man, bald top with thin grey hair at the sides, white beard, brown traditional jacket, dark trousers, slightly hunched.`

---

## A. Đi lại ngoài làng: `<tên>_walk.png`

```
Create a 4x4 sprite sheet of the character walking, top-down RPG view.
Row 1: walking DOWN (facing the viewer), 4 frames of a walk cycle.
Row 2: walking LEFT (side view, facing left), 4 frames.
Row 3: walking RIGHT (side view, facing right), 4 frames.
Row 4: walking UP (back view), 4 frames.
Frame 1 of each row is a neutral standing pose; frames 2-4 alternate legs and swing arms. Small character, full body.
CHARACTER: ...
(khối chung)
```

## B. Trong trận: `<tên>_battle.png`

```
Create a 2x2 sprite sheet for side-view turn-based combat. The character faces RIGHT in every cell, full body, larger and more detailed than a map sprite.
Cell 1 (top-left): ready combat stance.
Cell 2 (top-right): same stance, slight breathing variation.
Cell 3 (bottom-left): attacking, lunging forward to the right (no slash effects, body only).
Cell 4 (bottom-right): hurt, recoiling backward, eyes shut.
CHARACTER: ...
(khối chung)
```

## C. Chân dung: `<tên>_portrait.png`

```
Create a 2x2 grid of pixel art bust portraits (head and shoulders, front view) of the same character, each on a plain dark background panel inside the cell.
Cell 1: neutral. Cell 2: angry. Cell 3: worried. Cell 4: afraid.
CHARACTER: ...
STYLE: crisp pixel art portrait, detailed face, clean outline, no text, no labels. BACKGROUND outside the panels: solid magenta #FF00FF.
```

---

## Ma (trong trận, quay sang trái): `<tên>_battle.png`

Dùng prompt **B** nhưng thay hai chỗ: `faces RIGHT` thành `faces LEFT`, `lunging forward to the right` thành `lunging forward to the left`.

- **ma_doi**: `CHARACTER: Ma đói, hungry ghost from Vietnamese folklore, emaciated green-grey skin, oversized bald head, huge mouth with jagged teeth, sunken yellow eyes, visible ribs, bloated belly, long thin arms with claws, torn loincloth.`
- **ma_nuoc**: `CHARACTER: Ma nước, female water ghost, very long wet black hair hiding most of the face, pale bluish skin, tattered white dress, floating, lower body fading into mist and dripping water, long pale fingers reaching forward.`
- **ma_nhen**: `CHARACTER: Ma nhện, giant black-purple spider with a pale human face for a head, long black hair hanging over the face, red eyes, red markings on the abdomen, eight jointed legs.`
