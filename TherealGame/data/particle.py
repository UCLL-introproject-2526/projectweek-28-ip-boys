import pygame
import random
from data import config

class Particle:
    """Dit is de standaard 'Splat' particle (kleine bolletjes die wegvliegen)"""
    def __init__(self, x, y, color, speed_range=4, size_range=6, lifetime=40):
        self.x = x
        self.y = y
        self.color = color
        # Willekeurige richting (explosie effect)
        self.dx = random.uniform(-speed_range, speed_range)
        self.dy = random.uniform(-speed_range, speed_range)
        self.size = random.randint(3, size_range)
        self.lifetime = lifetime 
        self.original_lifetime = lifetime

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1
        
        # Laat ze krimpen
        if self.lifetime < 15:
            self.size = max(0, self.size - 0.3)

    def draw(self, screen, camera_x, camera_y):
        if self.lifetime > 0 and self.size > 0:
            draw_x = int(self.x - camera_x)
            draw_y = int(self.y - camera_y)
            pygame.draw.circle(screen, self.color, (draw_x, draw_y), int(self.size))


class CuredStudent:
    """NIEUW: De geredde student in een bubbel die omhoog vliegt"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dy = -1.5 # Vliegt langzaam omhoog
        self.lifetime = 120 # Blijft 2 seconden zichtbaar
        self.wobble = 0
        self.wobble_speed = 0.1

    def update(self):
        self.y += self.dy
        self.lifetime -= 1
        self.wobble += self.wobble_speed

    def draw(self, screen, camera_x, camera_y):
        if self.lifetime > 0:
            draw_x = int(self.x - camera_x)
            
            # Beetje wiebelen links/rechts voor zweef effect
            import math
            wobble_offset = math.sin(self.wobble) * 5 
            draw_x += wobble_offset
            draw_y = int(self.y - camera_y)

            # 1. Teken de grote bubbel (96px)
            # We tekenen deze eerst zodat de student erin of er 'op' lijkt te zitten
            if "bubble_large" in config.ASSETS:
                bubble = config.ASSETS["bubble_large"]
                screen.blit(bubble, (draw_x - bubble.get_width()//2, draw_y - bubble.get_height()//2))
            else:
                # Fallback grote cirkel
                pygame.draw.circle(screen, (0, 200, 255), (int(draw_x), int(draw_y)), 48, 2)

            # 2. Teken de student sprite (64px) gecentreerd in de bubbel
            if "student_icon" in config.ASSETS:
                icon = config.ASSETS["student_icon"]
                screen.blit(icon, (draw_x - icon.get_width()//2, draw_y - icon.get_height()//2))
            else:
                # Fallback blokje
                pygame.draw.rect(screen, (0,0,255), (draw_x-32, draw_y-32, 64, 64))