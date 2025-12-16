import pygame
import config

class Projectile:
    def __init__(self, x, y, direction, weapon_type):
        self.rect = pygame.Rect(x, y, config.BULLET_SIZE, config.BULLET_SIZE)
        self.direction = direction 
        self.active = True
        
        # Haal stats op uit config op basis van wapen (pistol/shotgun)
        stats = config.WEAPONS[weapon_type]
        self.speed = stats["speed"]
        self.damage = stats["damage"]
        self.color = stats["color"]

    def update(self):
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

        if (self.rect.right < 0 or self.rect.left > 10000 or 
            self.rect.bottom < 0 or self.rect.top > 10000):
            self.active = False

    def draw(self, screen, camera_x, camera_y):
        pygame.draw.rect(screen, self.color, 
                         (self.rect.x - camera_x, self.rect.y - camera_y, 
                          config.BULLET_SIZE, config.BULLET_SIZE))