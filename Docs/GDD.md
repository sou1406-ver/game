# Ký Ức Bị Chôn — GDD v0.4

2026-10-02 · @Tien Giap

## Tổng quan

Năm người bạn cũ bị một thứ dưới lòng đất gọi về làng quê Bắc Bộ nơi người bạn thứ bảy đã chết. Ban ngày họ sống ở làng, ban đêm đánh ma quỷ dân gian bằng combat turn-based, và dần đào lại sự thật mà thực thể đó đã bóp méo.

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

Thực thể dưới làng là oán niệm của vô số người chết trên một chiến trường cũ, hòa vào nhau thành một thứ không tên. Nó không tạo ra ký ức giả: nó lấy chuyện thật rồi đặt cạnh nỗi sợ và tội lỗi để con người tự hiểu sai. Nó sống bằng sợ hãi, oán hận, tội lỗi, và những câu chuyện con người tự kể cho mình về quá khứ.

**Thuở lập làng**

1. Vùng đất từng là chiến trường. Người chết thuộc nhiều phe, nhiều người không được chôn. Địa thế giữ âm khí nên hồn không đi được; qua nhiều thế hệ chúng chồng lên nhau thành một thứ méo mó: có ký ức nhưng không có quá khứ của riêng mình, biết sợ mà không biết sợ gì, chỉ biết đói. Dân gọi nó bằng nhiều tên, không tên nào đúng.
2. Một nhóm thầy trừ tà tìm đến. Diệt từng hồn thì chúng nhập lại; dùng pháp lực cưỡng ép thì oán khí phản ngược. Họ chọn phong ấn: không giết nó, chỉ cho nó ngủ, tách các hồn ra và ngăn chúng hợp nhất.
3. Nghi thức cần mạng người làm lễ. Từng người chết trong lễ: máu thành một phần trận pháp, hồn thành điểm neo giữ phong ấn.
4. Biết phong ấn không bền mãi, những người còn lại lập các gia tộc canh giữ và dựng làng trên chính vùng đất đó. Đình, miếu, điện vừa để thờ vừa là điểm giữ phong ấn, nối thành một trận pháp phủ cả vùng. Mỗi gia tộc mang một phần huyết mạch người làm lễ. Bí mật chỉ truyền cho trưởng tộc. Lời dặn: sống ở đây, giữ lễ, không để phong ấn bị phá.
5. Lâu dần chuyện thật mất. Làng chỉ còn nhớ tổ tiên từng "trấn một thứ dưới đất". Người canh giữ ngày càng ít hiểu thứ mình canh.

**Năm xưa**

1. Bảy đứa trẻ lớn lên cùng nhau: Minh, Vy, Tuấn, Khoa, Lan, Phong, Hải. Nhà nào cũng mang huyết mạch người phong ấn, nhưng chúng không biết. Chỉ Phong được gia đình kể một phần: nhà Phong trông điện Thoải phủ, Phong có căn, và chỉ biết một điều: không được để thứ dưới điện thoát ra.
2. Phong tò mò dẫn cả nhóm xuống khu cấm dưới điện. Lúc nghịch, Phong vô tình làm xê dịch một vật giữ trận pháp. Người lớn sửa lại nhưng không ai biết phong ấn đã không còn nguyên. Thực thể bắt đầu chạm được ra ngoài: thì thầm trong giấc mơ, hình ảnh không rõ nguồn gốc, những thôi thúc vô cớ. Nó tìm đến bọn trẻ, nhất là những đứa đang mang cảm xúc mạnh nhất.
3. Nhóm dần xa nhau. Hải thấy mình bị bỏ rơi, Phong ngày càng khác, mỗi người có bí mật riêng. Nhóm bỏ lại Phong. Sự chia rẽ không hoàn toàn ngẫu nhiên: thực thể liên tục đẩy họ xa nhau, giống IT.
4. Trong một lần xảy ra chuyện, cả nhóm bỏ Hải lại. Hải giận, đi theo một nhóm thanh niên lêu lổng. Đêm đó nhóm này phá điện Thoải phủ đang bỏ hoang, làm phong ấn vốn đã tổn thương yếu thêm.
5. Thực thể tìm thấy Hải, đứa trẻ đang giận, thấy bị bỏ rơi, đầy oán, và kéo Hải xuống. Hải chết. Thực thể chưa ra hẳn được và cần một hình hài, nên dùng Hải: từ đó mặt Hải là mặt của nó, và Hải thành một điểm neo mới của nó.
6. Phong cảm được, chạy tới điện, thấy thứ gì đó kéo Hải xuống bóng tối. Muốn cứu nhưng sợ, đứng đó rồi bỏ chạy. Phong không cứu được, cũng không nói với ai. Minh đi tìm Hải, từ xa thấy Phong ở gần điện, chạy về phía Hải, nhưng không thấy thứ đang kéo Hải. Minh bỏ chạy.
7. Mọi người chỉ biết Phong là người cuối cùng ở bên Hải, và Hải đã chết. Thành chuyện "Phong giết Hải". Phong không giải thích. Nhóm rời làng; Phong và Lan ở lại.

