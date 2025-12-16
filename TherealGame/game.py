import pygame
import config
import UCLL_maps as maps

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.tile_size = config.TILE_SIZE
        
        self.player_rect = pygame.Rect(0, 0, config.PLAYER_SIZE, config.PLAYER_SIZE)

        # Start op het gelijkvloers
        # Let op: startpositie aangepast aan de nieuwe map structuur
        self.current_map_name = "ground"
        self.load_map("ground", 4, 22) 

    def load_map(self, map_name, start_tile_x, start_tile_y):
        self.current_map_name = map_name
        self.map_data = maps.ALL_MAPS[map_name]
        
        # We berekenen hier de maximale breedte voor de camera limieten
        # (We nemen de langste regel als referentie voor de breedte van de wereld)
        max_width = 0
        for row in self.map_data:
            if len(row) > max_width:
                max_width = len(row)

        self.map_pixel_width = max_width * self.tile_size
        self.map_pixel_height = len(self.map_data) * self.tile_size
        
        self.player_rect.x = start_tile_x * self.tile_size
        self.player_rect.y = start_tile_y * self.tile_size

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -config.PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = config.PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -config.PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = config.PLAYER_SPEED

        self.player_rect.x += dx
        if self.check_wall_collision(): self.player_rect.x -= dx

        self.player_rect.y += dy
        if self.check_wall_collision(): self.player_rect.y -= dy
            
        self.player_rect.left = max(0, self.player_rect.left)
        self.player_rect.right = min(self.map_pixel_width, self.player_rect.right)
        self.player_rect.top = max(0, self.player_rect.top)
        self.player_rect.bottom = min(self.map_pixel_height, self.player_rect.bottom)

        self.check_events()
        
        # DEBUG: Haal hekje weg als je coördinaten wilt zien in de console
        # grid_x = int(self.player_rect.centerx // self.tile_size)
        # grid_y = int(self.player_rect.centery // self.tile_size)
        # print(f"Speler positie: {grid_x}, {grid_y}") 

    def check_wall_collision(self):
        points = [self.player_rect.topleft, self.player_rect.topright,
                  self.player_rect.bottomleft, self.player_rect.bottomright]
        for point in points:
            col = int(point[0] // self.tile_size)
            row = int(point[1] // self.tile_size)
            
            # Veilige check: bestaat deze rij en kolom wel?
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

        # Veilige check
        if 0 <= row < len(self.map_data):
            if 0 <= col < len(self.map_data[row]):
                tile_char = self.map_data[row][col]
            
                if tile_char == '>': # Trap omhoog
                    print("Trap omhoog!")
                    self.load_map("first", 77, 22) 
                
                elif tile_char == '<': # Trap omlaag
                    print("Trap omlaag!")
                    self.load_map("ground", 77, 22) 

    def draw(self):
        self.screen.fill(config.BLACK)

        camera_x = self.player_rect.centerx - (config.SCREEN_WIDTH // 2)
        camera_y = self.player_rect.centery - (config.SCREEN_HEIGHT // 2)
        
        # Camera clamp (zorgen dat camera niet buiten de map kijkt)
        camera_x = max(0, min(camera_x, self.map_pixel_width - config.SCREEN_WIDTH))
        camera_y = max(0, min(camera_y, self.map_pixel_height - config.SCREEN_HEIGHT))

        start_col = int(camera_x // self.tile_size)
        end_col = start_col + (config.SCREEN_WIDTH // self.tile_size) + 2
        start_row = int(camera_y // self.tile_size)
        end_row = start_row + (config.SCREEN_HEIGHT // self.tile_size) + 2

        # Loop door de rijen
        for row in range(start_row, min(end_row, len(self.map_data))):
            
            # --- DE FIX ---
            # We kijken hoe lang DEZE specifieke regel is
            current_row_len = len(self.map_data[row])
            
            # We tekenen alleen kolommen die bestaan in deze regel
            for col in range(start_col, min(end_col, current_row_len)):
                char = self.map_data[row][col]
                x = (col * self.tile_size) - camera_x
                y = (row * self.tile_size) - camera_y

                color = config.GRAY
                if char == 'W': color = config.DARK_GRAY
                elif char == 'D': color = config.BLUE
                elif char == '>' or char == '<': color = config.YELLOW

                pygame.draw.rect(self.screen, color, (x, y, self.tile_size, self.tile_size))
                pygame.draw.rect(self.screen, (30, 30, 30), (x, y, self.tile_size, self.tile_size), 1)

        draw_rect = pygame.Rect(
            self.player_rect.x - camera_x,
            self.player_rect.y - camera_y,
            self.player_rect.width,
            self.player_rect.height
        )
        pygame.draw.rect(self.screen, config.PLAYER_COLOR, draw_rect)

        pygame.display.flip()


