
from pathlib import Path

import pygame

from gui.screens.base_screen import BaseScreen
from gui.button import Button


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MAP_DIR = PROJECT_ROOT / "maps"


class SetupScreen(BaseScreen):
    TILE = 24

    BACKGROUND = (24, 27, 32)
    PANEL = (34, 39, 47)
    BORDER = (78, 91, 108)
    TEXT = (240, 238, 225)
    MUTED = (165, 176, 190)
    ACCENT = (238, 164, 55)

    MAPS = [
        ("Map 1", "example_map.txt"),
        ("Map 2", "versus_map.txt"),
    ]

    # Keep only algorithms implemented in core/search.py.
    ALGORITHMS = ["UCS", "A*"]


    def __init__(self, app):
        super().__init__(app)

        from gui.renderer import SokobanRenderer

        self.renderer = SokobanRenderer(tile_size=32)
        self.preview_lines = []
        self.map_error = ""

        self.selected_map_index = 0
        self.selected_algorithm_index = 0
        self.message = ""

        self.font = pygame.font.SysFont("arial", 20, bold=True)
        self.small_font = pygame.font.SysFont("arial", 15)
        self.title_font = pygame.font.SysFont("arial", 32, bold=True)

        self.map_buttons = []
        self.algorithm_buttons = []
        self.back_button = None
        self.start_button = None

        self._build_buttons()
        self._load_preview()

    def _build_buttons(self):
        margin = 35
        gap = 20
        self.left_x = margin
        self.left_width = 230
        self.right_width = 230
        self.center_x = self.left_x + self.left_width + gap
        self.center_width = (
            self.app.WIDTH - 2 * margin
            - self.left_width - self.right_width - 2 * gap
        )
        self.right_x = self.center_x + self.center_width + gap

        self.map_buttons = [
            Button(
                (self.left_x + 15, 185 + index * 70,
                 self.left_width - 30, 50),
                label,
                lambda index=index: self._select_map(index),
            )
            for index, (label, _) in enumerate(self.MAPS)
        ]
        self.algorithm_buttons = [
            Button(
                (self.right_x + 15, 185 + index * 70,
                 self.right_width - 30, 50),
                algorithm,
                lambda index=index: self._select_algorithm(index),
            )
            for index, algorithm in enumerate(self.ALGORITHMS)
        ]
        self.back_button = Button(
            (margin, self.app.HEIGHT - 80, 160, 50),
            "Back", self._go_back,
        )
        self.start_button = Button(
            (self.app.WIDTH - margin - 160, self.app.HEIGHT - 80, 160, 50),
            "Start", self._start,
        )


    def _select_map(self, index):
        self.selected_map_index = index
        self.message = ""
        self._load_preview()

    def _select_algorithm(self, index):
        self.selected_algorithm_index = index
        self.message = ""



    def _go_back(self):
        from gui.screens.menu_screen import MenuScreen
        self.app.change_screen(MenuScreen(self.app))


    def _start(self):
        from gui.screens.game_screen import GameScreen

        _, filename = self.MAPS[self.selected_map_index]
        algorithm = self.ALGORITHMS[self.selected_algorithm_index]

        map_path = MAP_DIR / filename

        if not map_path.is_file():
            self.message = f"Map not found: {filename}"
            return

        self.app.selected_map = str(map_path)
        self.app.selected_algorithm = algorithm
        self.app.selected_agent = 1

        self.app.change_screen(GameScreen(self.app))


    def handle_event(self, event):
        for button in (
            self.map_buttons
            + self.algorithm_buttons
            + [self.back_button, self.start_button]
        ):
            button.handle_event(event)

    def _draw_text(self, surface, text, pos, color=None, font=None):
        font = font or self.font
        color = color or self.TEXT
        image = font.render(text, True, color)
        surface.blit(image, pos)

    def _draw_panel(self, surface, rect, title):
        pygame.draw.rect(
            surface, self.PANEL, rect, border_radius=10
        )
        pygame.draw.rect(
            surface, self.BORDER, rect, width=2, border_radius=10
        )

        title_image = self.font.render(title, True, self.TEXT)
        title_rect = title_image.get_rect(
            midtop=(rect.centerx, rect.top + 18)
        )
        surface.blit(title_image, title_rect)



    def draw(self, surface):
        surface.fill(self.BACKGROUND)

        self._draw_text(
            surface,
            "SOKOBAN",
            (self.app.WIDTH // 2 - 105, 35),
            self.ACCENT,
            self.title_font,
        )

        top = 115
        panel_height = self.app.HEIGHT - 225

        left_rect = pygame.Rect(
            self.left_x, top, self.left_width, panel_height
        )
        center_rect = pygame.Rect(
            self.center_x, top, self.center_width, panel_height
        )
        right_rect = pygame.Rect(
            self.right_x, top, self.right_width, panel_height
        )

        self._draw_panel(surface, left_rect, "SELECT MAP")
        self._draw_panel(surface, center_rect, "MAP PREVIEW")
        self._draw_panel(surface, right_rect, "ALGORITHM")

        for index, button in enumerate(self.map_buttons):
            button.draw(surface)
            if index == self.selected_map_index:
                pygame.draw.rect(
                    surface,
                    self.ACCENT,
                    button.rect,
                    width=3,
                    border_radius=10,
                )

        for index, button in enumerate(self.algorithm_buttons):
            button.draw(surface)
            if index == self.selected_algorithm_index:
                pygame.draw.rect(
                    surface,
                    self.ACCENT,
                    button.rect,
                    width=3,
                    border_radius=10,
                )


        preview_area = pygame.Rect(
            center_rect.x + 12,
            center_rect.y + 65,
            center_rect.width - 24,
            center_rect.height - 125,
        )

        pygame.draw.rect(
            surface,
            (18, 21, 25),
            preview_area,
            border_radius=8,
        )

        if self.preview_lines:
            self.renderer.render_map(
            surface,
            self.preview_lines,
            preview_area,
        )
        else:
            self._draw_text(
                surface,
                getattr(self, "map_error", "Map unavailable"),
                (preview_area.x + 10, preview_area.y + 10),
                self.MUTED,
                self.small_font,
    )

        _, filename = self.MAPS[self.selected_map_index]
        algorithm = self.ALGORITHMS[self.selected_algorithm_index]

        self._draw_text(
            surface,
            filename,
            (center_rect.x + 20, center_rect.bottom - 45),
            self.MUTED,
            self.small_font,
        )
        self._draw_text(
            surface,
            f"Algorithm: {algorithm}",
            (center_rect.x + 20, center_rect.bottom - 25),
            self.TEXT,
            self.small_font,
        )

        self.back_button.draw(surface)
        self.start_button.draw(surface)

        if self.message:
            message = self.small_font.render(
                self.message, True, self.ACCENT
            )
            surface.blit(
                message,
                message.get_rect(
                    center=(
                        self.app.WIDTH // 2,
                        self.app.HEIGHT - 105,
                    )
                ),
            )

    def _load_preview(self):
        _, filename = self.MAPS[self.selected_map_index]
        path = MAP_DIR / filename

        try:
            self.preview_lines = self.renderer.read_map(path)
            self.map_error = ""
        except (OSError, UnicodeError) as exc:
            self.preview_lines = []
            self.map_error = f"Cannot load map: {exc}"
