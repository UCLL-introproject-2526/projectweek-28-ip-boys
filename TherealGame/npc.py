import pygame
import config

class Teacher:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, config.TILE_SIZE, config.TILE_SIZE)
        self.defeated = False # Wordt True als de boss van deze leraar verslagen is
        self.active_dialogue = False
        
    def is_player_near(self, player_rect, distance=80):
        return self.rect.colliderect(
            player_rect.inflate(distance, distance)
    )

    def draw(self, screen, camera_x, camera_y, player_rect):
        if self.defeated:
            # Leraar is gered/weg, teken niets of een "vinkje"
            return
            
        draw_x = self.rect.x - camera_x
        draw_y = self.rect.y - camera_y
        
        if "teacher" in config.ASSETS:
            screen.blit(config.ASSETS["teacher"], (draw_x, draw_y))
        else:
            pygame.draw.rect(screen, (200, 200, 255), (draw_x, draw_y, config.TILE_SIZE, config.TILE_SIZE))

        # ---- E PROMPT ----
        if self.is_player_near(player_rect):
            font = pygame.font.Font(None, 32)
            e_text = font.render("E", True, (255, 255, 255))
            screen.blit(
                e_text,(draw_x + config.TILE_SIZE // 2 - 8, draw_y - 20))