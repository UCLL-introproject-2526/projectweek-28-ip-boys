import pygame
import config

class Teacher:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, config.TILE_SIZE, config.TILE_SIZE)
        self.defeated = False # Wordt True als de boss van deze leraar verslagen is
        self.active_dialogue = False
        
    def draw(self, screen, camera_x, camera_y):
        if self.defeated:
            # Leraar is gered/weg, teken niets of een "vinkje"
            return
            
        draw_x = self.rect.x - camera_x
        draw_y = self.rect.y - camera_y
        
        if "teacher" in config.ASSETS:
            screen.blit(config.ASSETS["teacher"], (draw_x, draw_y))
        else:
            pygame.draw.rect(screen, (200, 200, 255), (draw_x, draw_y, config.TILE_SIZE, config.TILE_SIZE))