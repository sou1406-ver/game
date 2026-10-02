# Ký Ức Bị Chôn — ghi chú cho Claude

Game indie của Tiến Giáp, làm một mình cùng AI cho tới bản demo. Unity 6.3 LTS (6000.3.25f1), template Universal 2D, project ở `G:\đồ án\My project`. Repo: https://github.com/sou1406-ver/game (nhánh `main`).

Thiết kế đầy đủ nằm ở `Docs/GDD.md`. Đọc file đó trước khi đổi gameplay hoặc cốt truyện.

## Cách làm việc với người dùng
- Trả lời bằng tiếng Việt, ngắn gọn, không văn hoa.
- Bám đúng ý người dùng nói. Không tự thêm cốt truyện hay lore: phần nào chưa có thì để chỗ trống, ghi chú lại và hỏi.
- Con số phải cụ thể. Số nào tự đặt (chưa có trong GDD) thì nói rõ là tự đặt.
- Bỏ phần thừa, không giữ lại chỉ cho đủ.
- Người dùng mới học Unity. Hướng dẫn thao tác Editor phải đi từng bước, ghi rõ tên menu và nút.
- Art do người dùng tạo bằng AI vẽ ảnh (ChatGPT). Không vẽ nhân vật, ma bằng code: lấy từ ảnh tham chiếu. Prompt mẫu ở `Docs/PROMPT_ART.md`.
- Sửa xong thì commit và đẩy lên git khi người dùng yêu cầu.

## Cấu trúc
```
Assets/Scripts/
  Data/        BalanceConfig, CharacterData, EnemyData, ItemData   (ScriptableObject, mọi số cân bằng)
  Combat/      Combatant, CombatRules (luật + sự kiện Fx), Commands (Command Pattern), EnemyBrain
  Village/     VillageConfig (số liệu làng), VillageState (logic thuần), VillageMap (đọc World/world.json),
               DayController (làng đi lại kiểu Stardew + bảng thao tác)
  BattleController.cs   trận đấu nhìn ngang + UI trận (IMGUI)
  UiSkin.cs             khung UI pixel dùng chung; PixelTex.Load nạp ảnh và ép lọc Point
  Editor/PixelArtImporter.cs   ảnh trong các thư mục pixel art → Point, không nén, giữ kích thước
Assets/Resources/
  Walk/       sprite đi 24x36: <tên>_<down|up|left|right>_<0|1|2>, right_atk, right_hurt (dùng cả trong trận)
  Portraits/  chân dung 48x48
  Battle/     ma (ma_doi, ma_nuoc, ma_nhen _0/_1), nền trận backdrop.png, icon_*
  World/      map làng: ground, objects (atlas), water_0..2, minimap, world.json (va chạm, cửa, vật thể)
  Items/      icon 24x24
  UI/         khung 9-slice
Assets/ArtSource/   script Python (Pillow) + reference/ (ảnh tham chiếu, concept/)
Docs/GDD.md, Docs/PROMPT_ART.md
```
Scene: một GameObject `Battle` gắn `BattleController` và `DayController`. Không dùng prefab, Canvas hay sprite renderer: mọi thứ vẽ bằng IMGUI trong `OnGUI`.

## Quy ước code
- Namespace `KyUc`. Chú thích tiếng Việt, ngắn.
- Everything Is Data: số liệu nằm trong ScriptableObject có `Create...()` trả bản mặc định. Ô Inspector để trống thì code tự dùng mặc định.
- Tên file ảnh = tên hiển thị bỏ dấu, khoảng trắng thành `_`, theo `BattleController.SpriteKey()`. Nạp ảnh bằng `PixelTex.Load("Thư mục/" + key)`.
- Thế giới và sân trận vẽ theo pixel màn hình với tỉ lệ nguyên (làng ~270 dòng, trận ~200 dòng); UI vẽ theo toạ độ ảo cao 720.
- Luật không phụ thuộc UI: UI nghe `CombatRules.Fx`.
- Code phải chạy được trên C# 9 của Unity. Không dùng gói ngoài.

## Art (ArtSource)
- `extract_ref.py`: cắt sprite đi lại, chân dung, ma từ `reference/` → Walk, Portraits, Battle.
- `draw_world.py`: map làng, va chạm, cửa → World. Dời địa điểm: sửa `SPOTS`.
- `draw_battle.py`: nền trận + icon. `draw_items.py`: icon đồ. `draw_ui.py`: khung UI.
- Cần `pip install pillow`. Ảnh ghi thẳng vào `Assets/Resources/...`.

## Hiện trạng
- Combat: lượt theo Tốc độ, ý định quái, gạt đòn, Tuyệt kỹ bấm nhịp, Âm khí, bị nhập, né/may mắn ẩn. Đội mặc định Vy, Tuấn, Khoa; skill Vy "Phá đòn", Tuấn "Đọc văn tự" (tạm vẫn là đòn mạnh x2), Khoa "Che chắn".
- Làng: map 960x640, WASD đi, E tương tác, 4 lượt/ngày, vòng lặp 30 ngày, chọn người đi mỗi sáng, nói chuyện với bạn để tìm manh mối, đi đêm ở Điện Thoải phủ, minimap (M).
- Chưa làm: hầu đồng, nội dung ký ức, chọn 3 trong 5 người ra trận, luật riêng từng con ma, kỷ vật, trang bị, save/load, luật đọc văn tự của Tuấn, hiệu ứng ảo giác.

## Kiểm tra sau khi sửa
- Code: biên dịch thử bằng DLL Unity (csproj tạm) hoặc mở Unity xem Console không có lỗi đỏ, rồi Play.
- Cân bằng: tách logic thuần (như `VillageState`) để chạy thử được ngoài Unity.