**Mười năm**

- Phong cố giữ phong ấn, nhưng phong ấn đã hỏng, và Hải đã thành điểm neo mới của thực thể.
- Năm người kia lớn lên với vết thương riêng (xem Nhân vật). Ai cũng có một phần của đêm Hải chết mà chưa từng đối diện.

**Hiện tại**

1. Phong ấn gần tới giới hạn. Thực thể mạnh hơn nhưng chưa tự phá được. Nó nhận ra 5 người là hậu duệ trực hệ cuối cùng: không giết được họ vì phong ấn dùng chính huyết mạch họ, nhưng huyết mạch đó cũng phá được phong ấn từ bên trong.
2. Nó gọi họ về bằng thứ họ không quên được: một giọng nói, một món đồ cũ, một giấc mơ, một lời nhắn, một ký ức về Hải. Ai cũng tin mình về vì lý do riêng, không ai biết người khác cũng đang về. Lan vốn vẫn sống ở làng. _[Lý do về của từng người: chưa chốt]_
3. Phong gặp năm người ở cổng làng, chỉ nói: "Chúng mày không nên về." Vy hỏi ngay về Hải, Minh không dám nhìn Phong, Khoa cho là chuyện mê tín, Tuấn né, Lan im lặng. Phong không nói hết sự thật: chưa chắc họ tin, và thứ đó cũng đang nghe.
4. Làng bắt đầu đổi: đường đổi hướng, nhà hoang hiện lại trong ký ức, người chết vào giấc mơ, chỗ quen thành lạ. Ký ức của họ bắt đầu bị bẻ cong (xem Mystery).
5. Thực thể nhốt cả làng trong một vòng lặp để tận hưởng nỗi sợ. _[Giữ từ v0.3, plot mới chưa nhắc]_
6. Thực thể bám vào các điện bỏ hoang, khoác hình tượng chư vị Tứ phủ. Đó là các "vị tha hóa" mà nhóm phải thanh tẩy. Để tìm câu trả lời, nhóm phải đi qua bốn phủ, những nơi gắn với phong ấn.
7. **Cái bẫy:** mỗi lần vượt qua một nơi bị nguyền, chạm vào một vật của quá khứ, nhớ lại một mảnh ký ức, phong ấn lại yếu đi. Càng điều tra để diệt nó, họ càng giúp nó thoát ra. Họ không được gọi về để tìm Hải, mà để phá phong ấn.
8. **Thứ nó tính sai:** nó hiểu sợ hãi, tội lỗi, biết biến ký ức thành lời buộc tội, nhưng không hiểu rằng con người có thể cùng nhau nhớ lại sự thật. Mỗi người giữ một mảnh của đêm Hải chết; không ai đủ một mình, ghép lại thì ký ức méo sụp đổ.

Chủ đề: quỷ không thắng bằng sức mạnh, mà bằng chính ký ức, tội lỗi và sự nghi ngờ của con người. Thứ nó không lấy được là sự thật mà nhiều người cùng nhớ lại.

## Nhân vật

Năm người chơi được, mỗi đêm ra trận 3. Hải và Phong không chơi được. Lỗi của mỗi người đều là thật; quỷ không nói dối, chỉ khuếch đại. Cả nhóm hiện 22–23 tuổi; Hải chết năm 12–13 tuổi.

