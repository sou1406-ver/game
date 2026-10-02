# Prompt tạo art trên ChatGPT

Theo quy tắc của agent-sprite-forge: nền magenta trơn để tách nền, lưới đều, cùng một nhân vật ở mọi ô, cùng cỡ, chân cùng một đường.

## Cách dùng

1. **Làm Minh trước** (prompt B). Khi Minh ra đúng mặt, đúng trang phục, đúng tỉ lệ, đúng kiểu pixel thì lấy ảnh đó làm **mẫu style** cho mọi nhân vật sau: tải nó lên kèm câu `Match the pixel art style, scale and level of detail of the attached style reference.`
2. Mỗi nhân vật mở **một cuộc chat riêng**. Nhân vật có ảnh concept trong `Assets/ArtSource/reference/concept/` (minh, vy, tuan, khoa) thì **tải ảnh concept lên kèm mọi prompt**, thêm câu: `Turn the character in the attached concept art into this sprite sheet. Keep the same face, hair, outfit and colors.`
3. Với mỗi nhân vật, tạo **ảnh trận (B)** trước. Khi làm A và C, tải thêm ảnh B lên để giữ đúng nhân vật.
4. Mỗi lần chỉ tạo **một tấm**. Nếu ảnh có chữ, có đường kẻ giữa các ô, nền không phải magenta trơn, có quầng sáng mờ lan ra nền, hoặc nhân vật đổi mặt hay đổi đồ giữa các ô thì tạo lại.
5. Lưu vào `Assets/ArtSource/reference/` đúng tên ghi ở từng mục (ví dụ `minh_battle.png`), rồi báo mình xử lý.

## Khối chung cho sprite (dùng với A, B, ma)

Dán vào **cuối** prompt A, B và prompt ma:

```
STYLE: crisp 2D pixel art for a Vietnamese rural folklore horror RPG. Compact adult RPG sprite proportions, approximately 2.5 heads tall. Clean dark outline, limited color palette, simple soft pixel shading, clearly visible square pixels, hard pixel edges, no anti-aliasing, no blur, no painterly rendering, no 3D rendering.

CHARACTER CONSISTENCY: The same exact character must appear in every cell. Preserve the same face, hairstyle, skin tone, body proportions, clothing, colors, accessories and overall silhouette in every frame. Do not redesign, reinterpret, age, or restyle the character between cells.

BACKGROUND: 100% solid flat chroma-key magenta #FF00FF covering every part of the image outside the character. No gradient, no environment, no floor, no texture, no shadow. Any glow, aura, mist or ghost-fire must be drawn as solid pixels with a hard edge, never as a soft halo blending into the background.

LAYOUT: evenly sized rectangular cells with identical dimensions. One pose/frame per cell. Equal spacing between cells. No visible grid lines, no borders, no separators, no frame outlines. Character fully inside each cell with clear magenta margin on every side. All characters stand on exactly the same horizontal baseline.

OUTPUT: sprite sheet only. No text, no labels, no numbers, no captions, no UI, no watermark.
```

---

## Nhân vật

Mỗi nhân vật dùng một đoạn `CHARACTER:` trong các prompt ở dưới.

- **minh** (có concept): `CHARACTER: Minh, Vietnamese young man, freelance tattoo artist, withdrawn and sleep-deprived, messy short black hair, dark circles under the eyes, frowning, long wooden prayer-bead necklace with a small bronze bell, dark navy button shirt with rolled sleeves, brown cloth sash belt with a leather pouch on the hip, dark trousers, worn dark shoes.`
- **vy** (có concept): `CHARACTER: Vy, Vietnamese young woman, motorbike mechanic, tough and hot-tempered, scowling, short bob hair dyed copper-orange with visible black roots, mustard yellow t-shirt, dark grey work trousers, a small brass bell hanging from her belt, worn grey sneakers.`
- **lan** (chưa có concept, trang phục chưa chốt trong GDD): `CHARACTER: Lan, Vietnamese young woman, farmer who sells herbal medicine, tired and patient, long black hair tied back, green áo bà ba (traditional Vietnamese blouse), wide dark trousers, plastic sandals, small cloth herb pouch.`
- **tuan** (có concept): `CHARACTER: Tuấn, Vietnamese young man, unemployed office worker keeping up appearances, slim and tired, messy short black hair, charcoal knit sweater vest over a wrinkled white shirt, loosened dark red tie, old company ID badge on a blue lanyard, pens in the shirt pocket, grey dress trousers, brown leather shoes.`
- **khoa** (có concept): `CHARACTER: Khoa, Vietnamese young man, factory mechanic, muscular with grease stains on his arms, practical and blunt, short black hair, black rectangular glasses, a pencil tucked behind one ear, sage green tank top, dark olive work trousers with a brown belt, brown work boots.`
- **phong** (NPC): `CHARACTER: Phong, Vietnamese young man, keeper of an abandoned shrine, thin and gaunt, long messy black hair covering one eye, dark brown traditional shirt, wooden prayer beads, faint purple corruption veins on the neck, sandals.`
- **hai** (hồn ma): `CHARACTER: Hải, ghost of a drowned Vietnamese teenage boy, pale grey-blue skin, wet black hair stuck to the face, glowing blank eyes, torn white school shirt, dark shorts, barefoot, dripping water, a few small blue ghost-fire wisps drawn as solid pixel flames.`
- **ong_cu** (NPC): `CHARACTER: an old Vietnamese village man, bald top with thin grey hair at the sides, white beard, brown traditional jacket, dark trousers, slightly hunched.`

