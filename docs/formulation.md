# Requirement 1 — Mô hình hóa bài toán dưới dạng tìm kiếm trong không gian trạng thái

Tài liệu này là **phần thiết kế lý thuyết** của nhóm. Không phải code.

**Vai trò trong bài:**
- Đề yêu cầu (Requirement 1, 1.0 điểm): mô hình hóa Sokoban thành bài toán tìm kiếm trong không gian trạng thái và xác định chi tiết các thành phần liên quan. Đây là nội dung chấm ở rubric mục "Formulation" (2.0 điểm).
- Nội dung này đưa thẳng vào **slide thuyết trình** và phần **trả lời hỏi đáp**.
- Sau này, `state.py` phải cài đặt đúng mô hình viết ở đây. Nếu code và tài liệu lệch nhau, sẽ bị trừ điểm khi hỏi đáp.
- Requirement 6 (bài 2 agent) cũng dựa trên mô hình này. Phần cuối tài liệu có chỗ để ghi thay đổi khi chuyển sang 2 agent.

**Ai viết:** C viết bản nháp, cả nhóm cùng đọc và thống nhất. Câu trả lời phải do nhóm tự suy nghĩ và viết, không nhờ AI viết hộ, vì nội dung này sẽ nằm trong bài nộp và slide.

---

## Các thành phần cần xác định

Với mỗi mục, nhóm viết câu trả lời ở ô "Nhóm trả lời" bên dưới.

### 1. Trạng thái (State)

Câu hỏi: cần những thông tin gì để mô tả đầy đủ một thời điểm của trò chơi?

Gợi ý suy nghĩ:
- Vị trí người đẩy có cần lưu không? Tôi nghĩ là có, vì nó cần biết vị trí hiện tại đang ở đâu, và sau đó từ vị trí đó sử dụng thuật toán tìm kiếm để tìm đường đi
- Vị trí các box có cần lưu không? Lưu dưới dạng gì (danh sách, tập hợp, tuple)? Các vị trí của box có cần lưu, và lưu dưới dạng tuple để theo thứ tự cố định. Và dù có box trên target hay không thì có thể suy ra được từ tập vị trí box và tập vị trí target, không cần lưu thêm. Một state chỉ cần: vị trí người đẩy, và tập vị trí các box
- Tường và target có đổi trong quá trình chơi không? Nếu không đổi, có nên lưu trong state không? Giải thích lý do chọn. Tường và target thì không thay đổi, và tôi nghĩ là không lưu trong state, vì đã lưu vị trí của các box rồi

**Nhóm trả lời:**

### 2. Trạng thái đầu (Initial state)

Câu hỏi: lấy từ file map như thế nào?

Gợi ý: ký hiệu `A` là vị trí người đẩy, `B` là box chưa đúng chỗ, `C` là box đã đúng chỗ, `D` là target.

**Nhóm trả lời:**
- Trạng thái A là vị trí của người đẩy
- Trạng thái B là vị trí của box chưa đúng chỗ
- Trạng thái C là box đã nằm trên target
- Trạng thái D là target
- Ta sẽ duyệt từng ô của map, ghi vị trí A cho người đẩy, gom B và C vào tập box, gom D và C vào tập target.
- Lưu ý: C vừa là box vừa là target. C nằm trong tập target vì ô đó là target, và đang có box trên đó

### 3. Kiểm tra đích (Goal test)

Câu hỏi: khi nào thì coi là thắng?

Gợi ý suy nghĩ:
- Đích là mọi box nằm trên target. Với `C` (box đã đúng chỗ), vị trí đó tính là target không?  
- Thứ tự các box có quan trọng không, hay chỉ cần tập vị trí khớp? 

**Nhóm trả lời:**
- Đích là mọi box đều nằm trên target, và khi box nằm trên target, tập target = ô D và ô C, với số box bằng số target, điều này tương đương với "tập box bằng tập target".
- Thứ tự không quan trọng, miễn là các box nằm trên được các điểm chấm là được

### 4. Hành động (Actions)

Câu hỏi: có những hành động nào? Điều kiện để một hành động hợp lệ là gì?