| Nhân vật | Bề ngoài và nghề | Vết thương tâm lý | Combat | Phản ứng với quá khứ | Khúc mắc |
|---|---|---|---|---|---|
| Minh | Thợ xăm tự do. Điềm tĩnh, dễ tạo cảm giác đáng tin; mất ngủ, quầng thâm mắt | Tội lỗi vì đã bỏ chạy đêm Hải chết | Hầu đồng, đổi luật | **Chạy trốn**: ít nhắc quá khứ, ai nhắc Hải thì đổi chủ đề; dùng tiếng máy xăm át những tiếng thì thầm mà Minh không biết là của mình hay của cõi âm | Bề ngoài: bỏ làng vì sợ căn, sợ thành như Phong. Thật ra: đêm đó Minh thấy Phong chạy về phía Hải nhưng không thấy thứ kéo Hải, rồi bỏ chạy. Chỉ còn nhớ "Phong ở đó. Hải chết. Minh bỏ chạy" |
| Vy | Chị gái Hải, thợ sửa xe. Tóc ngắn nhuộm nâu đỏ/cam đồng, chân tóc đen mọc ra rõ; đeo chiếc chuông nhỏ, kỷ vật của Hải | Mất Hải, thấy mình đã không bảo vệ được em. Lần cãi nhau cuối, Vy nói với Hải: "Nếu mày thích đi thì đi luôn đi." | Kiểm soát, phá đòn | **Tức giận**: dùng giận dữ che đau buồn, thích kiểm soát, ghét bị thương hại, rất khó xin lỗi và nhận sai | Tin Phong biết Hải sẽ chết, đã ở đó và đã để Hải chết. Càng nhớ những lần cãi nhau với Hải, càng tin chính mình đã khiến Hải chết |
| Tuấn | Nhân viên văn phòng thất nghiệp. Áo gile, vẫn đeo thẻ nhân viên công ty cũ để giữ thể diện. Khéo léo, biết quan sát, giỏi nói chuyện để tránh xung đột | Xấu hổ. Biết Hải đang giận nhóm mà không nói với ai. Túng quẫn, giấu nợ và thói xấu cũ | Sát thương, đọc văn tự. Kháng Âm khí thấp nhất đội; các hiệu ứng gây ảo giác có xu hướng ưu tiên Tuấn | **Che giấu**: đùa cợt như thường, tỏ ra như đã quên Hải; dựng vỏ bọc thành đạt, dễ sụp khi bị bóc trần | Sống 10 năm với câu hỏi "nếu mình nói sớm hơn". Vay tiền Khoa không trả |
| Khoa | Thợ cơ khí xưởng máy. Cơ bắp, kính cận, cài bút sau tai. Lý trí, thực tế, thẳng thắn, thích bằng chứng | Không chấp nhận được thứ mình không giải thích được. Bị bạn lừa tiền, chán ghét sự nhập nhằng dối trá | Đỡ đòn. Kháng Âm khí cao nhờ luôn tập trung vào những gì kiểm chứng được, khiến ảo giác và thao túng tâm lý khó tác động | **Phủ nhận**: dùng lý trí để tránh cảm xúc, bám chặt vào công cụ, từ chối tin thứ vô hình | Năm xưa tin phải có người chịu trách nhiệm, góp phần khiến chuyện "Phong giết Hải" nghe hợp lý. Chưa tha cho Tuấn |
| Lan | Người duy nhất ở lại làng, làm ruộng, bán thuốc nam, chăm mẹ già. Trầm, ít nói, nhớ những chuyện người khác quên. Dáng vẻ mỏi mòn, cam chịu | Cảm giác bị bỏ lại; oán nhưng không nói ra | Hồi phục, giảm Âm khí | **Chịu đựng**: gánh ký ức, ở lại, im lặng nhìn | Oán những người đã rời làng. Một phần vẫn oán Phong, nhưng chưa bao giờ hỏi Phong |
| Phong | Người trông điện Thoải phủ, hậu duệ trực tiếp của một người làm lễ phong ấn, có căn từ nhỏ, người duy nhất trong nhóm được kể một phần sự thật. Bị làng xa lánh | Biết mình đã có thể làm gì đó cho Hải mà không làm. Tin mình đã góp phần làm phong ấn yếu | Không chơi được; bị nghi là phản diện | **Im lặng**: trả lời nửa chừng, giấu điều mình biết, việc gì cũng nhận "Là lỗi của tao" | 10 năm trước từng thử nói, nghĩ không ai tin, rồi im luôn. Càng lâu càng không biết bắt đầu từ đâu |
| Hải | Em trai Vy, đứa năng động nhất nhóm. Nay là bộ mặt và điểm neo mới của thực thể | Thấy mình không còn ai cần | Không chơi được | **Bị quá khứ nuốt lấy** | Giận cả nhóm, chưa giải |

**Sáu cách đối diện quá khứ**

| Nhân vật | Cách đối diện | Quỷ đẩy họ giữ cách cũ |
|---|---|---|
| Phong | Im lặng | Tiếp tục im lặng |
| Minh | Chạy trốn | Tiếp tục chạy |
| Vy | Giận dữ | Tiếp tục giận |
| Tuấn | Che giấu | Tiếp tục giấu |
| Khoa | Phủ nhận | Tiếp tục phủ nhận |
| Lan | Chịu đựng | Tiếp tục chịu đựng |
| Hải | Bị quá khứ nuốt lấy | — |

Con quỷ không chỉ đánh nhau với họ: nó khuyến khích từng người giữ cách đối diện cũ. Truyện không chỉ là tìm ai giết Hải, mà là các nhân vật phải đối diện với cách chính mình đã xử lý đêm Hải chết. True End không phải nhân vật trở nên hoàn hảo, mà là cuối cùng họ nhìn thẳng được vào những gì đã xảy ra. Hải là người bị quá khứ nuốt mất; năm người còn lại vẫn còn cơ hội thoát khỏi nó. Vì vậy câu "Nó ăn những câu chuyện mà con người tự kể cho mình về quá khứ" là trung tâm của game.