Dấu hiệu phân biệt cần giữ: người sống bình thường; Hải có lửa ma xanh (hồn ma); Phong có vết tha hoá tím (người bị tha hoá).

---

## A. Đi lại ngoài làng: `<tên>_walk.png`

Không cần hướng PHẢI: game tự lật hướng TRÁI.

```
Create a 4x3 sprite sheet (4 columns, 3 rows) of the character walking in a compact top-down RPG view.

Row 1: walking DOWN, facing the viewer — 4 sequential walk-cycle frames.
Row 2: walking LEFT, side view facing left — 4 sequential walk-cycle frames.
Row 3: walking UP, back view — 4 sequential walk-cycle frames.

For every row, frame 1 is the neutral standing pose and frames 2–4 show a simple walking cycle with alternating legs and natural arm movement.

All four frames within each row must depict the exact same character with identical body proportions, clothing, colors, face, hairstyle and accessories. Only the limb positions should change between frames. Do not redesign or reinterpret the character between frames.

Small full-body gameplay sprite. Keep the entire character visible in every cell.

CHARACTER: ...
(khối chung cho sprite)
```

## B. Trong trận: `<tên>_battle.png`

```
Create a 2x2 sprite sheet for a side-view turn-based RPG combat system.

The character faces RIGHT in every cell and is shown full-body. The combat sprite is larger and more detailed than the walking sprite.

Cell 1, top-left: ready combat stance.
Cell 2, top-right: same ready stance with a very subtle breathing variation.
Cell 3, bottom-left: attacking, lunging forward toward the RIGHT. Body movement only, with no weapon trails, slash effects, magic effects or particles.
Cell 4, bottom-right: hurt reaction, recoiling backward with eyes closed.

Keep the exact same head, face, hairstyle, body proportions, clothing silhouette, colors and accessories in all four cells. Do not change the character design between poses.

CHARACTER: ...
(khối chung cho sprite)
```

## C. Chân dung: `<tên>_portrait.png`

Không dùng khối chung cho sprite: chân dung cần mặt đẹp và biểu cảm, không bị ép tỉ lệ 2.5 đầu. Game tự vẽ nền tối phía sau.

```
Create a 2x2 grid of pixel art bust portraits (head and shoulders, front view) of the same character for dialogue and UI.
Cell 1: neutral. Cell 2: angry. Cell 3: worried. Cell 4: afraid.

STYLE: detailed pixel art portrait, expressive face, clean dark outline, limited palette, visible square pixels, hard edges, no blur.
CONSISTENCY: same face, hairstyle, skin tone, clothing and accessories in all four cells; only the expression changes.
BACKGROUND: each cell contains only the character bust against 100% solid flat magenta #FF00FF. No panel, no frame, no gradient, no shadow.
LAYOUT: equal square cells, the bust centered and the same size in every cell, no grid lines, no borders.
OUTPUT: no text, no labels, no watermark.

CHARACTER: ...
```

---

## Ma (trong trận, quay sang trái): `<tên>_battle.png`

Dùng prompt **B** nhưng thay hai chỗ: `faces RIGHT` thành `faces LEFT`, `lunging forward toward the RIGHT` thành `lunging forward toward the LEFT`.

- **ma_doi**: `CHARACTER: Ma đói, hungry ghost from Vietnamese folklore, emaciated green-grey skin, oversized bald head, huge mouth with jagged teeth, sunken yellow eyes, visible ribs, bloated belly, long thin arms with claws, torn loincloth.`
- **ma_nuoc**: `CHARACTER: Ma nước, female water ghost, very long wet black hair hiding most of the face, pale bluish skin, tattered white dress, floating, lower body fading into ragged mist drawn as solid pixels, dripping water, long pale fingers reaching forward.`
- **ma_nhen**: `CHARACTER: Ma nhện, giant black-purple spider with a pale human face for a head, long black hair hanging over the face, red eyes, red markings on the abdomen, eight jointed legs.`
