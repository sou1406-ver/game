# Ký Ức Bị Chôn — GDD v0.3

2026-10-01 · @Tien Giap

## Tổng quan

Năm người bạn cũ về một làng quê Bắc Bộ dự giỗ người bạn đã mất. Ban ngày họ sống ở làng, ban đêm đánh ma quỷ dân gian bằng combat turn-based, và dần đào lại sự thật mà một thực thể tà ác đã bóp méo.

| Mục | Nội dung |
|---|---|
| Thể loại | Life-sim + turn-based RPG + mystery, roguelite nhẹ |
| Tham chiếu | Welcome to Elderfield (ngày/đêm), Darkest Dungeon (sanity, đội 3 người), IT (nhóm bạn trở về), Return of the Obra Dinn (suy luận) |
| Engine | Unity 6 |
| Đồ họa | Pixel |
| Team | Solo dev + AI đến khi có demo hoàn chỉnh; sau đó có thể thêm 1 bạn dev |
| Nền tảng | PC (chưa chốt) |

## Design Pillars

1. **Every Turn Matters** — quái báo trước ý định, mỗi lượt là một lựa chọn.
2. **Folklore Creates Mechanics** — mỗi con ma có một luật lấy từ truyện dân gian.
3. **Knowledge Is Progress** — biết luật ma, biết giá nào khắc ma nào, biết điều gì thật sự đã xảy ra. Crit là tỉ lệ %, nhưng bấm nhịp càng chuẩn thì tỉ lệ càng cao; gạt đòn đúng nhịp thì không mất máu.
4. **Everything Is Data** — ma, giá đồng, đồ cúng, cây trồng, kỷ vật đều là ScriptableObject.
5. **Ngày nuôi đêm** — việc ban ngày đổi ra sức mạnh ban đêm, hoặc đổi ra sự thật. Mỗi ngày phải chọn: tối nay mạnh hơn, hay hiểu nhau hơn.

## Cốt truyện

Một thực thể bị phong ấn dưới điện Thoải phủ không tạo ra oán hận; nó chỉ khiến con người tin rằng oán hận của mình là sự thật. Nó sống bằng tham sân si. Nó chia rẽ nhóm 7 người bạn, giết Hải, rồi 10 năm sau gọi 5 người còn lại về để họ tự hủy lần nữa.

**Năm xưa**

1. Làng ven sông ở đồng bằng Bắc Bộ dần bỏ lễ. Đình đổ, điện thờ hoang.
2. Nhóm 7 người bạn thân bỏ lại Phong. Việc này nằm trong kế hoạch của thực thể: đẩy nhóm bạn xa nhau, giống IT.
3. Hải còn nhỏ, giận dỗi cả nhóm, bỏ sang chơi với một nhóm lêu lổng.
4. Nhóm lêu lổng đi phá làng, phá phong ấn ở điện Thoải phủ nhà Phong và thả thực thể ra.
5. Thực thể kéo Hải chết rồi tha hóa Hải. Hải thành bộ mặt của nó.
6. Phong có căn nên thấy Hải bị kéo đi, chạy theo rồi dừng lại, không cứu được, cũng không nói với nhóm. Minh đi tìm Hải, từ xa thấy Hải bị một thứ vô hình kéo về phía điện và Phong chạy theo, rồi Minh bỏ chạy. Cả làng và cả nhóm nghi Phong giết Hải.
7. Vì ân hận, Phong bị Hải tha hóa một phần nhưng vẫn giữ được một phần tỉnh táo.

**Hiện tại**

- 10 năm sau, 5 người còn lại về làng dự giỗ Hải và bị kẹt lại.
- Thực thể nhốt cả làng trong một vòng lặp để tận hưởng nỗi sợ.
- Thực thể cũng bám vào các điện bỏ hoang, khoác hình tượng chư vị Tứ phủ. Đó là các "vị tha hóa" mà nhóm phải thanh tẩy.
- Thực thể khiến cả nhóm diễn giải ký ức theo hướng tệ nhất, vì nếu họ nhớ đúng chuyện năm xưa, họ sẽ biết cách làm nghi lễ tiêu diệt nó.

Chủ đề: quỷ không thắng bằng sức mạnh, mà bằng chính ký ức, tội lỗi và sự nghi ngờ của con người.

## Nhân vật

Năm người chơi được, mỗi đêm ra trận 3. Hải và Phong không chơi được. Lỗi của mỗi người đều là thật; quỷ không nói dối, chỉ khuếch đại.

