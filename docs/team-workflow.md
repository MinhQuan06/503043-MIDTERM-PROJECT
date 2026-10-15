# Quy trình làm việc nhóm — Midterm 503043 (Sokoban)

Deadline nộp: **17/10/2026**. Freeze code: **16/10/2026**.

Tài liệu này gộp toàn bộ: quy tắc, phân công, hợp đồng giữa các phần, hướng dẫn Git và lịch làm việc. Đọc theo thứ tự từ Bước 1 đến Bước 8. Làm xong bước nào thì qua bước đó.

---

## Bước 1 — Quy tắc bắt buộc (đọc trước khi làm bất cứ việc gì)

- **Cấm dùng AI viết code nộp.** Đề ghi: nếu trong source code có ký hiệu hoặc nội dung do AI tạo, phần đó bị **0 điểm**. Áp dụng cho **cả 3 người**.
  - Được: đọc tài liệu, học khái niệm, hỏi ý tưởng thuật toán.
  - Không được: nhờ AI viết, sửa, hay gợi ý đoạn code để chép vào bài. Kể cả một đoạn ngắn.
- **Không copy** code từ Internet hoặc của nhóm khác.
- **Không chia sẻ** bài với nhóm khác. Repo GitHub phải để **Private**.
- **Không push trực tiếp lên `main`.** Mọi thay đổi đi qua Pull Request (xem Bước 5).
- **Chỉ sửa file thuộc phần của mình** (xem Bước 3). Muốn sửa file người khác thì nhắn họ hoặc mở PR.

---

## Bước 3 — Phân công theo từng yêu cầu của đề

Ký hiệu: **A** = trưởng nhóm (GUI, formulation, state), **B** = thuật toán tìm kiếm và điều khiển agent, **C** = thực nghiệm, slide, demo. Thay chữ bằng tên thật sau khi họp. Danh sách chia theo **đúng số thứ tự Requirement trong đề** (không xen kẽ theo người), để ai cũng tra được rubric của mình đang ở đâu.

**Quy tắc chung cho mọi task bên dưới:** chỉ sửa file thuộc phần của mình. File người khác phụ trách thì chỉ được **đọc/import**, không sửa trực tiếp — xem comment "QUYỀN SỞ HỮU" ở đầu mỗi file code. Cần đổi file người khác thì nhắn trong nhóm hoặc mở Pull Request, chờ người đó review.

- A = Công Thắng
- B = Minh Quân
- C = Trung Kiên

---

### Req 1 — Formulation (1.0đ) — ✅ ĐÃ XONG (06/10)

| ID | Người | Việc | File | Lưu ý |
|---|---|---|---|---|
| T1 | A | State, initial state, goal test, action, transition model, path cost | `docs/formulation.md` | Đã chốt, B/C đọc file này trước khi code để hiểu đúng mô hình. |

### Req 2 — UCS và A* (1.0đ) — 🔲 B làm, bắt đầu ngay

| ID | Người | Việc | File | Lưu ý |
|---|---|---|---|---|
| T5 | B | Uniform Cost Search | `sokoban/search.py` (đã có stub) | Dùng `get_valid_actions(state)`, `step(state, action)`, `goal_check(state)` từ `state.py` — chỉ đọc, không sửa `state.py`. Không có lời giải thì trả `[]`, không trả `None`, không để crash. |
| T6 | B | A* + heuristic tự đề xuất | `sokoban/search.py`, `sokoban/heuristic.py` (đã có stub) | **Cấm** dùng Euclidean/Manhattan distance thuần (đề nói rõ). Nghĩ heuristic khác, ví dụ: số box chưa đúng target, hoặc khoảng cách đi thực tế có né tường (không phải đường chim bay). |

### Req 3 — Thực nghiệm so sánh (1.0đ) — 🔲 C làm, cần T5/T6 xong trước mới đo được

