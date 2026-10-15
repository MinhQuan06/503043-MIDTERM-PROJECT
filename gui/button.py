
import pygame


class Button:
    def __init__(self, rect, text, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback

        self.normal_color = (139, 132, 76)
        self.hover_color = (80, 120, 75)
        self.text_color = (255, 255, 255)

        self.font = pygame.font.SysFont("arial", 24, bold=True)

    def handle_event(self, event):
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        ):
            self.callback()

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = (
            self.hover_color
            if self.rect.collidepoint(mouse_pos)
            else self.normal_color
        )

        pygame.draw.rect(
            surface, color, self.rect, border_radius=10
        )

        label = self.font.render(
            self.text, True, self.text_color
        )
        surface.blit(
            label, label.get_rect(center=self.rect.center)
        )
