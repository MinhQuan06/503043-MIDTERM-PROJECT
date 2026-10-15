import pygame
from pathlib import Path
from state import load_map, get_valid_actions, step, walls, target
from search import solve

# TODO: pygame GUI (Requirement 5) - current focus.
# Design spec: see docs/gui-design.md
# QUYỀN SỞ HỮU: file này do A (Track A / GUI) phụ trách.
# B, C: không tự ý sửa/xóa. Cần đổi gì thì nhắn A hoặc mở Pull Request để A review trước khi merge.

class SokobanGame:
    def __init__(self, map_path):
        pygame.init() # KHởi tạo pygame
        self.clock = pygame.time.Clock() # Tạo clock để giới hạn FPS
        self.screen = pygame.display.set_mode((400, 500), pygame.RESIZABLE) # Tạo màn hình hiển thị pygame với size 400x500 và có thể thay đổi kích thước của sổ
        self.color = (195, 222, 221)
        self.font = pygame.font.SysFont(None, 28) # Tạo chữ trên UI
        self.target_color = (245, 116, 110)
        self.isRunning = True # Biến dùng để thoát vòng lặp khi người dùng tắt cửa số pygame
        self.block_size = 50

        self.ASSET_DIR = Path(__file__).parent.parent / "assets" # Đường dẫn tới asset

        # Hàm load hình ảnh
        def load_and_scale(file_path, pixel_size):
            img = pygame.image.load(file_path).convert_alpha()
            return pygame.transform.scale(img, (pixel_size, pixel_size))

        def load_character(file_path, max_size):
            img = pygame.image.load(file_path)
            img.set_colorkey((255, 255, 255))
            img = img.convert()
            w, h = img.get_size()
            scale = max_size / max(w, h)
            new_size = (int(w * scale), int(h * scale))
            return pygame.transform.scale(img, new_size)

        self.wall_img = load_and_scale(self.ASSET_DIR / "wall.png", self.block_size)
        self.box_img = load_and_scale(self.ASSET_DIR / "box.png", self.block_size)
        self.agent_img = load_character(self.ASSET_DIR / "roblox_character.jpg", self.block_size)
        self.box_on_target_img = load_and_scale(self.ASSET_DIR / "box_on_target.png", self.block_size)

        self.initial_state = load_map(Path(__file__).parent.parent/"example_map.txt") # Khởi tạo trạng thái ban đầu
        self.algorithm = "UCS"
        self.screen_mode = "menu" # Menu giao diện
        self.algo_options = ["UCS", "A*"]
        self.algo_index = 0
        self.title_font = pygame.font.SysFont(None, 60)

        """
        Đường đi chưa có thuật toán
        """
        self.path = solve(self.initial_state, self.algorithm)
        self.build_sequence()

        self.is_playing = False # Biến kiểm tra xem game, trạng thái đang chạy hay dừng
        self.last_step_time = 0 # Biến đo mốc thời gian lần cuối play-back hoặc play-next
        self.step_interval = 500 # Thời gian ms tối thiểu để play-back hoặc play-next

        self.right_flash_time = -9999   # mốc thời gian lần cuối bấm →, để âm lớn cho chắc chắn ban đầu không hiện icon
        self.left_flash_time = -9999
        self.flash_duration = 200

    def build_sequence(self):
        self.states_sequence = [self.initial_state]
        current = self.initial_state

        # Lặp qua các action hợp lệ đã từ thuật toán
        for action in self.path:
            current = step(current, action) # Cập nhật trạng thái hiện tại lên trạng thái của bước kế tiếp
            self.states_sequence.append(current) # Bỏ trạng thái đó vào danh sách

        self.current_step = 0

    # Giao diện menu game
    def draw_menu(self):
        title_text = self.title_font.render("Sokoban", True, (0, 0, 0))
        self.screen.blit(title_text, title_text.get_rect(center=(200, 100)))

        algo_text = self.font.render(self.algorithm, True, (0, 0, 0))
        algo_rect = algo_text.get_rect(center=(200, 220))
        self.screen.blit(algo_text, algo_rect)

        self.left_arrow_rect = pygame.Rect(130, 205, 30, 30)
        self.right_arrow_rect = pygame.Rect(240, 205, 30, 30)
        pygame.draw.polygon(self.screen, (0, 0, 0), [(160, 205), (160, 235), (130, 220)])
        pygame.draw.polygon(self.screen, (0, 0, 0), [(240, 205), (240, 235), (270, 220)])

        self.start_button_rect = pygame.Rect(150, 300, 100, 50)
        pygame.draw.rect(self.screen, (0, 0, 0), self.start_button_rect, 2)
        start_text = self.font.render("START", True, (0, 0, 0))
        self.screen.blit(start_text, start_text.get_rect(center=self.start_button_rect.center))

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.left_arrow_rect.collidepoint(event.pos):
                    self.algo_index = (self.algo_index - 1) % len(self.algo_options)
                    self.algorithm = self.algo_options[self.algo_index]
                elif self.right_arrow_rect.collidepoint(event.pos):
                    self.algo_index = (self.algo_index + 1) % len(self.algo_options)
                    self.algorithm = self.algo_options[self.algo_index]
                elif self.start_button_rect.collidepoint(event.pos):
                    self.path = solve(self.initial_state, self.algorithm)
                    self.build_sequence()
                    self.screen_mode = "playing"

    def draw_walls(self, walls_set : set):
        # Lặp qua tập walls để lấy các tọa độ
        for (row, column) in walls_set:
            # Chuyển sang tọa độ pixel x, y
            x = column * self.block_size
            y = row * self.block_size
            self.screen.blit(self.wall_img, (x, y))

    def draw_target(self, target_set):
        for (row, column) in target_set:
            # Chuyển sang tọa độ pixel x, y
            x = column * self.block_size + self.block_size // 2
            y = row * self.block_size + self.block_size // 2
            pygame.draw.circle(self.screen, self.target_color, [x, y], 10)

    def draw_boxes(self, boxes_set, target_set):
        for (row, column) in boxes_set:
            # Chuyển sang tọa độ pixel x, y
            x = column * self.block_size
            y = row * self.block_size

            if (row, column) in target_set:
                self.screen.blit(self.box_on_target_img, (x, y))
            else:
                self.screen.blit(self.box_img, (x, y))

    def draw_agent(self, agent_pos):
        row, column = agent_pos
        # Chuyển sang tọa độ pixel x, y
        x = column * self.block_size
        y = row * self.block_size
        img_rect = self.agent_img.get_rect(center=(x + self.block_size // 2, y + self.block_size // 2))
        self.screen.blit(self.agent_img, img_rect)

    def handle_events(self):
        for event in pygame.event.get():
            # Vòng lặp duyệt qua các sự kiện để kiểm tra có tắt cửa sổ không
            if event.type == pygame.QUIT:
                self.isRunning = False # Gán false khi tắt cửa sổ để kết thúc vòng lặp
            
            # Vòng lặp duyệt qua các sự kiện xem có sự kiện bấm phím không
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # Nếu bấm space thì dừng hoặc play
                    self.is_playing = not self.is_playing
                
                elif event.key == pygame.K_RIGHT: # Nếu bấm muỗi tên phải thì xem trạng thái kế tiếp từ trạng thái hiện tại
                    self.current_step = min(self.current_step + 1, len(self.path)) # Lấy giá trị nhỏ nhất giữa current_step và len(path) để không vượt quá path, tức là qua trạng thái tiếp theo khi bấm play-next
                    self.right_flash_time = self.now
    
                elif event.key == pygame.K_LEFT: # Nếu bấm muỗi tên trái thì lùi lại trạng thái trước đó từ trạng thái hiện tại
                    self.current_step = max(self.current_step - 1, 0) # Lấy giá trị lớn nhất giữa current_step và 0 để không vượt xuống âm, tức là qua trạng thái khởi tạo khi chọn play-back         
                    self.left_flash_time = self.now

    def run(self):
        # Vòng lặp liên tục để mở của số pygame
        while(self.isRunning):
            self.screen.fill(self.color) # Tô màu nền cho game
            self.now = pygame.time.get_ticks() # Biến thời gian chạy để biết ms đã trôi qua

            if self.screen_mode == "menu":
                self.draw_menu()
                self.handle_menu_events()
                pygame.display.update()
                self.clock.tick(60)
                continue
            
            # Kiểm tra xem game có đang chạy không, và xem bước tiếp theo agent đi có tối thiểu 500ms không thì mới cập nhật
            if self.is_playing and self.now - self.last_step_time >= self.step_interval:
                if self.current_step < len(self.path):
                    self.current_step += 1 # Cập nhật bước hiện tại
                    self.last_step_time = self.now # Lưu thời gian 
                else:
                    self.is_playing = False   # Tắt play không đi tiếp trạng thái nào nữa

            self.draw_walls(walls) # Vẽ tường
            self.draw_target(target) # Vẽ các chấm target
            self.draw_boxes(self.states_sequence[self.current_step].boxes, target) # Vẽ các box và box trên target
            self.draw_agent(self.states_sequence[self.current_step].agent) # Vẽ agent

            counter_text = self.font.render(f"Step: {self.current_step}/{len(self.path)}", True, (0, 0, 0))
            self.screen.blit(counter_text, (10, 460))
            algo_text = self.font.render(f"Algo: {self.algorithm}", True, (0, 0, 0))
            self.screen.blit(algo_text, (250, 460))
            icon_x = 150
            icon_y = 460

            if self.is_playing:
                pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(icon_x, icon_y, 6, 20))
                pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(icon_x+10, icon_y, 6, 20))
            else:
                pygame.draw.polygon(self.screen, (0,0,0), [(icon_x, icon_y), (icon_x, icon_y+20), (icon_x+18, icon_y+10)])

            if self.now - self.right_flash_time < self.flash_duration:
                # Vẽ icon tua tới
                pygame.draw.polygon(self.screen, (0,0,0), [(icon_x+30, icon_y), (icon_x+30, icon_y+20), (icon_x+44, icon_y+10)])
                pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(icon_x+46, icon_y, 4, 20))
                    
            if self.now - self.left_flash_time < self.flash_duration:
                # Vẽ icon tua lùi
                pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(icon_x-30, icon_y, 4, 20))
                pygame.draw.polygon(self.screen, (0,0,0), [(icon_x-12, icon_y), (icon_x-12, icon_y+20), (icon_x-26, icon_y+10)])
            
            self.handle_events()
            
            pygame.display.update() # Cập nhật màn hình pygame

            self.clock.tick(60) # Giới hạn FPS 60

        pygame.quit() # Tắt màn hình pygame

if __name__ == "__main__":
    game = SokobanGame(Path(__file__).parent.parent / "example_map.txt")
    game.run()