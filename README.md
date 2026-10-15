# 503043 - Midterm Project: Sokoban

## Cài đặt
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt


## Hướng Dẫn

 `Solve` tính lời giải; dùng `Space`, `Left`, `Right` để phát/tạm dừng và chuyển bước. 
### Run app
Mở terminal trong thư mục dự án và chạy: `python main.py`

## Cấu trúc dự án
- `main.py` — CLI và điểm vào ứng dụng.
- `core/` — mô hình Sokoban, UCS/A*, heuristic và thống kê.
- `gui/` — ứng dụng, màn hình menu/setup/game, renderer, controls và assets.
- `maps/` — bản đồ dùng chung.
- `source/task1_sokoban/` — controller và thống kê cho chế độ một agent.
- `source/task2_competitive/` — competitive state, engine và hai agent độc lập.
- `tests/` — kiểm thử solver.
- `docs/` — formulation, rubric và quy trình nhóm.