Gợi ý: hành động đặt tên theo đề bài (kiểm tra lại đề để dùng đúng tên). Một hành động hợp lệ khi:
- Ô đích không phải tường.
- Nếu ô đích có box, ô kế tiếp theo cùng hướng phải trống và không phải tường. Khi đó box cũng di chuyển.

**Nhóm trả lời:**
- Có những hành động như North, East, West, South
- Ô không phải tường và không có box, hoặc ô sau box không phải tường và không có box hợp lệ.
- Nếu ô đích có box: ô kế tiếp theo cùng hướng phải không phải tường và không có box. Khi đó box cũng dịch một ô

### 5. Mô hình chuyển trạng thái (Transition model)

Câu hỏi: từ một state và một action, state mới là gì? Viết dưới dạng công thức hoặc lời mô tả, không viết code.

**Nhóm trả lời:**
- Người đẩy di chuyển sang ô mới theo hướng action.
- Nếu ô mới có box thì box cũng dịch một ô theo hướng đó.
- State mới = vị trí mới người đẩy + tập box mới. State cũ không thay đổi.
- Nếu người đẩy đi vào ô trống thì tập box sẽ không đổi vì chưa có box nào bị đẩy
- Nếu action không hợp lệ thì không có state kế tiếp, ví dụ như action đụng tường

### 6. Chi phí đường đi (Path cost)

Câu hỏi: đề yêu cầu "tổng chi phí". Mỗi bước có chi phí bao nhiêu? Vì sao chọn như vậy?

Gợi ý: nếu mọi bước có chi phí 1 thì gọi là chi phí đồng nhất. Đây là lựa chọn đơn giản và dễ bảo vệ, trừ khi đề bài nói khác.

**Nhóm trả lời:**
- Mỗi bước đi có chi phí là 1, vì cứ mỗi 1 ô thì sẽ là 1 bước. Và việc làm như vậy thì sẽ dễ dàng tìm đường đi có số bước ít nhất để đẩy box về target, ngoài ra nó dùng để cho biết total cost khi hoàn thành đích là bao nhiêu bước

---

## Requirement 6 — Bài toán 2 agent (làm sau, khi Requirement 1 đã xong)

Sau khi mô hình 1 agent đã chốt, ghi ở đây những thay đổi khi chuyển sang 2 agent:
- Trạng thái thêm gì? (vị trí của cả 2 agent, lượt đi của ai?)
- Điều kiện thắng thay đổi thế nào? (ví dụ: đẩy được nhiều box hơn sau n bước)
- Ràng buộc: 2 agent đi cùng lúc mỗi bước, và không được đứng cùng một ô.

**Nhóm trả lời:**
- Trạng thái có thêm vị trí của agent thứ hai. 2 agent sẽ action cùng lúc với nhau, nên 1 action bây giờ là 2 agent sẽ thực hiện cùng lúc
- Cả 2 agent đều không đứng cùng 1 ô, vì sẽ bị đè
- Cho phép agent đẩy box đã được agent kia đặt đúng target, để trường hợp nếu cần tìm đường thì có thể di chuyển chúng được, sau khi làm vậy thì phải để lại box vào target ban đầu. Điều này ảnh hưởng đến goal test và điều kiện thắng.
- Điều kiện thắng: sau n bước, ai đưa được nhiều box vào target đúng hơn thì thắng
- Nếu mỗi agent chỉ được đụng box của mình, hai agent đi độc lập và không ảnh hưởng nhau. Khi được đẩy box của đối phương, mỗi quyết định của agent này có thể làm agent kia mất lợi thế, nên đây mới là bài cạnh tranh.
- Tránh bế tắc. Box đã nằm đúng target có thể chắn lối đi duy nhất. Nếu không được đẩy ra, agent kia có thể không bao giờ tới được box của mình.
- Hệ quả cho formulation: goal test và điều kiện thắng phải tính theo từng agent. Mỗi agent có tập target riêng, và số box đúng target của mỗi bên được tính sau n bước. Box có thể đổi bên trong quá trình chơi, nên không thể chỉ kiểm tra "tất cả box đã đúng chỗ