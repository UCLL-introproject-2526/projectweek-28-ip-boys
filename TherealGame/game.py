import pygame
import config
import UCLL_maps as maps

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.tile_size = config.TILE_SIZE
        
        self.player_rect = pygame.Rect(0, 0, config.PLAYER_SIZE, config.PLAYER_SIZE)
        
        # NIEUW: We houden bij welke kant de speler op kijkt.
        # We beginnen met naar beneden (voren) kijken.
        self.player_direction = "down" 

        self.current_map_name = "ground"
        self.load_map("ground", 4, 22) 

    def load_map(self, map_name, start_tile_x, start_tile_y):
        self.current_map_name = map_name
        self.map_data = maps.ALL_MAPS[map_name]
        
        max_width = 0
        for row in self.map_data:
            if len(row) > max_width: max_width = len(row)

        self.map_pixel_width = max_width * self.tile_size
        self.map_pixel_height = len(self.map_data) * self.tile_size
        
        self.player_rect.x = start_tile_x * self.tile_size
        self.player_rect.y = start_tile_y * self.tile_size

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        # NIEUW: Als we een toets indrukken, veranderen we ook de 'player_direction'
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -config.PLAYER_SPEED
            self.player_direction = "left" # Kijk naar links
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]: # Gebruik elif zodat je niet links EN rechts tegelijk kijkt
            dx = config.PLAYER_SPEED
            self.player_direction = "right" # Kijk naar rechts

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -config.PLAYER_SPEED
            self.player_direction = "up" # Kijk naar boven/achteren
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = config.PLAYER_SPEED
            self.player_direction = "down" # Kijk naar beneden/voren

        # Beweging en botsingen (hetzelfde als eerst)
        self.player_rect.x += dx
        if self.check_wall_collision(): self.player_rect.x -= dx

        self.player_rect.y += dy
        if self.check_wall_collision(): self.player_rect.y -= dy
            
        self.player_rect.left = max(0, self.player_rect.left)
        self.player_rect.right = min(self.map_pixel_width, self.player_rect.right)
        self.player_rect.top = max(0, self.player_rect.top)
        self.player_rect.bottom = min(self.map_pixel_height, self.player_rect.bottom)

        self.check_events()

    def check_wall_collision(self):
        points = [self.player_rect.topleft, self.player_rect.topright,
                  self.player_rect.bottomleft, self.player_rect.bottomright]
        for point in points:
            col = int(point[0] // self.tile_size)
            row = int(point[1] // self.tile_size)
            
            if 0 <= row < len(self.map_data):
                row_len = len(self.map_data[row])
                if 0 <= col < row_len:
                    if self.map_data[row][col] == 'W': return True
        return False

    def check_events(self):
        center_x = self.player_rect.centerx
        center_y = self.player_rect.centery
        col = int(center_x // self.tile_size)
        row = int(center_y // self.tile_size)

        if 0 <= row < len(self.map_data):
            if 0 <= col < len(self.map_data[row]):
                tile_char = self.map_data[row][col]
            
                if tile_char == '>':
                    print("Trap omhoog!")
                    self.load_map("first", 77, 22) 
                elif tile_char == '<':
                    print("Trap omlaag!")
                    self.load_map("ground", 77, 22) 

    def draw(self):
        self.screen.fill(config.BLACK)

        camera_x = self.player_rect.centerx - (config.SCREEN_WIDTH // 2)
        camera_y = self.player_rect.centery - (config.SCREEN_HEIGHT // 2)
        
        camera_x = max(0, min(camera_x, self.map_pixel_width - config.SCREEN_WIDTH))
        camera_y = max(0, min(camera_y, self.map_pixel_height - config.SCREEN_HEIGHT))

        start_col = int(camera_x // self.tile_size)
        end_col = start_col + (config.SCREEN_WIDTH // self.tile_size) + 2
        start_row = int(camera_y // self.tile_size)
        end_row = start_row + (config.SCREEN_HEIGHT // self.tile_size) + 2

        # 1. TEKEN DE MAP
        for row in range(start_row, min(end_row, len(self.map_data))):
            current_row_len = len(self.map_data[row])
            for col in range(start_col, min(end_col, current_row_len)):
                char = self.map_data[row][col]
                x = (col * self.tile_size) - camera_x
                y = (row * self.tile_size) - camera_y

                # Vloer tekenen (als fallback of ondergrond)
                if "floor" in config.ASSETS: self.screen.blit(config.ASSETS["floor"], (x, y))
                else: pygame.draw.rect(self.screen, (100,100,100), (x, y, self.tile_size, self.tile_size))

                # Objecten tekenen
                img = None
                if char == 'W': 
                    if "wall" in config.ASSETS: img = config.ASSETS["wall"]
                    else: pygame.draw.rect(self.screen, (50,50,50), (x,y, self.tile_size, self.tile_size))
                elif char == 'D': 
                    if "door" in config.ASSETS: img = config.ASSETS["door"]
                    else: pygame.draw.rect(self.screen, (0,0,255), (x,y, self.tile_size, self.tile_size))
                elif char == '>' or char == '<': 
                    if "stairs" in config.ASSETS: img = config.ASSETS["stairs"]
                    else: pygame.draw.rect(self.screen, (255,255,0), (x,y, self.tile_size, self.tile_size))

                if img: self.screen.blit(img, (x, y))

        # 2. TEKEN DE SPELER (NIEUW!)
        player_draw_x = self.player_rect.x - camera_x
        player_draw_y = self.player_rect.y - camera_y

        # Check of de sprites geladen zijn
        if "player_sprites" in config.ASSETS and config.ASSETS["player_sprites"]:
            # NIEUW: Kies het juiste plaatje op basis van de richting
            direction = self.player_direction 
            sprite_to_draw = config.ASSETS["player_sprites"][direction]
            self.screen.blit(sprite_to_draw, (player_draw_x, player_draw_y))
        else:
            # Fallback: Rood blokje als er iets mis is met de plaatjes
            draw_rect = pygame.Rect(player_draw_x, player_draw_y, self.player_rect.width, self.player_rect.height)
            pygame.draw.rect(self.screen, config.PLAYER_COLOR, draw_rect)

        pygame.display.flip()