| Nhân vật | Bề ngoài và nghề | Vết thương tâm lý | Combat | Phản ứng với quá khứ | Khúc mắc |
|---|---|---|---|---|---|
| Minh | Thợ xăm tự do. Khép kín, mất ngủ, quầng thâm mắt | Mặc cảm vì đã bỏ chạy đêm Hải mất | Hầu đồng, đổi luật | **Chạy trốn**: dùng tiếng máy xăm át những tiếng thì thầm mà Minh không biết là của mình hay của cõi âm | Bề ngoài: bỏ làng vì sợ căn, sợ thành như Phong. Thật ra: Minh thấy Phong cố cứu Hải nhưng đã bỏ chạy, và chỉ còn nhớ "Phong đã ở đó" |
| Vy | Em gái Hải, thợ sửa xe. Tóc ngắn nhuộm nâu đỏ/cam đồng, chân tóc đen mọc ra rõ; đeo chiếc chuông nhỏ, kỷ vật của Hải | Tự trách vì đã trù ẻo anh trai trước khi anh chết | Kiểm soát, phá đòn | **Tức giận**: dùng hung hăng làm giáp, tìm mục tiêu để đổ lỗi | Tin Phong đã giết anh mình |
| Tuấn | Nhân viên văn phòng thất nghiệp. Áo gile, vẫn đeo thẻ nhân viên công ty cũ để giữ thể diện | Tự ti vì túng quẫn, giấu nợ và thói xấu cũ | Sát thương, đọc văn tự. Kháng Âm khí thấp nhất đội; các hiệu ứng gây ảo giác có xu hướng ưu tiên Tuấn | **Che giấu**: dựng vỏ bọc thành đạt, dễ sụp khi bị bóc trần | Vay tiền Khoa không trả |
| Khoa | Thợ cơ khí xưởng máy. Cơ bắp, kính cận, cài bút sau tai. Thực tế, thẳng thắn, ít vòng vo, rất khó bị lay chuyển bởi những thứ không kiểm chứng được | Bị bạn lừa tiền, chán ghét sự nhập nhằng dối trá | Đỡ đòn. Kháng Âm khí cao nhờ luôn tập trung vào những gì kiểm chứng được, khiến ảo giác và thao túng tâm lý khó tác động | **Phủ nhận**: bám chặt vào công cụ, từ chối tin thứ vô hình | Chưa tha cho Tuấn |
| Lan | Người duy nhất ở lại làng, làm ruộng, bán thuốc nam, chăm mẹ già. Dáng vẻ mỏi mòn, cam chịu | Oán hận âm thầm vì cả nhóm bỏ mình lại giữa làng mục rữa | Hồi phục, giảm Âm khí | **Chịu đựng**: gánh ký ức, làm nhân chứng cho nỗi đau của Phong | Trách cả nhóm bỏ đi, bỏ mặc Phong |
| Phong | Con nhà thủ nhang giữ điện Thoải phủ và phong ấn bên trong, có căn từ nhỏ, bị làng xa lánh, ở lại giữ điện | Ân hận vì đã đứng nhìn mà không cứu được Hải | Không chơi được; bị nghi là phản diện | **Không thể buông bỏ**: chìm vào tội lỗi (xem dưới) | Hận cả nhóm vì bị bỏ rơi; ân hận vì không cứu Hải |
| Hải | Bộ mặt của thực thể | Giận dỗi bỏ nhóm, bị thực thể kéo chết rồi tha hóa | Không chơi được | — | Giận cả nhóm, chưa giải |

**5 cách đối diện một vết thương:** Minh chạy trốn, Vy tức giận, Tuấn che giấu, Khoa phủ nhận, Lan chịu đựng. Truyện không chỉ là tìm ai giết Hải, mà là 5 người phải đối diện với cách chính mình đã xử lý đêm Hải chết.

**Phong — kẻ không thể buông bỏ.** Phong là chiếc gương phản chiếu tội lỗi của cả 5:

- Không chạy đi đâu được, vì bị xích lại bởi chính căn đồng và ngôi điện hoang.
- Không giận dữ, không thanh minh, cũng không phủ nhận.
- Chỉ chìm vào đó: tự trừng phạt bằng cách sống như một cái bóng suốt 10 năm, nhai đi nhai lại cảm giác tội lỗi vì đã đứng nhìn mà không cứu được bạn.