Minh và Phong đều có căn: một người trốn khỏi nó, một người ở lại với nó.

### Phong

- **Tuổi thơ:** thường cảm thấy những thứ lạ ở điện: tiếng bước chân khi không có ai, bóng người cuối hành lang rồi biến mất, tiếng gọi tên mình ban đêm. Gia đình không kể hết, chỉ dạy: không vào nơi cấm, không chạm đồ của điện, không bao giờ trả lời khi nghe ai gọi tên mình từ bên dưới. Phong không hiểu vì sao, chỉ nghe lời.
- **Với nhóm:** không cầm đầu, không nói nhiều. Vì hay thấy thứ người khác không thấy, dần bị coi là kỳ quặc.
- **Ngày phong ấn tổn thương:** tưởng khu cấm dưới điện chỉ là hầm cũ. Sau khi làm xê dịch vật giữ trận pháp, căn của Phong mạnh lên, thấy nhiều hơn, nghe tiếng gọi rõ hơn. Phong không biết chính mình đã làm phong ấn yếu đi.
- **Đêm Hải chết:** cảm được thứ dưới điện trước mọi người, chạy tới, thấy thứ gì đó kéo Hải xuống bóng tối. Muốn cứu nhưng sợ, đứng đó, rồi bỏ chạy. Điều đau nhất không phải Hải chết, mà là Phong biết mình đã có thể làm gì đó nhưng không làm.
- **Mười năm:** không rời làng, nhận nhiệm vụ gia đình trông điện. Làng nghĩ đó là hình phạt; Phong không giải thích. Phong ở lại vì tin mình đã góp phần làm phong ấn yếu: giữ lễ, sửa các điểm phong ấn, theo dõi làng, âm thầm tìm hiểu thứ đã giết Hải, và nhận ra không thể giải quyết một mình.
- **Vì sao không nói:** 10 năm trước đã thử nói. Không ai tin, hoặc Phong nghĩ vậy. Sau ánh mắt của Minh, Vy và những người khác, Phong chọn im lặng.
- **Arc:** giữ bí mật không phải lúc nào cũng là bảo vệ người khác; có sự thật dù đau vẫn phải nói. Điều Phong phải đối diện không chỉ là cái chết của Hải, mà là 10 năm tự trừng phạt mình.

### Hải

- **Tuổi thơ:** đứa năng động nhất nhóm, thích khám phá, thích nơi bị cấm, thích chuyện ma, hay trêu Phong vì Phong sợ những thứ Hải không thấy. Thường kéo cả nhóm đi chơi. Phong nói "Đừng vào đó", Hải hỏi "Tại sao?" rồi vẫn vào.
- **Gia đình:** em trai Vy. Hai chị em thân khi nhỏ, Vy hay phải trông Hải. Hải càng lớn càng muốn tự quyết, Vy thấy Hải khó bảo, Hải thấy Vy coi mình như trẻ con. Những mâu thuẫn đó không bao giờ được giải.
- **Với nhóm:** người kết nối cả nhóm. Kéo Phong về khi Phong bị xa lánh, làm dịu khi Minh và Vy cãi nhau, cười rồi kéo cả Tuấn và Khoa đi chơi khi hai đứa tranh luận. Nhưng chính người kết nối lại là người đầu tiên thấy mình bị bỏ lại.
- **Sự thay đổi:** Phong ở điện nhiều hơn, Minh quan tâm chuyện khác, Vy nghiêm khắc hơn, Tuấn và Khoa có bí mật riêng, Lan có cuộc sống riêng. Hải thấy không ai còn cần mình, không nói ra mà biến thành trò nghịch: càng bị nhắc càng làm, càng bị bỏ lại càng tỏ ra không quan tâm.
- **Đêm cuối:** bị nhóm bỏ lại, đi theo nhóm thanh niên để chứng minh mình không cần bạn cũ. Thực thể không chọn Hải ngẫu nhiên: nó cảm được oán hận, cảm giác bị bỏ rơi, giận dữ, cô độc của Hải và dùng chính chúng để kéo Hải xuống.
- **Sau cái chết:** Hải không trở thành con quỷ. Hải đã chết. Thứ mang mặt Hải là con quỷ dùng hình hài và ký ức của Hải. Vì nó hấp thụ Hải đầu tiên, một phần ký ức Hải hòa vào nó: nó có thể nói những câu chỉ Hải biết, nhớ chuyện Hải từng trải, dùng giọng Hải. Nhưng nó không hiểu Hải, chỉ hiểu những cảm xúc Hải từng có. Nhờ đó nó dùng Hải để thao túng năm người.

### Phong — Hải

