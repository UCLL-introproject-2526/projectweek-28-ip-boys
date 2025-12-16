import pygame
import config
import UCLL_maps as maps

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.tile_size = config.TILE_SIZE
        
        # De hitbox blijft 40 (zodat je nergens vast komt te zitten)
        self.player_rect = pygame.Rect(0, 0, config.PLAYER_SIZE, config.PLAYER_SIZE)
        self.player_direction = "down" 

        # Startpositie: We zoeken gewoon een lege plek op de map
        self.load_map("ground") 
        # Zet speler handmatig op een logische startplek (bijv in de inkomhal)
        self.player_rect.x = 4 * self.tile_size
        self.player_rect.y = 25 * self.tile_size

    def load_map(self, map_name):
        self.current_map_name = map_name
        self.map_data = maps.ALL_MAPS[map_name]
        
        # Bereken breedte/hoogte van de nieuwe map
        max_width = 0
        for row in self.map_data:
            if len(row) > max_width:
                max_width = len(row)

        self.map_pixel_width = max_width * self.tile_size
        self.map_pixel_height = len(self.map_data) * self.tile_size

    def find_spawn_point(self, target_char):
        """
        Deze functie zoekt op de HUIDIGE map naar een specifiek teken (bijv '<' of '>')
        en geeft de X en Y coördinaten terug.
        """
        for row_idx, row in enumerate(self.map_data):
            for col_idx, char in enumerate(row):
                if char == target_char:
                    # We hebben de trap gevonden!
                    # Zet de speler er iets NAAST (anders val je gelijk terug)
                    return (col_idx - 1) * self.tile_size, row_idx * self.tile_size
        
        # Als we niks vinden, zet speler op 2,2
        return 2 * self.tile_size, 2 * self.tile_size

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -config.PLAYER_SPEED
            self.player_direction = "left"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = config.PLAYER_SPEED
            self.player_direction = "right"

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -config.PLAYER_SPEED
            self.player_direction = "up"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = config.PLAYER_SPEED
            self.player_direction = "down"

        # Beweeg X
        self.player_rect.x += dx
        if self.check_wall_collision(): self.player_rect.x -= dx

        # Beweeg Y
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

        if 0 <= row < len(self.map_data) and 0 <= col < len(self.map_data[row]):
            tile_char = self.map_data[row][col]
            
            # === DE AUTOMATISCHE TRAP LOGICA ===
            if tile_char == '>':
                print("Trap omhoog! Zoeken naar '<' op map 'first'...")
                self.load_map("first")
                # Zoek waar de trap naar beneden staat, en zet de speler daar
                new_x, new_y = self.find_spawn_point('<')
                self.player_rect.x = new_x
                self.player_rect.y = new_y
                
            elif tile_char == '<':
                print("Trap omlaag! Zoeken naar '>' op map 'ground'...")
                self.load_map("ground")
                # Zoek waar de trap naar boven staat, en zet de speler daar
                new_x, new_y = self.find_spawn_point('>')
                self.player_rect.x = new_x
                self.player_rect.y = new_y

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

        # 1. MAP
        for row in range(start_row, min(end_row, len(self.map_data))):
            
            # --- DE FIX ---
            # We kijken hoe lang DEZE specifieke regel is
            current_row_len = len(self.map_data[row])
            
            # We tekenen alleen kolommen die bestaan in deze regel
            for col in range(start_col, min(end_col, current_row_len)):
                char = self.map_data[row][col]
                x = (col * self.tile_size) - camera_x
                y = (row * self.tile_size) - camera_y

                if "floor" in config.ASSETS: self.screen.blit(config.ASSETS["floor"], (x, y))
                else: pygame.draw.rect(self.screen, (100,100,100), (x, y, self.tile_size, self.tile_size))

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

        # 2. SPELER
        player_draw_x = self.player_rect.x - camera_x
        player_draw_y = self.player_rect.y - camera_y

        if "player_sprites" in config.ASSETS and config.ASSETS["player_sprites"]:
            direction = self.player_direction 
            sprite_to_draw = config.ASSETS["player_sprites"][direction]
            
            # Centreer de grote sprite over de kleine hitbox
            offset_x = (config.PLAYER_VISUAL_SIZE - config.PLAYER_SIZE) // 2
            offset_y = config.PLAYER_VISUAL_SIZE - config.PLAYER_SIZE
            
            self.screen.blit(sprite_to_draw, (player_draw_x - offset_x, player_draw_y - offset_y))
        else:
            pygame.draw.rect(self.screen, config.PLAYER_COLOR, (player_draw_x, player_draw_y, config.PLAYER_SIZE, config.PLAYER_SIZE))

        pygame.display.flip()