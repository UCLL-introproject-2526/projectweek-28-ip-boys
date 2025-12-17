import pygame
import config

class Projectile:
    def __init__(self, x, y, direction, weapon_type):
        self.rect = pygame.Rect(x, y, config.BULLET_SIZE, config.BULLET_SIZE)
        self.direction = direction 
        self.active = True
        
        # Haal stats op uit config
        stats = config.WEAPONS[weapon_type]
        self.speed = stats["speed"]
        self.damage = stats["damage"]
        # Kleur wordt nu genegeerd voor het tekenen, maar stats blijven
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

        # Verwijder kogel als hij ver buiten beeld is
        if (self.rect.right < 0 or self.rect.left > 10000 or 
            self.rect.bottom < 0 or self.rect.top > 10000):
            self.active = False

    def draw(self, screen, camera_x, camera_y):
        # Teken de bubble.png
        if "projectile" in config.ASSETS:
            screen.blit(config.ASSETS["projectile"], (self.rect.x - camera_x, self.rect.y - camera_y))
        else:
            # Fallback als plaatje mist: teken toch een bolletje
            pygame.draw.circle(screen, self.color, 
                             (self.rect.centerx - camera_x, self.rect.centery - camera_y), 
                             config.BULLET_SIZE // 2)