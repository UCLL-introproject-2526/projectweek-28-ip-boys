import pygame
import random

class Particle:
    def __init__(self, x, y, color, speed_range=3, size_range=4, lifetime=30):
        self.x = x
        self.y = y
        self.color = color
        # Willekeurige snelheid
        self.dx = random.uniform(-speed_range, speed_range)
        self.dy = random.uniform(-speed_range, speed_range)
        self.size = random.randint(2, size_range)
        self.lifetime = lifetime # Hoeveel frames hij bestaat
        self.original_lifetime = lifetime

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1
        # Maak ze kleiner als ze sterven
        if self.lifetime < 10:
            self.size = max(0, self.size - 0.2)

    def draw(self, screen, camera_x, camera_y):
        if self.lifetime > 0 and self.size > 0:
            draw_x = self.x - camera_x
            draw_y = self.y - camera_y
            pygame.draw.rect(screen, self.color, (draw_x, draw_y, self.size, self.size))