| ID | Người | Việc | File | Lưu ý |
|---|---|---|---|---|
| T2 | C | Bộ map test: nhỏ, vừa, khó (map khó hơn map mẫu để thấy rõ khác biệt UCS/A*) | `source/task1_sokoban/maps/` | Làm trước, không cần chờ T5/T6, chỉ cần `state.py` đọc được map là test thử. |
| T7 | C | Harness đo thời gian chạy, số node đã mở, bộ nhớ dùng — so UCS với A* trên từng map T2 | `source/task1_sokoban/experiments/` | Phải chạy được nhiều map liên tiếp, xuất ra bảng số liệu (CSV hoặc in ra console đều được), không cần làm UI đẹp cho phần này. |

### Req 4 — Chứng minh heuristic (1.0đ) — 🔲 B làm, sau khi xong T6

| ID | Người | Việc | File | Lưu ý |
|---|---|---|---|---|
| T8 | B | Chứng minh heuristic admissible (không vượt chi phí thật) và consistent (tam giác bất đẳng thức), kèm test code kiểm chứng | `docs/heuristic-proof.md`, `tests/` | Chứng minh viết bằng lời/công thức toán trong `.md`, **không phải code** — nhưng phần test kiểm chứng bằng code thì viết trong `tests/`, file này do B tạo, không đụng gì của A. |

### Req 5 — Pygame GUI (1.0đ) — 🟡 A, phần lớn đã xong, còn 3 việc nhỏ

| ID | Người | Việc | File | Trạng thái |
|---|---|---|---|---|
| T3 | A | `state.py`: biểu diễn state, đọc map, kiểm tra đích | `sokoban/state.py` | ✅ Xong, đã test kỹ bằng REPL. |
| T4 | A | Vẽ map bằng asset thật, Space tạm dừng/chạy, → / ← bước tới/lùi, bộ đếm action, icon play/pause kiểu Youtube, tổ chức OOP (`class SokobanGame`) | `sokoban/game.py` | ✅ Xong (13/10). |
| — | A | Thêm lựa chọn UCS hoặc A* trên UI (đề bắt buộc: "two options of algorithms") | `sokoban/game.py` | 🔲 Chưa làm — việc kế tiếp sau T11. |
| T9 | A | Thay `self.path = ['E', 'W']` (dữ liệu test tạm) bằng gọi `solve()` thật từ `search.py` | `sokoban/game.py` | 🔲 Chờ B xong T5/T6 mới làm được. |
| T15 | A | Chạy thử toàn bộ trên macOS 13.7.8 Intel, ghi lại kết quả (bản Python, bản pygame, lỗi nếu có) | `README.md` | 🔲 Chưa làm — cần mượn máy Mac trước D11 (16/10). |

### Req 6 — Reformulation bài toán 2 agent (1.0đ) — 🟡 A, **đang làm tiếp theo**

| ID | Người | Việc | File | Lưu ý |
|---|---|---|---|---|
| T11 | A | Hoàn thiện formulation 2 agent: state thêm gì, điều kiện thắng sau n bước, luật đẩy box của đối phương | `docs/formulation.md` (mục Requirement 6) | Đã có bản nháp, câu "để lại target ban đầu" từng bị flag là chưa rõ — đọc lại kỹ trước khi chốt, vì B sẽ dựa vào đây viết T10. |

### Req 7 — Thuật toán điều khiển 2 agent (1.0đ) — 🔲 B làm, sau khi xong Req 2/4

| ID | Người | Việc | File | Lưu ý |
|---|---|---|---|---|
| T10 | B | Thuật toán chọn action cho từng agent mỗi bước, giới hạn ≤1000ms/bước | `source/task2_competitive/agent_a/`, `source/task2_competitive/agent_b/` | Hai thư mục **không import lẫn nhau** (đề yêu cầu tách biệt để 2 nhóm có thể đấu nhau). Phải đọc xong T11 (formulation 2 agent của A) trước khi viết, vì luật thắng/thua nằm ở đó. |

### Req 8 — GUI competitive (1.0đ) — 🔲 A làm, sau khi B xong T10

| ID | Người | Việc | File | Lưu ý |
|---|---|---|---|---|
| T12 | A | GUI cho chế độ 2 agent, box của mỗi agent hiển thị màu khác nhau, agent tách file riêng | `source/task2_competitive/main.py` + GUI | Tái dùng cấu trúc `class SokobanGame` đã làm ở T4 nếu hợp lý, không viết lại từ đầu. |