Quan hệ quan trọng nhất của nhóm. Không phải "hai đứa thân nhất" đơn giản, mà là hai người đối lập: một đứa thích khám phá, một đứa luôn muốn ngăn lại. Hải kéo Phong về phía con người, khiến Phong biết cười, biết chơi, biết sống như một đứa trẻ. Phong kéo Hải tránh xa thứ bên dưới, và là người duy nhất thật sự hiểu Hải đang thay đổi, nhưng không biết cách giúp. Cuối cùng, người duy nhất biết Hải chết thế nào lại là người không cứu được Hải, và thứ mang mặt Hải liên tục nhắc Phong về thất bại đó.

### Minh

- **Tuổi thơ:** khá thân với Hải, hay kéo Hải về khi Hải quá nghịch. Hải lao vào nguy hiểm, Minh đứng sau quan sát, nên được coi là người tỉnh táo nhất, thường đứng giữa khi nhóm mâu thuẫn.
- **Đêm Hải chết:** người đầu tiên thấy có chuyện, đi tìm Hải. Gần điện, thấy Phong chạy về phía Hải nhưng không thấy thứ đang kéo Hải xuống. Sợ, bỏ chạy, chưa từng kể với ai. Trong ký ức Minh chỉ còn "Phong ở đó. Hải chết. Minh bỏ chạy": ba sự thật thiếu phần quan trọng nhất.
- **Mười năm:** rời làng, cố sống bình thường. Không ghét Phong nhưng không tha thứ được, luôn hỏi: "Nếu lúc đó tao không chạy thì sao?"
- **Hiện tại:** điềm tĩnh, hay phân tích, nhưng sự bình tĩnh là cách tự kiểm soát. Ghét xung đột, ghét phải chọn, nhất là chịu trách nhiệm cho người khác.
- **Quỷ khai thác:** cho Minh thấy nhiều phiên bản đêm đó: Phong giết Hải, Minh cứu được Hải, Hải chưa từng chết, đến khi Minh không biết bản nào thật.
- **Phải đối diện:** đã chạy, không vì xấu hay muốn Hải chết, mà vì sợ. Chấp nhận mình từng sợ mới giúp Minh nhớ đúng điều mình thấy.

### Vy

- **Tuổi thơ:** lớn hơn Hải, quen chăm em. Hay mắng Hải, nhưng Hải gặp chuyện thì Vy chạy đến đầu tiên. Cãi nhau nhiều, kiểu chỉ có giữa người rất thân.
- **Trước khi Hải chết:** Vy muốn Hải trưởng thành, Hải muốn Vy thôi coi mình là trẻ con. Lần cãi nhau Vy hối hận nhất: "Nếu mày thích đi thì đi luôn đi." Không lâu sau Hải chết.
- **Mười năm:** chưa bao giờ chấp nhận cái chết của Hải. Tin Phong có liên quan; Phong càng không giải thích, Vy càng chắc. Không muốn nghe Phong giải thích.
- **Quỷ khai thác:** đưa Vy về những lần cãi nhau, đổi từng câu của Hải: "Chị ghét em", "Chị muốn em biến mất", "Tại chị nên em mới chết". Câu nào cũng dựng từ chuyện thật, nhưng không câu nào đúng hoàn toàn.
- **Phải đối diện:** yêu một người không có nghĩa là cứu được họ khỏi mọi thứ; lời nói lúc giận không đổi được cái chết của Hải. Chấp nhận mình từng làm Hải tổn thương, không để tự trách mà để nhớ Hải như một con người thật.

### Tuấn

- **Tuổi thơ:** không nổi bật, đứng giữa, không quá thân Hải, không quá gần Phong. Quan sát tốt nên mọi người hay vô thức kể bí mật cho Tuấn.
- **Bí mật:** biết Hải thấy bị bỏ rơi, đang giận nhóm, từng nghe Hải nói: "Nếu chúng nó không cần tao thì tao cũng chẳng cần chúng nó." Không nói với ai, vì nghĩ đó là chuyện giữa Hải và nhóm. Sau khi Hải chết, Tuấn sống 10 năm với câu hỏi: nếu nói sớm hơn thì có khác không.
- **Mười năm:** rất giỏi giấu cảm xúc, nói chuyện và đùa như thường, có thể tỏ ra đã quên Hải, nhưng thật ra nhớ rất nhiều.
- **Quỷ khai thác:** cho Tuấn thấy các phiên bản khác của những bí mật cậu từng giữ: "Nếu mày nói ra, Hải sẽ không chết", "Chính mày đã giết Hải". Nó biến sự im lặng thành tội lỗi.
- **Phải đối diện:** nói ra điều mình biết, không vì chắc sẽ đổi được quá khứ, mà vì sự thật bị che giấu vẫn là một phần của sự thật.

### Khoa

