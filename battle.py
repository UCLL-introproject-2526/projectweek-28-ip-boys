import pygame
import random
import config

class Battle:
    def __init__(self, screen, player, enemy):
        self.screen = screen
        self.player = player
        self.enemy = enemy

        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 48)

        self.turn = "player"
        self.running = True
        self.message = f"Een wild {enemy['name']} verschijnt!"

    def draw_text(self, text, x, y, color=config.WHITE):
        img = self.font.render(text, True, color)
        self.screen.blit(img, (x, y))

    def attack(self, attacker, defender):
        damage = random.randint(8, 18)
        defender["hp"] -= damage
        return damage

    def draw_ui(self):
        self.screen.fill((30, 30, 30))

        # Namen + HP
        self.draw_text(f"{self.player['name']} HP: {self.player['hp']}", 50, 450)
        self.draw_text(f"{self.enemy['name']} HP: {self.enemy['hp']}", 600, 100)

        # Battle message
        msg = self.big_font.render(self.message, True, config.WHITE)
        self.screen.blit(msg, (50, 520))

        # Attack knop
        self.attack_button = pygame.Rect(50, 600, 200, 50)
        pygame.draw.rect(self.screen, (0, 180, 0), self.attack_button, border_radius=8)
        self.draw_text("ATTACK", 105, 615, config.BLACK)

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.turn == "player" and self.attack_button.collidepoint(event.pos):
                        dmg = self.attack(self.player, self.enemy)
                        self.message = f"Jij doet {dmg} damage!"
                        self.turn = "enemy"
