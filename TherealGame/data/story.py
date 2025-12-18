import pygame
import os
from data import config

class Story:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 32)

        self.lines = [
            "Welcome To University Colleges Leuven-Limburg",
            "You'll either survive... or become a teacher",
            "Forget exams! The real challenge is staying alive",
            "AH! AH! AH! AH! STAYING ALIVE! STAYING ALIVE! AH UHM...!",
            "School survival 101: don't become a snack",
            "GOOD LUCK"
        ]
        self.current_line = 0

        # Gebruik de assets dictionary of laad specifiek
        if "boss" in config.ASSETS:
             self.boss = config.ASSETS["boss"]
        else:
             self.boss = pygame.Surface((260, 260))

        if os.path.exists(os.path.join(config.IMAGE_PATH, "background_story.webp")):
             self.background = pygame.image.load(os.path.join(config.IMAGE_PATH, "background_story.webp")).convert()
             self.background = pygame.transform.scale(self.background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        else:
             self.background = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
             self.background.fill((0,0,0))

    def handle_click(self):
        self.current_line += 1

    def finished(self):
        return self.current_line >= len(self.lines)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.boss, (40, config.SCREEN_HEIGHT - self.boss.get_height() - 40))

        text_box = pygame.Rect(30, config.SCREEN_HEIGHT - 140, config.SCREEN_WIDTH - 60, 100)
        pygame.draw.rect(self.screen, (220, 220, 220), text_box, border_radius=12)

        if self.current_line < len(self.lines):
            text = self.font.render(self.lines[self.current_line], True, (0, 0, 0))
            self.screen.blit(text, (text_box.x + 20, text_box.y + 35))

        pygame.display.flip()