### Presentation (2.0đ) — 🔲 C làm dần, dựa trên tiến độ các Req trên

| ID | Người | Việc | File | Lưu ý |
|---|---|---|---|---|
| T13 | C | Slide: tỉ lệ 4:3, ≤5 phút, nền sáng, đọc được khi in grayscale, **không dán code**, có bảng % hoàn thành mỗi Req | `presentation.pdf` | Bắt đầu khung slide sớm (không cần chờ mọi Req xong), điền nội dung dần khi từng Req hoàn tất. |
| T14 | C | Quay demo ≤3 phút, ghi URL vào `demo.txt` | `demo.txt` | Chỉ quay được sau khi T9 và T12 xong (cần GUI chạy với solve() thật). |

### Nền tảng / nộp bài (không tính điểm riêng nhưng bắt buộc)

| ID | Người | Việc | File | Trạng thái |
|---|---|---|---|---|
| T0 | Cả 3 | Tạo repo Private, mời thành viên, thống nhất hợp đồng | `docs/team-workflow.md`, `README.md` | ✅ Xong. |
| T16 | Cả 3 | Freeze, tạo zip, mỗi người kiểm tra và tự nộp | — | 🔲 Cuối cùng, D12 (17/10). |

**Lưu ý tải việc:** A đang gánh nặng nhất (T4 ✅, T9, T11 đang làm, T12, T15). Nếu sát deadline mà A chưa xong T15 (test Mac), ưu tiên nhờ C hỗ trợ tìm máy Mac thay vì bỏ qua — đây là yêu cầu bắt buộc của Req 5. B cũng nặng (T5, T6, T8, T10) — nếu B chậm, C có thể nhận T8 (chứng minh, không cần giỏi thuật toán, chỉ cần đọc hiểu và viết test) để B tập trung T5/T6/T10.

---

## Bước 4 — Hợp đồng giữa các phần

### 4.1. Map (đầu vào)

- File `.txt`. Mỗi dòng là một hàng của bản đồ. Các dòng cùng độ dài (thiếu thì thêm khoảng trắng).
- Ký hiệu theo đề:

| Ký hiệu | Ý nghĩa |
|---|---|
| `%` | tường |
| khoảng trắng | ô trống |
| `A` | vị trí người đẩy (agent) |
| `B` | box |
| `D` | target (đích của box) |
| `C` | box đã nằm đúng target |

- Số box bằng số target. Mỗi map có đúng một `A`.
- Ví dụ: `source/task1_sokoban/example_map.txt`.

### 4.2. State (owner: A, T3)

State là ảnh chụp đủ để biết trò chơi đang ở đâu. **Không sửa state tại chỗ**, luôn tạo state mới. Nhờ vậy UCS và A* có thể giữ nhiều state cùng lúc.

Gồm:
- Vị trí agent (hàng, cột).
- Tập vị trí box hiện tại.
- Tập vị trí tường (không đổi, dùng chung).
- Tập vị trí target (không đổi, dùng chung).

Phải làm được:
- Tạo state ban đầu từ file map.
- Liệt kê các action hợp lệ từ một state.
- Áp dụng một action và trả về state mới.
- Kiểm tra đích: đúng khi mọi box nằm trên target.
- So sánh hai state có giống nhau không (để search biết state đã thăm).

### 4.3. Action (owner: A, B dùng)

- Bốn hướng: lên, xuống, trái, phải.
- Mỗi action đi đúng một ô. Nếu ô đích có box thì đẩy box sang ô kế tiếp, ô đó phải trống (không tường, không box).
- Chi phí mỗi action = 1 (nếu nhóm chọn khác thì ghi vào `formulation.md`).
- Action không hợp lệ không được xuất hiện trong kết quả.

### 4.4. Hàm giải `solve` (owner: B, A dùng)

Đây là **điểm nối duy nhất** giữa GUI và phần tìm kiếm.

- **Tên:** `solve`
- **Đầu vào:**
  - `initial_state`: state ban đầu (mục 4.2).
  - `algorithm`: chuỗi, chỉ nhận `"UCS"` hoặc `"A*"`.
