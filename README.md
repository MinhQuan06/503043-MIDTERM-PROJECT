# 503043 - Midterm Project: Sokoban

## Cài đặt
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt

## Chạy solver
    python main.py --algorithm astar
    python main.py --algorithm ucs

Thêm `--gui` để mở ứng dụng Pygame. Từ menu, chọn chế độ 1 agent hoặc 2 agent; màn hình thiết lập cho phép chọn map và thuật toán/số lượt.

    python main.py --gui

Ở chế độ 1 agent, `Solve` tính lời giải; dùng `Space`, `Left`, `Right` để phát/tạm dừng và chuyển bước. Chế độ 2 agent chạy hai controller đồng thời tới giới hạn lượt đã chọn.


## Cấu trúc dự án
- `main.py` — CLI và điểm vào ứng dụng.
- `core/` — mô hình Sokoban, UCS/A*, heuristic và thống kê.
- `gui/` — ứng dụng, màn hình menu/setup/game, renderer, controls và assets.
- `maps/` — bản đồ dùng chung.
- `source/task1_sokoban/` — controller và thống kê cho chế độ một agent.
- `source/task2_competitive/` — competitive state, engine và hai agent độc lập.
- `experiments/` — thí nghiệm thuật toán (đang chờ bổ sung).
- `tests/` — kiểm thử solver.
- `docs/` — formulation, rubric và quy trình nhóm.