Minh và Phong đều có căn: một người trốn khỏi nó, một người chìm vào nó. Con quỷ không cần bịa ra chuyện gì: nó chỉ cần giam 5 người quanh cái bóng của Phong, để 5 cách đối diện sai lầm đó tự cắn xé nhau cho đến khi cả nhóm tan rã lần thứ hai.

Lan là trục cảm xúc: người duy nhất tin và mang cơm cho Phong suốt 10 năm. Mỗi người nhìn Phong một kiểu:

- Vy: Phong là kẻ giết Hải.
- Minh: Phong đáng sợ, vì Minh từng thấy thứ gì đó.
- Tuấn: Phong biết bí mật của mình.
- Khoa: Phong nói chuyện ma quỷ vô lý.
- Lan: "Tao không biết chuyện đêm đó. Nhưng tao biết Phong không phải thứ chúng mày đang nghĩ."

**Chia phe sau khi Phong bị nghi**

| Nhân vật | Phe | Lý do |
|---|---|---|
| Lan | Tin Phong vô điều kiện | Năm 8 tuổi đi lạc trong rừng tre, Phong dùng căn tìm ra và cõng về. 10 năm qua vẫn mang cơm cho Phong khi cả làng tránh mặt |
| Khoa | Tin Phong | Không tin chuyện làm phép giết người |
| Minh | Lưỡng lự | Cũng có căn, sợ mình sẽ thành như Phong; đó là lý do Minh bỏ làng |
| Tuấn | Không tin Phong | Hồi nhỏ lấy trộm tiền công đức ở đình, Phong biết nhưng không tố. Tuấn sợ Phong nhìn thấu bí mật của mình |
| Vy | Không tin Phong | Cần một người để trách cho cái chết của anh |

**Trạng thái quan hệ** (dùng cho truyện và ending, không phải một thanh điểm)

| Quan hệ | Trạng thái có thể có |
|---|---|
| Vy → Phong | Tin / Nghi / Thù |
| Minh → Phong | Tin / Sợ / Nghi |
| Lan → cả nhóm | Tha thứ / Oán |
| Tuấn → Khoa | Đã thú nhận / Vẫn giấu |
| Khoa → tâm linh | Phủ nhận / Chấp nhận |

Trạng thái đổi qua các lựa chọn cụ thể trong sự kiện truyện, ví dụ Tuấn thú nhận khoản nợ, Vy chấp nhận ký ức về Hải có thể sai.

## Mystery

Quỷ không sửa ký ức. Nó khuếch đại nỗi sợ, tội lỗi và oán hận để con người diễn giải ký ức thật theo hướng tệ nhất. Mọi bí ẩn đi theo 3 tầng: sự kiện → ký ức → diễn giải.

**Ví dụ với Phong**

| Tầng | Nội dung |
|---|---|
| Sự kiện thật | Phong chạy theo Hải, dừng lại, không cứu được, rồi im lặng |
| Ký ức của Phong | "Tôi đã đứng đó. Tôi đã không cứu nó." |
| Diễn giải bị khuếch đại | "Tôi đã chọn để Hải chết." |
| Kết luận của người khác | "Phong giết Hải" — sai, dù không câu nào vô căn cứ |

**Quy tắc**

- Mỗi ký ức bị bóp méo có ít nhất 1 chi tiết mâu thuẫn với một kỷ vật hoặc ký ức khác. Để ý kỹ là phát hiện được.
- Kỷ vật là bằng chứng khó bị bóp méo.
- Game không báo lựa chọn nào là "sai". Nhân vật hành động theo điều họ tin; người chơi tự nhận ra mình bị dẫn dắt khi tìm thấy sự thật.
- Ví dụ: Vy nghe "Phong đã nhìn thấy Hải chết" và người chơi chọn: tin Phong giết Hải, đối chất với Phong, hoặc chưa kết luận để tìm thêm ký ức.

**Tiết lộ theo 3 tầng**

1. **Người chơi tin:** Phong có căn, bị bỏ lại, ở lại làng, Hải chết. Vậy Phong đã giết Hải.
2. **Người chơi bắt đầu nghi:** lời kể trong làng mâu thuẫn, kỷ vật cho thấy Hải giận nhóm trước khi chết, dấu vết ở hiện trường không giống phép của Phong.
3. **Sự thật:** thực thể thoát khỏi phong ấn đã kéo Hải chết và tha hóa Hải. Phong không giết Hải, nhưng đã thấy mà không cứu, không nói. Việc nhóm bỏ Phong nằm trong kế hoạch của thực thể.

