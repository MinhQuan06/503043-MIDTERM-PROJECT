# 503043 - Midterm Project: Sokoban

## Cài đặt
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

## Chạy
    python main.py            # GUI một agent (UCS / A*)
    python main_versus.py     # GUI hai agent đối kháng

## Cấu trúc
- core/        logic bài toán, UCS, A*, heuristic
- versus/      luật chơi đối kháng hai agent
- agents/      mỗi agent một file riêng
- gui/         giao diện pygame
- experiments/ thí nghiệm so sánh và kiểm chứng heuristic
- maps/        các file map
- report/      báo cáo
