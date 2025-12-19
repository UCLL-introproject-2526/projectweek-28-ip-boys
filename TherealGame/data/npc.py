import pygame
from data import config

class Teacher:
    # Nieuwe parameter: sprite_type
    def __init__(self, x, y, sprite_type="teacher"):
        self.rect = pygame.Rect(x, y, config.TILE_SIZE, config.TILE_SIZE)
        self.defeated = False 
        self.active_dialogue = False
        self.sprite_type = sprite_type # Sla op welk plaatje we moeten gebruiken
        
    def is_player_near(self, player_rect, distance=80):
        # KEYWORD: PROXIMITY CHECK
        # [NL] We willen weten of de speler dichtbij genoeg is om te praten.
        # [NL] We gebruiken 'inflate' om de hitbox van de speler tijdelijk groter te maken.
        # [NL] Als deze grotere hitbox de leraar raakt, staan we dichtbij genoeg.
        return self.rect.colliderect(player_rect.inflate(distance, distance))

    def draw(self, screen, camera_x, camera_y, player_rect):
        if self.defeated: return
            
        draw_x = self.rect.x - camera_x
        draw_y = self.rect.y - camera_y
        
        # Gebruik self.sprite_type om het juiste plaatje uit de assets te halen
        if self.sprite_type in config.ASSETS:
            screen.blit(config.ASSETS[self.sprite_type], (draw_x, draw_y))
        else:
            # Fallback als plaatje mist
            color = (200, 200, 255)
            if self.sprite_type == "director": color = (0, 0, 0) # Zwart voor directeur
            pygame.draw.rect(screen, color, (draw_x, draw_y, config.TILE_SIZE, config.TILE_SIZE))

        if self.is_player_near(player_rect):
            font = pygame.font.Font(None, 32)
            e_text = font.render("E", True, (255, 255, 255))
            screen.blit(e_text,(draw_x + config.TILE_SIZE // 2 - 8, draw_y - 20))