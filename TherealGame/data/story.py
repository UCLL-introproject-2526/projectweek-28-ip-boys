import pygame
import os
from data import config

class Story:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 32)

        # ---- PADEN (AANGEPAST) ----
        # We gebruiken nu config.IMAGE_PATH zodat hij in assets/images kijkt
        self.boss_image_path = os.path.join(config.IMAGE_PATH, "boss.png")
        self.background_path = os.path.join(config.IMAGE_PATH, "background_story.webp")

        # ---- STORY TEKST ----
        self.lines = [
            "Welcome to University Colleges Leuven-Limburg.",
            "Your mission, if you choose to accept it...",
            "Eliminate the Teacher inside every classroom.",
            "Teachers are powerful. Use your ammo wisely.",
            "Get hit? Find a medkit. There is one in every classroom.",
            "You cannot leave a classroom until the Teacher is defeated.",
            "After defeating all Teachers, go upstairs.",
            "Use the stairs to reach the first floor.",
            "Find the key to unlock the final room.",
            "To win: eliminate all Teachers and survive the zombies.",
            "Big tip: You need at least 80 ammo and full health.",
            "Anything less... and you become staff."
        ]

        self.current_line = 0

        # ---- IMAGE (MET SAFETY CHECK) ----
        # Probeer boss.png te laden, anders een paars vierkant
        if os.path.exists(self.boss_image_path):
            try:
                self.boss = pygame.image.load(self.boss_image_path).convert_alpha()
            except Exception as e:
                print(f"Fout bij laden boss: {e}")
                self.boss = self._create_placeholder((100, 0, 100))
        else:
            print(f"Let op: boss.png niet gevonden in {self.boss_image_path}")
            self.boss = self._create_placeholder((100, 0, 100))
            
        self.boss = pygame.transform.scale(self.boss, (260, 260))

        # ---- BACKGROUND (MET SAFETY CHECK) ----
        if os.path.exists(self.background_path):
            try:
                self.background = pygame.image.load(self.background_path).convert()
            except:
                 self.background = self._create_placeholder((20, 20, 40))
        else:
            self.background = self._create_placeholder((20, 20, 40))

        self.background = pygame.transform.scale(
            self.background,
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )

        # ---- TEXTBOX ANIMATIE ----
        self.textbox_x = 30
        self.textbox_width = config.SCREEN_WIDTH - 60
        self.textbox_height = 100

        self.textbox_target_y = config.SCREEN_HEIGHT - 140
        self.textbox_y = config.SCREEN_HEIGHT + 120 
        self.textbox_speed = 8

    def _create_placeholder(self, color):
        """Hulpfunctie om een leeg vlak te maken als een plaatje mist"""
        s = pygame.Surface((260, 260))
        s.fill(color)
        return s

    def handle_click(self):
        self.current_line += 1
        # textbox opnieuw laten inschuiven
        self.textbox_y = config.SCREEN_HEIGHT + 120

    def finished(self):
        return self.current_line >= len(self.lines)

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        # Boss tekenen
        self.screen.blit(
            self.boss,
            (40, config.SCREEN_HEIGHT - self.boss.get_height() - 40)
        )

        # ---- TEXTBOX BEWEGING ----
        # KEYWORD: SLIDE ANIMATION
        # [NL] We willen dat het tekstvak mooi van onder naar boven schuift.
        # [NL] We checken of de huidige Y-positie (textbox_y) groter is dan het doel (target_y).
        # [NL] Zo ja, trekken we er elke frame de snelheid vanaf. Dit creëert de animatie.
        if self.textbox_y > self.textbox_target_y:
            self.textbox_y -= self.textbox_speed
            if self.textbox_y < self.textbox_target_y:
                self.textbox_y = self.textbox_target_y

        # Tekst box
        text_box = pygame.Rect(
            self.textbox_x,
            self.textbox_y,
            self.textbox_width,
            self.textbox_height
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