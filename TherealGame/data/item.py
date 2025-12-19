import pygame
from data import config

class Item:
    def __init__(self, x, y, item_type):
        self.rect = pygame.Rect(x + 16, y + 16, config.ITEM_SIZE, config.ITEM_SIZE) 
        self.item_type = item_type
        self.start_y = y 
        self.float_offset = 0
        self.float_direction = 0.5

    def draw(self, screen, camera_x, camera_y):
        # KEYWORD: FLOATING ANIMATION
        # [NL] We laten het item op en neer zweven om de aandacht te trekken.
        # [NL] We tellen steeds een klein beetje bij de offset op.
        # [NL] Als de offset te groot wordt (> 5), draaien we de richting om (float_direction *= -1).
        self.float_offset += self.float_direction
        if abs(self.float_offset) > 5: self.float_direction *= -1
        
        offset_x = (config.ITEM_VISUAL_SIZE - config.ITEM_SIZE) // 2
        offset_y = (config.ITEM_VISUAL_SIZE - config.ITEM_SIZE) // 2
        
        draw_x = self.rect.x - camera_x - offset_x
        draw_y = self.rect.y - camera_y - offset_y + self.float_offset

        asset_name = f"item_{self.item_type}"
        if asset_name in config.ASSETS:
             screen.blit(config.ASSETS[asset_name], (draw_x, draw_y))
        else:
             color = (255, 255, 255)
             if self.item_type == "health": color = (0, 255, 0)
             if self.item_type == "ammo": color = (255, 255, 0)
             if self.item_type == "shotgun": color = (255, 0, 0)
             if self.item_type == "key": color = (255, 215, 0) 
             pygame.draw.rect(screen, color, (draw_x + offset_x, draw_y + offset_y, config.ITEM_SIZE, config.ITEM_SIZE))