**Tiết lộ theo phủ**

| Phủ | Tầng | Lộ ra |
|---|---|---|
| Thoải (Vertical Slice) | 1 → đầu 2 | Phong thấy Hải bị kéo đi mà không nói; kỷ vật đầu tiên mâu thuẫn với lời kể trong làng |
| Nhạc | 2 | Ngày bỏ lại Phong và khúc mắc của từng người |
| Địa | 2 | Dấu vết hiện trường không giống phép của Phong; Hải đã giận nhóm trước khi chết; điều Minh thấy đêm đó |
| Thiên | 3 | Thực thể, kế hoạch của nó, nghi lễ cuối |

## Ending

Ending do nghi lễ cuối quyết định, không do điểm số. Bad End là lịch sử lặp lại: nhóm lại không thể cùng nhau làm việc cuối như 10 năm trước, và quỷ thắng. Game không nói thẳng điều này; người chơi tự nhận ra.

**Nghi lễ cuối** cần đủ 5 người, vì mỗi người giữ một phần sự thật mà người khác không tự nhớ lại được: Vy giữ ký ức về Hải, Minh về đêm đó, Lan về ngày Phong bị bỏ lại, Tuấn về bí mật của nhóm, Khoa giữ bằng chứng vật chất. Mỗi người làm một phần:

- Đứng ở bờ sông
- Gọi tên Hải
- Giữ chuông
- Đọc lời khấn
- Hoàn thành phần cuối

Nếu trạng thái quan hệ của một người quá xấu (ví dụ Vy → Phong là Thù, hoặc Tuấn vẫn giấu nợ), người đó từ chối làm phần của mình.

| Ending | Điều kiện | Kết quả |
|---|---|---|
| Bad End — Chia rẽ | Có người từ chối phần nghi lễ | Nghi lễ thất bại, phong ấn vỡ hẳn, quỷ thoát |
| Normal End — Phong ấn | Đủ 5 người làm đủ 5 phần | Quỷ bị phong ấn lại, chưa bị diệt |
| True End — Ký Ức | Đủ 5 phần, và dựng lại đúng đêm Hải chết từ bằng chứng | Thực thể mất thứ nó ăn; người chơi chọn tiêu diệt hay giải thoát |

True End là màn dựng lại sự kiện kiểu Return of the Obra Dinn, không phải trắc nghiệm. Người chơi tự trả lời 4 câu: ai kéo Hải đi, Phong ở đâu, vì sao Phong không cứu, Hải làm gì trước đó. Không câu nào giải được bằng một bằng chứng duy nhất; mỗi câu cần ít nhất 3 mảnh giao nhau (lời kể, kỷ vật, dấu vết hiện trường, luật của thực thể, lời Minh). Game chỉ xác nhận khi đúng cả 4 câu, để không đoán mò được. Thực thể không bị giết bằng combat: nó sống nhờ oán hận, nên khi nhóm nhớ đúng rằng ai cũng có phần lỗi, nó mất thứ nó ăn. Lúc đó người chơi chọn tiêu diệt hay giải thoát; game không xác nhận bên nào tốt hơn.

## Core loop

Một ngày gồm ban ngày ở làng và một chuyến đi đêm ở điện. Ba mươi ngày là một vòng lặp.

_[Sơ đồ core loop: một ngày gồm ban ngày ở làng (4 lượt) và một chuyến đi đêm ở điện; 30 ngày là một vòng lặp]_

- **Đi đêm:** chọn 1 điện đã mở, đánh chuỗi 3 trận, không có map để đi.
- **Thua trong đêm:** tỉnh dậy ở nhà sáng hôm sau, mất một nửa đồ mang theo.
- **Lịch:** âm lịch, 1 vòng = 30 ngày. Đêm rằm có boss của điện.
- **Vòng lặp**: hết ngày 30 mà chưa thanh tẩy điện thì làng quay về ngày 1.

| Qua vòng lặp | Gồm |
|---|---|
| Giữ lại | Kỷ vật, ký ức, gắn kết, trạng thái quan hệ, giá đã mở, hiểu biết về luật ma |
| Mất | Đồ, đồ cúng, ruộng, tiền |

