import pygame
import config

class Projectile:
    def __init__(self, x, y, direction, weapon_type):
        self.rect = pygame.Rect(x, y, config.BULLET_SIZE, config.BULLET_SIZE)
        self.direction = direction 
        self.active = True
        
        # Haal stats op uit config op basis van wapen
        stats = config.WEAPONS[weapon_type]
        self.speed = stats["speed"]
        self.damage = stats["damage"]
        # We gebruiken nog steeds de wapenkleur, maar nu voor de bel
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
        # Bereken het midden van de bel
        center_x = self.rect.centerx - camera_x
        center_y = self.rect.centery - camera_y
        radius = config.BULLET_SIZE // 2

        # 1. Teken de bel (Gekleurde cirkel)
        pygame.draw.circle(screen, self.color, (center_x, center_y), radius)
        
        # 2. Teken een randje (donkerder of zwart voor contrast)
        pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), radius, 1)

        # 3. Teken de "shine" (Witte reflectie linksboven) - Maakt het een bel!
        pygame.draw.circle(screen, (255, 255, 255), (center_x - 2, center_y - 2), 2)