- **Tuổi thơ:** ít tin chuyện ma nhất nhóm. Phong nói có thứ ở điện, Khoa giải thích khác: tiếng động là gió, bóng người là ánh sáng, tiếng gọi là ai chơi khăm. Khoa không sợ ma, ít nhất là luôn nói vậy.
- **Đêm Hải chết:** không tin chuyện ma quỷ, tin phải có người chịu trách nhiệm. Không có bằng chứng nên mọi thứ quy về Phong; Khoa góp phần làm chuyện "Phong giết Hải" nghe hợp lý.
- **Mười năm:** sống rất thực tế, tránh chuyện tâm linh, không tin bói toán, ma quỷ, không tin ký ức có thể bị đổi. Về làng, phản ứng đầu tiên: "Có người đang làm trò."
- **Quỷ khai thác:** không cho Khoa thấy ma mà cho thấy bằng chứng: một dấu chân, một vết máu, một vật bị dời, một đoạn ghi chép. Từng cái đều hợp lý, ghép lại thành một câu chuyện sai. Khoa càng tin bằng chứng riêng lẻ càng xa sự thật.
- **Phải đối diện:** thứ chưa giải thích được ngay không có nghĩa là không tồn tại; có những sự thật phải nhìn từ nhiều góc.

### Lan

- **Tuổi thơ:** không nổi bật, đứng ngoài quan sát, nhưng nhớ những chuyện người khác quên: ai nói gì, ai cãi nhau, ai bỏ đi, ai quay lại.
- **Sau khi Hải chết:** những người khác rời làng, Lan ở lại vì gia đình không cho đi. Càng ở càng gắn với làng: biết đường cũ, nhà hoang, nơi không nên đến, và những chuyện người lớn giấu trẻ con.
- **Mười năm:** biết Phong vẫn ở đó, điện vẫn còn, có chuyện lạ xảy ra, nhưng chưa bao giờ hỏi Phong. Một phần vẫn oán Phong, một phần oán những người đã đi.
- **Quỷ khai thác:** cho Lan thấy lại những ngày mọi người rời làng, những lần đứng nhìn họ đi, những lời hứa sẽ quay lại mà không ai quay lại. Nó khiến Lan tin: "Chúng nó chỉ quay về vì cần mày", để tách Lan khỏi nhóm lần nữa.
- **Phải đối diện:** thừa nhận mình đã oán rất lâu; ở lại không có nghĩa là bị bỏ rơi mãi mãi. Lan có quyền giận, nhưng không cần sống mãi trong cơn giận đó.

### Quan hệ với Phong

Mỗi người nhìn Phong một kiểu:

- Vy: Phong biết Hải sẽ chết, đã ở đó và đã để Hải chết.
- Minh: không ghét Phong, nhưng không tha thứ được.
- Tuấn: Phong biết bí mật của mình.
- Khoa: Phong nói chuyện ma quỷ vô lý; phải có người chịu trách nhiệm.
- Lan: chưa bao giờ hỏi Phong; một phần vẫn oán Phong.

**Chia phe sau khi Phong bị nghi** _[Lan và Khoa đổi theo background mới; cần chốt lại vì gắn kết ban đầu tính theo phe]_

| Nhân vật | Phe | Lý do |
|---|---|---|
| Lan | Lưỡng lự | Một phần vẫn oán Phong, nhưng chưa bao giờ hỏi Phong |
| Khoa | Không tin Phong | Không tin ma quỷ, tin phải có người chịu trách nhiệm; không có bằng chứng nên quy về Phong |
| Minh | Lưỡng lự | Không ghét Phong nhưng không tha thứ được. Cũng có căn, sợ mình sẽ thành như Phong; đó là lý do Minh bỏ làng |
| Tuấn | Không tin Phong | Hồi nhỏ lấy trộm tiền công đức ở đình, Phong biết nhưng không tố. Tuấn sợ Phong nhìn thấu bí mật của mình |
| Vy | Không tin Phong | Cần một người để trách cho cái chết của em |

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
| Sự kiện thật | Phong thấy Hải bị kéo đi, đứng đó rồi bỏ chạy, không cứu được, rồi im lặng |
| Ký ức của Phong | "Tôi đã đứng đó. Tôi đã không cứu nó." |
| Diễn giải bị khuếch đại | "Tôi đã chọn để Hải chết." |
| Kết luận của người khác | "Phong giết Hải" — sai, dù không câu nào vô căn cứ |

**Quy tắc**