**Nguyên tắc vòng lặp:** reset thế giới, không reset tiến trình. Người chơi mạnh lên về hiểu biết, không chỉ về chỉ số. Ví dụ với Ma Da:

1. Vòng 1: nó kéo người xuống nước.
2. Vòng 2: nó luôn chọn người có Âm khí cao nhất.
3. Vòng 3: nhập giá Cô hút Âm khí về Minh thì nó đổi mục tiêu sang Minh.
4. Vòng 4: nó không săn người, nó đang tái hiện cái chết của Hải.

## Làng ban ngày

Mỗi ngày có 4 lượt hành động, mỗi hành động tốn 1 lượt. Mỗi ngày phải chọn: tối nay mạnh hơn, hay hiểu nhau hơn.

| Hành động | Kết quả | Dùng cho đêm |
|---|---|---|
| Làm ruộng | Trồng, tưới, thu hoạch | Nguyên liệu |
| Nấu ăn | Món ăn | Hồi máu, buff 1 đêm |
| Làm đồ cúng | Gạo muối, nhang, trầu cau, hoa huệ | Vật phẩm combat, lễ để nhập giá |
| Thăm người | Tăng thân thiết với NPC hoặc gắn kết giữa 2 bạn, nghe tin đồn | Mở bùa, thuốc; biết điểm yếu ma |
| Sửa đình | Khôi phục một nghi lễ | Mở điện mới để đi đêm |
| Tìm manh mối (đi cùng 1 bạn) | Mở 1 đoạn ký ức, +1 gắn kết với bạn đi cùng | Không có; đổi lại tiến truyện |

**Ruộng:** 1 thửa, 5 loại cây. Ruộng bị xóa khi vòng lặp quay lại, nên farming giữ ở mức nhẹ: ruộng để tạo lựa chọn trong ngày, không để tối ưu năng suất. Hệ thống nào không phục vụ combat, mystery hoặc không khí thì cắt.

| Cây | Lớn trong | Làm ra |
|---|---|---|
| Lúa nếp | 6 ngày | Gạo, xôi |
| Trầu | 4 ngày | Trầu cau (cùng cau) |
| Cau | 6 ngày | Trầu cau (cùng trầu) |
| Ngải cứu | 3 ngày | Thuốc giảm Âm khí |
| Hoa huệ | 4 ngày | Hoa cúng |

**NPC:** 4 người, mỗi người 5 mức thân thiết, mỗi mức mở 1 thứ.

| NPC | Mở ra |
|---|---|
| Thầy cúng | Bùa, công thức đồ cúng |
| Bà đồng | Giá đồng, nghi thức nhập giá |
| Ông lang | Thuốc hồi máu, giảm Âm khí |
| Cô hàng nước | Tin đồn: luật và điểm yếu của từng con ma |

**Bàn thờ ở nhà:** trước khi đi đêm, dâng 1 bộ lễ để chọn giá được ngự đêm đó.

**Đình làng:** hub. Mỗi lễ khôi phục mở 1 điện mới để đi đêm.

## Combat

Turn-based thuần: không map, không ô, không hàng trước/sau. Mỗi đêm 3 trong 5 người ra trận, đấu tối đa 4 quái. Lượt theo Tốc độ: mỗi vòng ai nhanh đi trước, đến lượt ai người đó hành động 1 lần. Chiều sâu đến từ ý định của quái, thứ tự lượt và luật riêng của từng con ma.

**Thứ tự một vòng**

1. Quái lộ ý định: ai bị đánh và đánh bằng gì.
2. Xếp lượt theo Tốc độ; bằng nhau thì người chơi đi trước.
3. Đến lượt nhân vật: chọn 1 hành động. Đến lượt quái: quái làm đúng ý định, người chơi có thể gạt đòn.
4. Hết lượt mọi người thì sang vòng mới.

**Hành động mỗi lượt**

| Hành động | Hiệu quả |
|---|---|
| Đánh thường | Crit theo %; hồi 2 MP, +20 Nộ |
| Skill | Tốn 4 MP |
| Tuyệt kỹ | Cần Nộ đầy; 3 đòn, mỗi đòn có thanh căng nhịp |
| Dùng vật phẩm | Tốn 1 vật phẩm |
| Đỡ | Đòn kế tiếp giảm 50%, hết hiệu lực khi đến lượt mình lần sau |
| Chờ | Bỏ lượt |

