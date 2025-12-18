import pygame
import random

class Particle:
    def __init__(self, x, y, color, speed_range=3, size_range=4, lifetime=30):
        self.x = x
        self.y = y
        self.color = color
        self.dx = random.uniform(-speed_range, speed_range)
        self.dy = random.uniform(-speed_range, speed_range)
        self.size = random.randint(2, size_range)
        self.lifetime = lifetime 
        self.original_lifetime = lifetime

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1
        if self.lifetime < 10:
            self.size = max(0, self.size - 0.2)

    def draw(self, screen, camera_x, camera_y):
        if self.lifetime > 0 and self.size > 0:
            draw_x = int(self.x - camera_x)
            draw_y = int(self.y - camera_y)
            pygame.draw.circle(screen, self.color, (draw_x, draw_y), int(self.size))
            if self.size > 2:
                pygame.draw.circle(screen, (255, 255, 255), (draw_x, draw_y), int(self.size), 1)