- Mỗi người nhớ một mảnh thật, bị bẻ theo vết thương của mình: Minh nhớ Phong đã ở đó, Vy nhớ những lần cãi nhau với Hải, Tuấn nhớ bí mật của nhóm, Khoa nhớ dấu vết vật chất, Lan nhớ ngày cả nhóm bỏ lại Phong.
- Mỗi ký ức bị bóp méo có ít nhất 1 chi tiết mâu thuẫn với một kỷ vật hoặc ký ức khác: một vật kỷ niệm, một dấu chân, một vết thương, một lời nói, hoặc một thứ lẽ ra phải có mà không có. Để ý kỹ là phát hiện được.
- Kỷ vật là bằng chứng khó bị bóp méo.
- Game không báo lựa chọn nào là "sai". Nhân vật hành động theo điều họ tin; người chơi tự nhận ra mình bị dẫn dắt khi tìm thấy sự thật.
- Ví dụ: Vy nghe "Phong đã nhìn thấy Hải chết" và người chơi chọn: tin Phong giết Hải, đối chất với Phong, hoặc chưa kết luận để tìm thêm ký ức.

**Tiết lộ theo 3 tầng**

1. **Người chơi tin:** Phong có căn, bị bỏ lại, ở lại làng, Hải chết. Vậy Phong đã giết Hải.
2. **Người chơi bắt đầu nghi:** lời kể trong làng mâu thuẫn, kỷ vật cho thấy Hải giận nhóm trước khi chết, dấu vết ở hiện trường không giống phép của Phong.
3. **Sự thật:** thực thể chạm ra ngoài qua phong ấn đã hỏng, kéo Hải chết và dùng Hải làm hình hài. Phong không giết Hải, nhưng đã thấy mà không cứu, không nói. Việc nhóm chia rẽ nằm trong kế hoạch của thực thể. Năm người được gọi về để phá phong ấn.

**Tiết lộ theo phủ**

| Phủ | Tầng | Lộ ra |
|---|---|---|
| Thoải (Vertical Slice) | 1 → đầu 2 | Phong thấy Hải bị kéo đi, không giết Hải nhưng không cứu được, và im lặng suốt 10 năm; kỷ vật đầu tiên mâu thuẫn với lời kể trong làng |
| Nhạc | 2 | Ngày bỏ lại Phong và khúc mắc của từng người; việc chia rẽ không ngẫu nhiên, có thứ liên tục đẩy họ xa nhau |
| Địa | 2 | Dấu vết vật chất không khớp chuyện cũ; Hải đã giận nhóm trước khi chết; Minh nhớ lại điều mình thấy đêm đó |
| Thiên | 3 | Ghi chép về các gia tộc: chiến trường, những người chết trong lễ phong ấn, các gia tộc ở lại giữ phong ấn. Họ được gọi về để phá phong ấn |

## Ending

Ending do nghi lễ cuối quyết định, không do điểm số. Bad End là lịch sử lặp lại: nhóm lại không thể cùng nhau làm việc cuối như 10 năm trước, và quỷ thắng. Game không nói thẳng điều này; người chơi tự nhận ra.

**Nghi lễ cuối** cần đủ 5 người, vì mỗi người giữ một phần sự thật mà người khác không tự nhớ lại được: Vy giữ ký ức về Hải, Minh về đêm đó, Lan về ngày Phong bị bỏ lại, Tuấn về bí mật của nhóm, Khoa giữ bằng chứng vật chất. Lần này không cần máu. Mỗi người phải thừa nhận sự thật mình đã chôn:

| Người | Phải thừa nhận | Trạng thái quan hệ liên quan |
|---|---|---|
| Vy | Từng nói những lời làm Hải tổn thương | Vy → Phong |
| Minh | Đã chạy trốn | Minh → Phong |
| Tuấn | Bí mật luôn che giấu: biết Hải giận nhóm mà không nói | Tuấn → Khoa |
| Khoa | Có những điều không giải thích được bằng lý trí | Khoa → tâm linh |
| Lan | Vẫn oán những người đã bỏ mình lại | Lan → cả nhóm |
| Phong | "Tao đã nhìn thấy Hải chết. Tao đã chạy theo nó. Nhưng tao không cứu được nó. Và tao đã để chúng mày nghĩ tao là kẻ giết nó." | — |

Nếu trạng thái quan hệ của một người quá xấu (ví dụ Vy → Phong là Thù, hoặc Tuấn vẫn giấu nợ), người đó từ chối phần của mình.

**Diễn biến cuối game**

1. **Nghi lễ kích hoạt, phong ấn vỡ, thực thể thoát ra.** Nhưng như những người phong ấn năm xưa đã tính: vừa thoát ra là lúc nó yếu nhất. Hàng trăm năm bị giam khiến nó không đủ oán lực giữ hình dạng; nó cần thời gian hấp thụ sợ hãi, ký ức méo, oán hận, tội lỗi, và cần Hải. Lần đầu sau 10 năm, năm người nhìn Hải như một con người: một người bạn, một người em, một đứa trẻ từng giận, một người đã chết. Không phải gương mặt của thứ đứng trước mặt họ.
2. **Trận cuối.** Nó biến những ký ức tồi tệ nhất thành thật, cho mỗi người thấy phiên bản quá khứ họ sợ nhất, cố chia họ lần nữa. Lần này họ biết chuyện gì đang xảy ra. Mỗi người phải tự đối diện vết thương của mình: không chạy, không giận, không giấu, không phủ nhận, không chỉ chịu đựng. Cả nhóm cùng phá các điểm neo cuối. Mặt Hải xuất hiện lần cuối, nhưng đó không còn là Hải.