**Mục tiêu:** skill đánh 1 quái, cả phe quái, hoặc hủy một ý định đã báo. Đọc ý định để chọn đánh, đỡ hay hủy là quyết định chính mỗi lượt.

**Thanh căng nhịp:** chỉ có trong Tuyệt kỹ. Mỗi đòn, một vạch chạy ngang thanh trong 1 giây và một vùng sáng hiện ở vị trí ngẫu nhiên. Bấm khi vạch trong vùng: sát tâm cộng +40% crit, ở mép cộng +10%, ngoài vùng không cộng. Tổng crit tối đa 80%.

**Mana và Nộ:** mỗi người có MP 0–10 (bắt đầu 4) và Nộ 0–100. Đánh thường hồi 2 MP và +20 Nộ; bị đánh +10 Nộ; gạt đòn thành công +10 Nộ. Skill tốn 4 MP. Nộ đầy thì dùng được Tuyệt kỹ.

**Gạt đòn:** mỗi khi quái đánh, một thanh hiện ra với vùng đỏ hẹp gần cuối. Bấm đúng lúc vạch trong vùng thì đòn không gây sát thương; bấm sớm, trễ hoặc không bấm thì nhận đòn bình thường. Chỉ được bấm 1 lần mỗi đòn.

**Âm khí** (thay sanity), 0–100 mỗi nhân vật. Âm khí là mức một người đang mở cửa cho thực thể, chính là thứ nó ăn:

- Tăng khi bị ma đánh hoặc bị crit.
- Khúc mắc chưa giải thì nhân vật nhận gấp đôi Âm khí.
- Đầy 100 thì bị nhập: đến lượt mình ở vòng sau thì đánh 1 đồng đội, báo trước như ý định của quái.
- Giảm bằng nhang, thuốc ngải, nghỉ ở đình, hoặc ở nhà không ra trận.

**Gắnkết:** mỗi cặp bạn có thanh 0–5, tăng khi làm việc ban ngày cùng nhau. Từ 3 trở lên mở skill phối hợp của cặp đó. Gắn kết ban đầu: cùng phe 2, khác phe 0, với Minh 1.

**Thắng:** tùy luật từng con ma: giết, siêu độ hoặc thanh tẩy.

**Thua:** cả đội gục thì tỉnh dậy ở nhà, mất một nửa đồ mang theo.

## Chỉ số, trang bị và kỷ vật

Chỉ số đến từ 3 nguồn: chỉ số gốc, trang bị và kỷ vật. Mọi số là tạm, cân bằng ở Sprint 0.

| Chỉ số | Tác dụng | Trần |
|---|---|---|
| HP | Máu | — |
| Công | Sát thương đòn thường | — |
| Thủ | Trừ thẳng vào sát thương nhận | — |
| Crit | Tỉ lệ % gây x1.5 sát thương. Trong Tuyệt kỹ, thanh căng nhịp cộng thêm tới +40%; tổng tối đa 80% | 20 |
| Tốc độ | Ai cao đi trước trong vòng | 20 |
| Né (ẩn) | Tỉ lệ % tránh hẳn một đòn đơn mục tiêu; tổng tối đa 40% | 20 |
| May mắn (ẩn) | Mỗi điểm +0.5% crit và +0.5% né | 10 |
| Kháng Âm khí | Giảm Âm khí nhận vào | 50% |

Né và May mắn là chỉ số ẩn, người chơi không thấy số. Né không tác dụng với đòn đánh cả phe.

**Chỉ số gốc**

| Nhân vật | HP | Công | Thủ | Crit | Tốc | Né (ẩn) | May mắn (ẩn) | Kháng Âm khí |
|---|---|---|---|---|---|---|---|---|
| Minh | 24 | 5 | 2 | 5% | 10 | 5% | 2 | 10% |
| Vy | 22 | 4 | 2 | 10% | 12 | 10% | 3 | 5% |
| Lan | 26 | 3 | 3 | 5% | 8 | 5% | 4 | 10% |
| Tuấn | 26 | 7 | 2 | 15% | 9 | 5% | 2 | 0% |
| Khoa | 32 | 4 | 5 | 5% | 6 | 0% | 1 | 25% |

Khoa có Kháng Âm khí cao nhờ luôn tập trung vào những gì kiểm chứng được, nên ảo giác và thao túng tâm lý khó tác động tới anh. Tuấn có Kháng Âm khí thấp nhất đội.