- **Đầu ra:** danh sách action (mục 4.3) theo thứ tự từ đầu đến đích. Không có lời giải thì trả về danh sách rỗng và báo rõ, không được im lặng.
- **Hiện trạng:** là **stub** (hàm giả). Trả về danh sách rỗng hoặc một đường cố định để GUI chạy thử được. Khi B xong UCS và A*, chỉ đổi thân hàm. GUI không đổi.

GUI **không** gọi trực tiếp `search.py` hay `heuristic.py`. Chỉ gọi `solve`.

**Đã tạo sẵn stub** tại `sokoban/search.py` (hàm `solve`, `ucs`, `a_star`) và `sokoban/heuristic.py` (hàm `heuristic`), mỗi hàm có comment `TODO` + docstring ghi rõ input/output. B chỉ cần mở 2 file này và điền thân hàm — không cần đụng `game.py` hay `state.py`, nên không lo conflict với A.

**Ghi chú cho B khi bắt đầu T5/T6:**
- Branch riêng: `feat/T5-ucs` rồi `feat/T6-astar` (xem Bước 5.4).
- Tự test bằng script nhỏ, không cần chạy `game.py`:
  ```
  from state import load_map
  from search import solve
  s = load_map("đường_dẫn_tới_example_map.txt")
  print(solve(s, "UCS"))
  ```
- `ucs`/`a_star` phải trả về `list` rỗng `[]` nếu không có lời giải — không được trả `None` hay để crash, vì GUI sẽ lặp qua kết quả này.
- Heuristic (T6) không được dùng Euclidean hay Manhattan distance thuần — đề cấm rõ. Nghĩ heuristic khác (vd: số box chưa đúng chỗ, tổng khoảng cách theo ô đi được thực tế...).
- Xong `ucs`/`a_star`, báo A để nối `solve()` thật vào GUI (T9) — A tự đổi 1 dòng trong `game.py`, B không cần sửa gì thêm bên đó.

### 4.5. GUI (owner: A)

- Nhận state ban đầu từ `main.py`.
- Gọi `solve` một lần khi người dùng chọn thuật toán. Lưu danh sách action trả về.
- Điều khiển bằng bàn phím:
  - Space: tạm dừng / tiếp tục.
  - → : bước tới một action.
  - ← : lùi một action.
- Hiển thị bộ đếm số action đã thực hiện.
- Cho phép chọn UCS hoặc A* trước khi chạy.

### 4.6. Chế độ 2 agent (B cho thuật toán, A cho GUI)

- Mỗi agent nằm trong thư mục riêng: `source/task2_competitive/agent_a/` và `agent_b/`. Hai thư mục không import lẫn nhau.
- Thuật toán điều khiển nhận state chung, trả về action cho từng agent trong ≤1000 ms.
- GUI gọi thuật toán điều khiển, không chứa logic agent bên trong.

### 4.7. Đường dẫn