| Ending | Điều kiện | Kết quả |
|---|---|---|
| Bad End — Ký Ức Bị Chôn | Có người từ chối phần nghi lễ (nhóm không đủ gắn kết) | Nghi lễ thất bại, phong ấn vỡ hẳn. Quỷ hấp thụ đủ oán niệm để tồn tại bên ngoài. Làng biến mất trong sương âm khí, năm người không còn nhớ chính xác mình là ai, thứ mang mặt Hải rời làng |
| Normal End — Phong Ấn | Đủ 5 người hoàn thành nghi lễ | Quỷ bị đẩy về, phong ấn tái lập, chưa bị diệt. Nhóm sống sót, làng trở lại bình thường. Có những thứ không xóa khỏi ký ức được, chỉ học cách sống cùng |
| True End — Sự Thật Được Nhớ Lại | Đủ 5 phần, và dựng lại đúng đêm Hải chết từ bằng chứng | Thực thể mất thứ nó ăn, yếu đến mức diệt được; người chơi chọn tiêu diệt hay giải thoát |

True End là màn dựng lại sự kiện kiểu Return of the Obra Dinn, không phải trắc nghiệm. Người chơi tự trả lời 4 câu: ai kéo Hải đi, Phong ở đâu, vì sao Phong không cứu, Hải làm gì trước đó. Không câu nào giải được bằng một bằng chứng duy nhất; mỗi câu cần ít nhất 3 mảnh giao nhau (lời kể, kỷ vật, dấu vết hiện trường, luật của thực thể, lời Minh). Game chỉ xác nhận khi đúng cả 4 câu, để không đoán mò được.

Sự thật dựng lại được: Hải giận cả nhóm; nhóm bỏ Hải lại; những kẻ khác phá phong ấn; thực thể kéo Hải đi; Phong đã thấy; Minh đã thấy Phong; và không ai trong số họ thật sự hiểu chuyện gì xảy ra đêm đó.

Trận cuối không đủ để diệt thực thể. Thứ nó ăn không chỉ là oán hận mà là những câu chuyện con người tự kể về quá khứ; khi sự thật được nhớ lại, nó mất thứ đã nuôi nó 10 năm. Lúc đó người chơi chọn: tiêu diệt nó hoàn toàn, hoặc giải thoát những linh hồn đã kẹt hàng trăm năm, chấp nhận rằng nó không hẳn là một sinh vật riêng mà là oán niệm của vô số người chết. Game không xác nhận bên nào tốt hơn. Chọn bên nào Hải cũng không trở lại, nhưng lần đầu sau 10 năm, nhóm nhớ Hải như một người bạn chứ không như một bí ẩn. Đó là thứ con quỷ không lấy được.

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
2. Nghi lễ cuối: plot nói lễ để phong ấn lại, nhưng kích hoạt thì phong ấn vỡ và quỷ thoát ra. Có phải nhóm cố ý mở phong ấn lúc nó yếu nhất để đánh, rồi mới đẩy về (Normal) hoặc diệt/giải thoát (True)?
3. Lý do về làng của từng người (giọng nói, món đồ cũ, giấc mơ, lời nhắn, ký ức về Hải): ai nhận cái nào? v0.3 là về dự giỗ Hải.
4. Vòng lặp 30 ngày chưa có trong plot mới: giữ lý do "thực thể nhốt làng để tận hưởng nỗi sợ"?
5. "Điều tra làm phong ấn yếu đi" có thành cơ chế trong game (ví dụ một chỉ số phong ấn) hay chỉ là twist truyện?
6. Năm việc trong nghi lễ cũ (đứng bờ sông, gọi tên Hải, giữ chuông, đọc lời khấn, phần cuối) đã thay bằng lời thừa nhận. Có giữ thêm phần hành động không?
7. Phe ban đầu của Lan và Khoa đã đổi theo background mới (Lan: Lưỡng lự, Khoa: Không tin Phong). Gắn kết ban đầu tính theo phe nên cần chốt lại. Chi tiết cũ đã bỏ: Lan mang cơm cho Phong 10 năm, Phong cõng Lan về năm 8 tuổi, Phong hận cả nhóm.
8. Đêm Hải chết, background ghi Phong "đứng đó rồi bỏ chạy", nhưng lời thừa nhận của Phong ở nghi lễ cuối là "Tao đã chạy theo nó". Chốt một bản.
