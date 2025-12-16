import pygame
import config

class Item:
    def __init__(self, x, y, item_type):
        self.rect = pygame.Rect(x + 16, y + 16, config.ITEM_SIZE, config.ITEM_SIZE) 
        self.item_type = item_type # "health", "ammo", "shotgun", "key"
        self.start_y = y 
        self.float_offset = 0
        self.float_direction = 0.5

    def draw(self, screen, camera_x, camera_y):
        self.float_offset += self.float_direction
        if abs(self.float_offset) > 5: self.float_direction *= -1
        
        draw_x = self.rect.x - camera_x
        draw_y = self.rect.y - camera_y + self.float_offset

        asset_name = f"item_{self.item_type}"
        if asset_name in config.ASSETS:
             screen.blit(config.ASSETS[asset_name], (draw_x, draw_y))
        else:
             color = (255, 255, 255)
             if self.item_type == "health": color = (0, 255, 0)
             if self.item_type == "ammo": color = (255, 255, 0)
             if self.item_type == "shotgun": color = (255, 0, 0)
             if self.item_type == "key": color = (255, 215, 0) # Goud
             pygame.draw.rect(screen, color, (draw_x, draw_y, config.ITEM_SIZE, config.ITEM_SIZE))