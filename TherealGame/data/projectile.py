import pygame
from data import config

class Projectile:
    def __init__(self, x, y, direction, weapon_type):
        self.rect = pygame.Rect(x, y, config.BULLET_SIZE, config.BULLET_SIZE)
        self.direction = direction 
        self.active = True
        stats = config.WEAPONS[weapon_type]
        self.speed = stats["speed"]
        self.damage = stats["damage"]
        self.color = stats["color"]

    def update(self):
        if self.direction == "up": self.rect.y -= self.speed
        elif self.direction == "down": self.rect.y += self.speed
        elif self.direction == "left": self.rect.x -= self.speed
        elif self.direction == "right": self.rect.x += self.speed

        # KEYWORD: MEMORY MANAGEMENT
        # [NL] Als een kogel buiten het spel vliegt, moet hij weg.
        # [NL] We checken hier of de coördinaten te groot of te klein zijn.
        # [NL] Zo ja, zetten we 'active' op False. game.py zal hem dan uit de lijst verwijderen.
        if (self.rect.right < 0 or self.rect.left > 10000 or self.rect.bottom < 0 or self.rect.top > 10000):
            self.active = False

    def draw(self, screen, camera_x, camera_y):
        if "projectile" in config.ASSETS:
            screen.blit(config.ASSETS["projectile"], (self.rect.x - camera_x, self.rect.y - camera_y))
        else:
            pygame.draw.circle(screen, self.color, (self.rect.centerx - camera_x, self.rect.centery - camera_y), config.BULLET_SIZE // 2)