**Trang bị:** mỗi người 2 ô, gồm 1 vật dụng đời thường (rựa, đèn pin, gậy tre) và 1 bùa từ thầy cúng.

**Kỷ vật** (thay cho Relic)

- Đồ hồi nhỏ của từng người, rơi sau trận ở điện hoặc nhận qua sự kiện truyện.
- Chỉ có tác dụng khi đúng chủ cầm. Giữ lại qua vòng lặp.
- Nhặt được thì tăng 1 chỉ số vĩnh viễn và mở 1 đoạn ký ức.
- Là bằng chứng khó bị quỷ bóp méo, dùng để đối chiếu ký ức sai.

| Kỷ vật | Chủ | Chỉ số | Mở ký ức |
|---|---|---|---|
| Chuông nhỏ của bà nội | Minh | +10% Kháng Âm khí | Lần đầu Minh thấy ma |
| Con diều Hải làm | Vy | +5% Né | Buổi chiều cuối cùng với Hải |
| Quyển lưu bút của nhóm | Lan | +4 HP | Ngày cả nhóm chia tay |
| Viên bi ve thắng của Khoa | Tuấn | +5% Crit | Lần đầu Tuấn nợ Khoa |
| La bàn tự chế | Khoa | +1 Thủ | Khoa thôi tin chuyện tâm linh |
| Ảnh chụp 7 người | Cả nhóm | +2 HP mỗi người | Ngày bỏ lại Phong |

## Hầu đồng

Trong nhóm chơi được, chỉ Minh có căn đồng, đối xứng với Phong. Nhập giá thì Minh chơi theo luật riêng của giá đó trong 3 lượt, không chỉ đổi bộ skill.

- **Thanh căn đồng 0–10:** +2 mỗi vòng, +1 khi đánh trúng điểm yếu của ma.
- **Đầy 10:** nhập giá 3 lượt, sau đó thanh về 0.
- **Điều kiện:** chỉ ngự được giá đã dâng lễ ở bàn thờ trước khi đi. Mỗi đêm mang 1 bộ lễ, nên phải chọn trước 1 giá.
- **Mở giá mới:** thanh tẩy vị tha hóa ở điện. Thực thể bị đuổi khỏi điện, giá đó mở cho người chơi.

**5 giá** (mỗi hàng 1 giá, vị cụ thể chọn sau khi tham vấn)

| Hàng | Luật khi nhập giá |
|---|---|
| Quan | Không gây sát thương, nhưng chuyển được ý định của ma sang mục tiêu khác |
| Chầu | Đồng đội càng nhiều Âm khí thì khiên càng dày |
| Ông Hoàng | Mỗi đòn mạnh hơn, nhưng Minh nhận Âm khí sau mỗi đòn |
| Cô | Hồi máu bằng cách hút Âm khí của đồng đội về Minh |
| Cậu | Minh được đi thêm 1 lượt ngay sau, nhưng ý định của ma bị ẩn |

## Tứ phủ và quái

Mỗi phủ là một điện bỏ hoang mà thực thể đang bám vào. Mỗi đêm chọn 1 điện đã mở và đánh chuỗi 3 trận. Đêm rằm, trận cuối là vị tha hóa của điện đó.

| Phủ | Màu | Hệ | Ma thường | Boss: vị tha hóa |
|---|---|---|---|---|
| Thoải phủ (sông nước) | Trắng | Kiểm soát, hủy ý định | Ma Da | Hàng Cô |
| Nhạc phủ (rừng núi) | Xanh | Độc, hồi máu | Hổ và ma trành | Hàng Chầu |
| Địa phủ (đất) | Vàng | Phòng thủ, chặn hồi sinh | Quỷ nhập tràng, ma lai | Hàng Cậu |
| Thiên phủ (trời) | Đỏ | Sát thương lớn | Mở cuối game | Hàng Quan và Ông Hoàng |

Phân bổ boss theo hàng là tạm, chốt sau khi tham vấn.

**Luật của từng con ma** — biết luật thì thắng gọn, không biết thì thua mòn:

