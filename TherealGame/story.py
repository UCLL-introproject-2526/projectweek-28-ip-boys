import pygame
import os
import config


class Story:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 32)

        # ---- PADEN (BELANGRIJK) ----
        base_dir = os.path.dirname(__file__)
        image_dir = os.path.join(base_dir, "images")
        self.boss_image_path = os.path.join(image_dir, "boss.png")
        self.background_path = os.path.join(image_dir, "background_story.webp")

        # ---- STORY TEKST ----
        self.lines = [
            "Welcome To University Colleges Leuven-Limburg",
            "You'll either survive... or become a teacher",
            "Forget exams! The real challenge is staying alive",
            "AH! AH! AH! AH! STAYING ALIVE! STAYING ALIVE! AH UHM...!",
            "School survival 101: don't become a snack",
            "GOOD LUCK"
        ]

        self.current_line = 0

        # ---- IMAGE ----
        self.boss = pygame.image.load(self.boss_image_path).convert_alpha()
        self.boss = pygame.transform.scale(self.boss, (260, 260))

        # ---- BACKGROUND ----
        self.background = pygame.image.load(self.background_path).convert()
        self.background = pygame.transform.scale(
            self.background,
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
)


    def handle_click(self):
        self.current_line += 1

    def finished(self):
        return self.current_line >= len(self.lines)

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        # Boss tekenen
        self.screen.blit(
            self.boss,
            (40, config.SCREEN_HEIGHT - self.boss.get_height() - 40)
        )

        # Tekst box
        text_box = pygame.Rect(
            30,
            config.SCREEN_HEIGHT - 140,
            config.SCREEN_WIDTH - 60,
            100
        )

        pygame.draw.rect(
            self.screen,
            (220, 220, 220),
            text_box,
            border_radius=12
        )

        # Tekst
        if self.current_line < len(self.lines):
            text = self.font.render(
                self.lines[self.current_line],
                True,
                (0, 0, 0)
            )
            self.screen.blit(text, (text_box.x + 20, text_box.y + 35))

        pygame.display.flip()