- Dùng `pathlib` cho mọi đường dẫn. Không ghi cứng dấu `\` hay `C:\`. Cần thiết để chạy được trên macOS.
- Đường dẫn tới file map tính từ vị trí file code, không tính từ thư mục đang đứng khi chạy.

---

## Bước 5 — Quy trình Git hằng ngày

### 5.1. Chuẩn bị (mỗi người làm một lần)

1. Tạo tài khoản GitHub (mỗi người một tài khoản).
2. Cài Git. Windows tải tại git-scm.com. Mac chạy `git --version` trong Terminal, nếu chưa có máy sẽ đề nghị cài Command Line Tools.
3. Cấu hình tên và email (dùng đúng email đã đăng ký GitHub):

   ```
   git config --global user.name "Tên của bạn"
   git config --global user.email "email-github@example.com"
   ```

4. **Không để repo trong OneDrive.** OneDrive đồng bộ cả `.git/` và làm hỏng lịch sử. Tạo thư mục riêng, ví dụ:
   - Windows: `C:\Users\<tên>\projects\`
   - Mac: `~/projects/`

### 5.2. Tạo repo (chỉ trưởng nhóm làm, một lần)

1. Trên GitHub bấm **New repository**. Tên: `ai-midterm-sokoban`.
2. Chọn **Private**. Không chọn Public.
3. Không tick "Add README" (để trống, sẽ đẩy code lên sau).
4. Vào **Settings → Collaborators → Add people**, mời 2 bạn còn lại. Hai bạn vào email và bấm accept.
5. Đưa code lần đầu lên (trong thư mục project đã có `.gitignore`):

   ```
   git init -b main
   git add .
   git commit -m "Khởi tạo cấu trúc project"
   git remote add origin https://github.com/<username>/ai-midterm-sokoban.git
   git push -u origin main
   ```

   Trước khi commit, chạy `git status`. Không được thấy `.venv/`, `__pycache__/`, file zip hay video. Nếu có, thêm vào `.gitignore` trước.

### 5.3. Clone về máy (hai bạn còn lại)

```
git clone https://github.com/<username>/ai-midterm-sokoban.git
cd ai-midterm-sokoban
```

Tạo môi trường ảo và cài thư viện:
- Windows: `py -m venv .venv` rồi `.venv\Scripts\activate`
- Mac: `python3 -m venv .venv` rồi `source .venv/bin/activate`
- Cả hai: `pip install -r requirements.txt`

### 5.4. Làm một việc (mỗi lần làm T…)

Mỗi việc làm trong **một branch riêng**, đặt tên `feat/<ID>-<mô tả ngắn>`, ví dụ `feat/T5-ucs`.

```
git checkout main
git pull origin main
git checkout -b feat/T5-ucs
```

Commit nhỏ và thường xuyên, mỗi commit là một bước có ý nghĩa. Dùng `git add <file cụ thể>`, không dùng `git add .`:

```
git add source/task1_sokoban/sokoban/search.py
git commit -m "Thêm UCS dùng hàng đợi ưu tiên"
```

Trước khi đẩy lên, cập nhật từ `main` để giảm conflict:

```
git pull --rebase origin main
git push -u origin feat/T5-ucs
```

### 5.5. Mở Pull Request và review

1. Trên GitHub bấm **Compare & pull request** cho branch vừa đẩy.
2. Ghi rõ: đã làm gì, sửa file nào, đã test thế nào.
3. Chọn **Reviewers**: một người khác trong nhóm.
4. Người review đọc code, để nhận xét hoặc **Approve**.
5. Sau khi được approve, bấm **Merge pull request**, rồi bấm **Delete branch**.

Sau khi merge, trên máy mình:

```
git checkout main
git pull origin main
git branch -d feat/T5-ucs
```

**Quy tắc review:** người review chỉ nhận xét về logic, cách đặt tên, lỗi tiềm ẩn. Không tự viết hộ đoạn code. Nếu cần sửa, người làm tự sửa.

### 5.6. Khi bị conflict

Conflict xảy ra khi hai người sửa cùng một dòng của một file.

- **Phòng tránh:** chỉ sửa file thuộc phần của mình (Bước 3). Pull trước khi bắt đầu mỗi buổi làm việc.
- **Khi gặp:** chạy `git status` để xem file nào conflict. Nhắn người owner file đó và cùng ngồi sửa. Không tự đoán bừa.
- Sau khi sửa xong:

  ```
  git add <file đã sửa>
  git rebase --continue
  ```

- Nếu rối quá: `git rebase --abort` để quay về trạng thái trước. Không mất code.

### 5.7. Không bao giờ commit

- `.venv/`, `__pycache__/`, `*.pyc`
- File zip, video, file lớn
- Mật khẩu, token, thông tin cá nhân

### 5.8. Lệnh hay dùng

| Việc | Lệnh |
|---|---|
| Xem trạng thái | `git status` |
| Xem lịch sử | `git log --oneline` |
| Xem thay đổi chưa commit | `git diff` |
| Chuyển branch | `git checkout <tên>` |
| Hủy thay đổi một file (**mất thay đổi chưa commit**) | `git checkout -- <file>` |

Trước khi dùng lệnh hủy, hỏi nhóm. Thay đổi đã hủy không lấy lại được.

---

## Bước 6 — Lịch làm việc

| Ngày | Việc cần xong |
|---|---|
| D1 · 06/10 | T0 (repo, hợp đồng). **T1 đã xong.** Bắt đầu T2, T3, T5. Sáng 07/10: A sửa lại `state.py` theo formulation |
| D2–D3 · 07–08/10 | T3 xong. T4 bắt đầu với stub. T5 chạy được trên map nhỏ. T1, T2 xong |
| D4–D6 · 09–11/10 | T4 hoàn thiện. T6 (A* và heuristic). T7 bắt đầu |
| D7 · 12/10 | T9 nối `solve` thật. T6 xong. **Review chéo PR lần đầu** |
| D8 · 13/10 | T7 có bảng số liệu. T8 chứng minh và test |
| D9–D10 · 14–15/10 | T10 thuật toán 2 agent. T12 GUI competitive. T11 formulation 2 agent |
| D11 · 16/10 | **Freeze code.** T15 chạy thử trên Mac. T13 slide và T14 demo xong |
| D12 · 17/10 | Tạo zip. Mỗi người kiểm tra và nộp. Sửa lỗi trước 12:00 |

**Cập nhật thực tế (13/10):** T4 (GUI) hoàn thành hôm nay, trễ so với kế hoạch gốc (dự kiến D2-3, 07-08/10) — do thời gian học pygame từ đầu. A chuyển sang T11 (formulation 2 agent) ngay. Chỉ còn **4 ngày** tới freeze (16/10). Nếu B/C chưa báo tiến độ T5/T6/T2/T7, hỏi ngay hôm nay — không chờ tới D7 như lịch gốc nữa, vì đã là D8.

Nếu một người trễ hơn 1 ngày, báo nhóm ngay để cân lại kế hoạch. Đừng đợi đến ngày freeze mới báo.

---

## Bước 7 — Tiêu chí "xong" cho từng việc

- **T1:** formulation đủ 6 mục (trạng thái, trạng thái đầu, kiểm tra đích, hành động, chuyển trạng thái, chi phí). Đối chiếu rubric "Formulation". Đã đạt.
- **T3:** đọc được `example_map.txt`, kiểm tra đích đúng khi mọi box nằm trên target.
- **T4:** chạy `main.py` thấy đúng map, Space tạm dừng, → / ← bước đúng, bộ đếm tăng/giảm đúng, chọn được UCS hoặc A*.
- **T5:** UCS tìm được đường trên map nhỏ, danh sách action replay được.
- **T6:** A* chạy với heuristic tự đề xuất, không dùng Euclidean hoặc Manhattan thuần.
- **T7:** bảng gồm map, thuật toán, thời gian, số node mở, bộ nhớ, kèm nhận xét UCS so với A*.
- **T8:** tài liệu chứng minh admissible và consistent, có test chạy được.
- **T9:** GUI chạy với `solve` thật, bước tới/lùi khớp với đường đi.
- **T10:** mỗi bước ≤1000 ms. agent_a và agent_b nằm ở hai file riêng.
- **T12:** GUI competitive hiển thị được cả hai agent. Logic agent tách khỏi GUI.
- **T13:** đủ nội dung rubric Presentation (phương pháp, kết quả, demo, hỏi đáp). Không có code, nền sáng.
- **T15:** ghi lại lệnh đã chạy và kết quả trên Mac (phiên bản Python và pygame). Nếu lỗi, ghi rõ lỗi.

---

## Bước 8 — Nộp bài

Theo đề: folder tên `AI_midterm_<group ID>_<student ID>`, chứa `source/`, `presentation.pdf`, `demo.txt`. Nén zip.

1. Đảm bảo `main` là bản cuối (đã merge hết, đã freeze).
2. Trên máy mình: `git checkout main` rồi `git pull origin main`.
3. Copy folder project ra chỗ khác. **Xóa** `.venv/`, `.git/`, `__pycache__/`.
4. Đổi tên folder theo đề.
5. Nén zip. Mở lại zip kiểm tra có đủ `source/`, `presentation.pdf`, `demo.txt`.
6. **Mỗi người làm bước 1–5 và tự nộp zip.** Đề yêu cầu cả nhóm đều nộp, chỉ một người nộp là không đủ.
