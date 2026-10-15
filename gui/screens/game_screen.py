
from pathlib import Path

import pygame

from gui.button import Button
from gui.renderer import SokobanRenderer
from gui.screens.base_screen import BaseScreen
from source.task1_sokoban.game_controller import GameController


class GameScreen(BaseScreen):
    BACKGROUND = (24, 27, 32)
    PANEL = (34, 39, 47)
    TEXT = (240, 238, 225)
    MUTED = (165, 176, 190)
    ACCENT = (238, 164, 55)

    STEP_INTERVAL = 0.4

    def __init__(self, app):
        super().__init__(app)

        self.renderer = SokobanRenderer(tile_size=48)

        self.controller = GameController(
            app.selected_map,
            app.selected_algorithm
        )

        self.playing = False
        self.elapsed = 0.0
        self.status = "Ready - press Solve"

        self.title_font = pygame.font.SysFont(
            "arial", 36, bold=True
        )
        self.font = pygame.font.SysFont(
            "arial", 21, bold=True
        )
        self.small_font = pygame.font.SysFont("arial", 17)

        y = app.HEIGHT - 85

        self.back_button = Button(
            (40, y, 150, 50),
            "Back",
            self._go_back
        )

        self.solve_button = Button(
            (220, y, 150, 50),
            "Solve",
            self._solve
        )

        self.play_button = Button(
            (400, y, 170, 50),
            "Play/Pause",
            self._toggle_play
        )

        self.reset_button = Button(
            (600, y, 150, 50),
            "Reset",
            self._reset
        )

        self.buttons = [
            self.back_button,
            self.solve_button,
            self.play_button,
            self.reset_button,
        ]

    def _go_back(self):
        from gui.screens.setup_screen import SetupScreen

        self.app.change_screen(SetupScreen(self.app))

    def _solve(self):
        self.playing = False
        self.elapsed = 0.0
        self.status = "Solving..."

        try:
            found = self.controller.solve()

            if found:
                self.status = "Solved - press Space to play"
            else:
                self.status = "No solution found"

        except (ValueError, OSError) as exc:
            self.status = f"Error: {exc}"

    def _toggle_play(self):
        if not self.controller.solved:
            return

        if (
            self.controller.current_step
            >= self.controller.total_actions
        ):
            self.controller.reset()

        self.playing = not self.playing
        self.elapsed = 0.0

        self.status = "Playing" if self.playing else "Paused"

    def _reset(self):
        self.playing = False
        self.elapsed = 0.0
        self.controller.reset()
        self.status = "Reset to initial state"

    def _next_step(self):
        self.playing = False
        self.elapsed = 0.0

        if self.controller.solved:
            self.controller.next_step()
            self.status = "Paused"

    def _previous_step(self):
        self.playing = False
        self.elapsed = 0.0

        if self.controller.solved:
            self.controller.previous_step()
            self.status = "Paused"

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self._toggle_play()

            elif event.key == pygame.K_RIGHT:
                self._next_step()

            elif event.key == pygame.K_LEFT:
                self._previous_step()

        for button in self.buttons:
            button.handle_event(event)

    def update(self, dt):
        if not self.playing:
            return

        self.elapsed += dt

        while self.elapsed >= self.STEP_INTERVAL:
            self.elapsed -= self.STEP_INTERVAL

            moved = self.controller.next_step()

            if not moved:
                self.playing = False
                self.status = "Playback finished"
                break

            if (
                self.controller.current_step
                >= self.controller.total_actions
            ):
                self.playing = False
                self.status = "Playback finished"
                break

    def _draw_text(self, surface, text, x, y, font=None,
                   color=None):
        font = font or self.font
        color = color or self.TEXT

        image = font.render(str(text), True, color)
        surface.blit(image, (x, y))

    def draw(self, surface):
        surface.fill(self.BACKGROUND)

        title = self.title_font.render(
            "SOKOBAN - 1 AGENT",
            True,
            self.ACCENT
        )

        surface.blit(
            title,
            title.get_rect(
                centerx=self.app.WIDTH // 2,
                top=25
            )
        )

        map_name = Path(self.app.selected_map).name

        self._draw_text(
            surface, f"Map: {map_name}", 40, 115
        )
        self._draw_text(
            surface,
            f"Algorithm: {self.app.selected_algorithm}",
            40, 155
        )

        if self.controller.solved:
            total = self.controller.total_actions
            current = self.controller.current_step
        else:
            total = "--"
            current = 0

        self._draw_text(
            surface, f"Actions: {total}", 40, 215
        )
        self._draw_text(
            surface, f"Step: {current} / {total}", 40, 255
        )

        if self.controller.metrics is not None:
            metrics = self.controller.metrics

            self._draw_text(
                surface,
                f"Time: {self.controller.execution_time:.4f} s",
                40, 325,
                self.small_font
            )

            self._draw_text(
                surface,
                f"Peak memory: {self.controller.peak_memory_mb:.2f} MB",
                40, 355,
                self.small_font
            )

            self._draw_text(
                surface,
                f"Expanded: {metrics.expanded:,}",
                40, 385,
                self.small_font
            )

        map_area = pygame.Rect(
            300,
            105,
            self.app.WIDTH - 340,
            self.app.HEIGHT - 235
        )

        pygame.draw.rect(
            surface,
            self.PANEL,
            map_area,
            border_radius=12
        )

        self.renderer.render_state(
            surface,
            self.controller.problem,
            self.controller.current_state,
            map_area.inflate(-25, -25)
        )

        self._draw_text(
            surface,
            f"Status: {self.status}",
            40,
            self.app.HEIGHT - 155,
            self.small_font,
            self.ACCENT
        )

        self._draw_text(
            surface,
            "Space: Play/Pause | Left: Previous | Right: Next",
            300,
            self.app.HEIGHT - 125,
            self.small_font,
            self.MUTED
        )

        for button in self.buttons:
            button.draw(surface)
