
import pygame

from gui.screens.menu_screen import MenuScreen

class App:
    WIDTH = 1200
    HEIGHT = 800
    FPS = 60

    def __init__(self):
        self.selected_map = None
        self.selected_algorithm = None
        self.selected_agent = None
        pygame.init()

        self.screen = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT)
        )
        pygame.display.set_caption("Sokoban")

        self.clock = pygame.time.Clock()
        self.running = True
        self.current_screen = MenuScreen(self)

        self.background_color = MenuScreen.BACKGROUND

    def change_screen(self, new_screen):
        """Switch to another screen."""
        self.current_screen = new_screen

    def run(self):
        while self.running:
            dt = self.clock.tick(self.FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.current_screen is not None:
                    self.current_screen.handle_event(event)

            if self.current_screen is not None:
                self.current_screen.update(dt)

            self.screen.fill(self.background_color)

            if self.current_screen is not None:
                self.current_screen.draw(self.screen)

            pygame.display.flip()

        pygame.quit()



    def quit(self):
        self.running = False