| Ma | Luật | Cách thắng |
|---|---|---|
| Ma Da | Mỗi vòng đánh dấu người có Âm khí cao nhất làm thế mạng. Cuối vòng người đó không được đỡ thì bị kéo xuống nước, mất khỏi trận | Hạ máu về 0 rồi dâng 1 lễ để siêu độ. Không dâng thì nó hồi đầy máu sau 2 vòng |
| Hổ và ma trành | Trành đỡ thay mọi đòn đơn mục tiêu nhắm vào hổ. Mỗi trành còn sống +2 sát thương cho hổ | Dùng skill đánh cả phe để hạ hổ. Hổ chết thì trành tự tan |
| Quỷ nhập tràng | Quái đã gục đứng dậy lại nếu mèo đen còn trong trận | Giết mèo đen trước, hoặc rắc gạo muối lên xác (dùng 1 lượt) |
| Ma lai | Cái đầu bay đi đánh, không bị thương. Cái thân nằm trong trận, không đánh trả | Phủ thân (dùng 1 lượt). Đầu không về được, tan sau 3 vòng |
| Vị tha hóa | Pha 1: đánh bằng luật của giá đó, bản tha hóa | Pha 2: chịu đòn và dâng đúng lễ 3 lần để thanh tẩy, không giết |

## Nguyên tắc với tín ngưỡng

Đạo Mẫu là tín ngưỡng đang được thờ thật, nên giữ các ranh giới sau.

- Mẫu luôn là phe thiện, không bao giờ là kẻ thù.
- Chư vị bị tha hóa vì thực thể bám vào, không vì bản chất ác. Kết cục luôn là thanh tẩy và trở về, không bị giết.
- Boss dùng tên tự đặt kèm hàng, không dùng tên vị có đền thờ thật.
- Không có chi tiết gây cười, không biến tấu trang phục giá đồng thành gợi cảm.
- Tham vấn thủ nhang hoặc người làm chầu văn trước khi làm art, nhạc và lời thoại cho các giá.

## Scope Vertical Slice

Vertical Slice chỉ có Thoải phủ, gói trong 1 vòng lặp (30 ngày), kết thúc ở boss đêm rằm. Chưa làm ending. Số lượng đã cắt cho vừa solo dev + AI.

| Hạng mục | Số lượng |
|---|---|
| Phủ / điện | 1 (Thoải phủ) |
| Ma thường | 2 (Ma Da + 1 ma sông nước) |
| Boss | 1 (vị tha hóa hàng Cô) |
| Nhân vật chơi được | 5, ra trận 3 |
| Khúc mắc giải được | 2: Vy (chuyện của Hải), Minh (Phong và căn đồng); hai đường gặp nhau ở boss Thoải phủ |
| Ký ức bị bóp méo | 1, kèm cách phát hiện |
| Skill phối hợp | 1 cặp |
| Kỷ vật | 6 (5 riêng + 1 chung) |
| Trang bị | 4 vật dụng, 2 bùa |
| Giá đồng | 2 (Cô, Cậu) |
| NPC | 4 |
| Cây trồng | 5 |
| Đồ cúng | 4 |
| Save | Có |

**Không làm trong Vertical Slice:** ending, romance, câu cá, chăn nuôi, trang trí nhà, chế tạo vũ khí, thời tiết, lịch sinh hoạt NPC, map ngẫu nhiên, 3 phủ còn lại. Design đã đóng: không thêm hệ thống mới.

## Lộ trình

Combat phải vui trước, rồi mới làm làng. Mỗi sprint 2 tuần.

1. **Sprint 0 — Combat lõi:** 3 nhân vật đấu 2 quái (ô vuông làm hình tạm), lượt theo Tốc độ, ý định quái, Âm khí, mana, Nộ, Tuyệt kỹ với thanh căng nhịp, gạt đòn, né và may mắn ẩn. Câu hỏi chính: có vui không. Giả thuyết phụ: thanh căng nhịp làm mỗi đòn hồi hộp hơn, hay thành phiền.
2. **Sprint 1 — Luật ma:** Ma Da + 1 ma thường, hầu đồng với 1 giá, 1 đồ cúng, 1 điện.
3. **Sprint 2 — Làng tối giản:** 4 hành động/ngày, ruộng 5 cây, đồ cúng, bàn thờ, vòng ngày–đêm, vòng lặp 30 ngày.
4. **Sprint 3 — Vertical Slice:** 4 NPC, đình, kỷ vật, 1 ký ức bị bóp méo, boss tha hóa, save.

Code Day 1 (bản grid cũ): giữ UnitData, Commands và FSM của AI; bỏ GridMap và phần click ô.

## Câu hỏi mở

1. Giao diện màn dựng lại sự kiện ở True End: chốt khi làm full game, sau Vertical Slice.
