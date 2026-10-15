import pygame

from gui.button import Button
from gui.renderer import SokobanRenderer
from gui.screens.base_screen import BaseScreen

from source.task2_competitive.competitive_controller import (
    CompetitiveController
)


class CompetitiveGameScreen(BaseScreen):
    BACKGROUND = (24, 27, 32)
    PANEL = (34, 39, 47)
    BORDER = (78, 91, 108)
    TEXT = (240, 238, 225)
    MUTED = (165, 176, 190)
    ACCENT = (238, 164, 55)

    AGENT1_COLOR = (80, 200, 120)
    AGENT2_COLOR = (90, 155, 255)

    # Seconds between automatic turns
    STEP_INTERVAL = 0.8

    def __init__(self, app):
        super().__init__(app)

        self.controller = CompetitiveController(
            map_path=app.selected_map,
            max_turns=app.max_turns
        )

        self.renderer = SokobanRenderer(tile_size=48)

        self.playing = False
        self.elapsed = 0.0
        self.last_report = None
        self.message = "Ready to play"

        self.title_font = pygame.font.SysFont(
            "arial", 32, bold=True
        )
        self.font = pygame.font.SysFont(
            "arial", 21, bold=True
        )
        self.small_font = pygame.font.SysFont(
            "arial", 16
        )

        self._build_layout()

    def _build_layout(self):
        self.board_rect = pygame.Rect(
            35, 115,
            self.app.WIDTH - 350,
            self.app.HEIGHT - 225
        )

        self.info_rect = pygame.Rect(
            self.board_rect.right + 20,
            115,
            260,
            self.app.HEIGHT - 225
        )

        button_y = self.app.HEIGHT - 80

        self.back_button = Button(
            (35, button_y, 160, 50),
            "Back",
            self._go_back
        )

        self.reset_button = Button(
            (220, button_y, 160, 50),
            "Reset",
            self._reset
        )

        self.play_button = Button(
            (405, button_y, 180, 50),
            "Play / Pause",
            self._toggle_play
        )

        self.next_button = Button(
            (610, button_y, 160, 50),
            "Next Step",
            self._next_step
        )

        self.previous_button = Button(
            (795, button_y, 200, 50),
            "Previous Step",
            self._previous_step,
        )

        self.buttons = [
            self.back_button,
            self.reset_button,
            self.play_button,
            self.next_button,
            self.previous_button,
        ]

    def _go_back(self):
        from gui.screens.competitive_setup_screen import (
            CompetitiveSetupScreen
        )

        self.app.change_screen(
            CompetitiveSetupScreen(self.app)
        )

    def _reset(self):
        self.controller.reset()
        self.playing = False
        self.elapsed = 0.0
        self.last_report = None
        self.message = "Game reset"

    def _toggle_play(self):
        if self.controller.finished:
            return

        self.playing = not self.playing
        self.elapsed = 0.0

        self.message = (
            "Playing" if self.playing else "Paused"
        )

    def _next_step(self):
        if self.controller.finished:
            return

        self.playing = False
        self.elapsed = 0.0

        self._advance_turn()

    def _previous_step(self):
        self.playing = False
        self.elapsed = 0.0
        if self.controller.previous_step():
            turn = self.controller.state.turn
            self.last_report = self.controller.history[turn - 1] if turn else None
            self.message = "Paused" if turn else "Ready to play"

    def _advance_turn(self):
        if self.controller.finished:
            return

        self.last_report = self.controller.step()

        if self.last_report["finished"]:
            self.playing = False

            winner = self.last_report["winner"]

            if winner is None:
                self.message = "Draw!"
            else:
                self.message = f"Agent {winner} wins!"
        else:
            self.message = "Turn completed"

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self._toggle_play()

            elif event.key == pygame.K_RIGHT:
                self._next_step()

            elif event.key == pygame.K_LEFT:
                self._previous_step()

            elif event.key == pygame.K_r:
                self._reset()

    def update(self, dt):
        if not self.playing or self.controller.finished:
            return

        self.elapsed += dt

        if self.elapsed >= self.STEP_INTERVAL:
            self.elapsed = 0.0
            self._advance_turn()

    def _draw_panel(self, surface, rect):
        pygame.draw.rect(
            surface,
            self.PANEL,
            rect,
            border_radius=10
        )

        pygame.draw.rect(
            surface,
            self.BORDER,
            rect,
            width=2,
            border_radius=10
        )

    def _draw_text(
        self,
        surface,
        text,
        x,
        y,
        color=None,
        font=None
    ):
        font = font or self.small_font
        color = color or self.TEXT

        image = font.render(
            str(text),
            True,
            color
        )

        surface.blit(image, (x, y))

    def draw(self, surface):
        surface.fill(self.BACKGROUND)

        title = self.title_font.render(
            "SOKOBAN - COMPETITIVE",
            True,
            self.ACCENT
        )

        surface.blit(
            title,
            title.get_rect(
                center=(self.app.WIDTH // 2, 55)
            )
        )

        self._draw_panel(surface, self.board_rect)
        self._draw_panel(surface, self.info_rect)

        # Game board
        board_area = self.board_rect.inflate(-30, -30)

        self.renderer.render_competitive_state(
            surface,
            self.controller.state,
            board_area
        )

        # Match information
        x = self.info_rect.x + 20
        y = self.info_rect.y + 25

        state = self.controller.state

        self._draw_text(
            surface, "MATCH STATUS",
            x, y, font=self.font
        )

        y += 60

        self._draw_text(
            surface,
            f"Turn: {state.turn} / {self.controller.max_turns}",
            x, y
        )

        y += 55

        self._draw_text(
            surface,
            f"Agent 1 (A*): {state.score(1)}",
            x, y, self.AGENT1_COLOR
        )

        y += 40

        self._draw_text(
            surface,
            f"Agent 2 (GBFS): {state.score(2)}",
            x, y, self.AGENT2_COLOR
        )

        y += 60

        self._draw_text(
            surface,
            "Decision time:",
            x, y, font=self.font
        )

        y += 40

        if self.last_report:
            times = self.last_report["decision_times_ms"]

            self._draw_text(
                surface,
                f"Agent 1: {times[1]:.2f} ms",
                x, y, self.AGENT1_COLOR
            )

            y += 30

            self._draw_text(
                surface,
                f"Agent 2: {times[2]:.2f} ms",
                x, y, self.AGENT2_COLOR
            )

        y += 65

        message_color = self.ACCENT
        if self.controller.finished:
            winner = state.winner()
            if winner == 1:
                message_color = self.AGENT1_COLOR
            elif winner == 2:
                message_color = self.AGENT2_COLOR

        self._draw_text(
            surface,
            self.message,
            x, y,
            message_color
        )

        for button in self.buttons:
            button.draw(surface)
