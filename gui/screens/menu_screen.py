
import pygame

from gui.button import Button
from gui.screens.base_screen import BaseScreen


class MenuScreen(BaseScreen):
    BACKGROUND = (24, 27, 32)
    ACCENT = (238, 164, 55)

    def __init__(self, app):
        super().__init__(app)

        center_x = app.WIDTH // 2
        button_width = 280
        button_height = 58

        def select_agent(agent_id):
            self.app.selected_agent = agent_id
            
            if agent_id == 1:
                self.open_single_agent()
            elif agent_id == 2:
                self.open_competitive_agent()

        self.buttons = [
            Button(
                (center_x - button_width // 2, 280,
                 button_width, button_height),
                "1 Agent",
                lambda: select_agent(1),
            ),
            Button(
                (center_x - button_width // 2, 355,
                 button_width, button_height),
                "2 Agent",
                lambda: select_agent(2),
            ),
            Button(
                (center_x - button_width // 2, 430,
                 button_width, button_height),
                "Exit",
                self.app.quit,
            ),
        ]

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

    def draw(self, surface):
        surface.fill(self.BACKGROUND)

        title_font = pygame.font.SysFont("arial", 46, bold=True)
        subtitle_font = pygame.font.SysFont("arial", 20)

        title = title_font.render(
            "SOKOBAN", True, self.ACCENT
        )
   

        surface.blit(
            title,
            title.get_rect(
                center=(self.app.WIDTH // 2, 155)
            ),
        )
      

        for button in self.buttons:
            button.draw(surface)
            
    def open_single_agent(self):
        from gui.screens.setup_screen import SetupScreen
        self.app.change_screen(SetupScreen(self.app))
    def open_competitive_agent(self):
        from gui.screens.competitive_setup_screen import (
            CompetitiveSetupScreen
        )

        self.app.change_screen(
            CompetitiveSetupScreen(self.app)
        )