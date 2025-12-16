import pygame
import config
import UCLL_maps as maps
from enemy import Enemy

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.tile_size = config.TILE_SIZE
        
        self.player_rect = pygame.Rect(0, 0, config.PLAYER_SIZE, config.PLAYER_SIZE)
        self.player_direction = "down" 

        # LIJST VOOR VIJANDEN
        self.enemies = []

        # Startpositie
        self.load_map("ground") 
        self.player_rect.x = 4 * self.tile_size
        self.player_rect.y = 25 * self.tile_size

    def load_map(self, map_name):
        self.current_map_name = map_name
        self.map_data_original = maps.ALL_MAPS[map_name]
        
        # We maken een nieuwe lijst voor map_data, omdat we de 'Z's eruit gaan halen
        self.map_data = []
        self.enemies = [] # Lijst leegmaken bij nieuwe map
        
        max_width = 0
        
        for row_idx, row_string in enumerate(self.map_data_original):
            if len(row_string) > max_width: max_width = len(row_string)
            
            # Check of er een Z in deze rij staat
            if 'Z' in row_string:
                new_row = ""
                for col_idx, char in enumerate(row_string):
                    if char == 'Z':
                        # MAAK ENEMY
                        new_enemy = Enemy(
                            col_idx * self.tile_size,
                            row_idx * self.tile_size,
                            self.map_data_original)
                        self.enemies.append(new_enemy)
                        new_row += "." # Vervang Z door vloer
                    else:
                        new_row += char
                self.map_data.append(new_row)
            else:
                self.map_data.append(row_string)

        self.map_pixel_width = max_width * self.tile_size
        self.map_pixel_height = len(self.map_data) * self.tile_size

    def find_spawn_point(self, target_char):
        for row_idx, row in enumerate(self.map_data):
            for col_idx, char in enumerate(row):
                if char == target_char:
                    return (col_idx - 1) * self.tile_size, row_idx * self.tile_size
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
        
        # UPDATE ALLE VIJANDEN
        for e in self.enemies:
            e.update(self.player_rect)


        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            for e in self.enemies:
                if not e.alive:
                    continue

                if self.player_rect.colliderect(e.rect):
                    e.hp -= 10
                    print("HIT! Enemy HP:", e.hp)

                    if e.hp <= 0:
                        print("ENEMY DEAD")
                        e.alive = False


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

        if 0 <= row < len(self.map_data) and 0 <= col < len(self.map_data[row]):
            tile_char = self.map_data[row][col]
            if tile_char == '>':
                self.load_map("first")
                new_x, new_y = self.find_spawn_point('<')
                self.player_rect.x = new_x
                self.player_rect.y = new_y
            elif tile_char == '<':
                self.load_map("ground")
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
            current_row_len = len(self.map_data[row])
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

        # 2. VIJANDEN (NIEUW)
        for e in self.enemies:
            e.draw(self.screen, camera_x, camera_y)

        # 3. SPELER
        player_draw_x = self.player_rect.x - camera_x
        player_draw_y = self.player_rect.y - camera_y

        if "player_sprites" in config.ASSETS and config.ASSETS["player_sprites"]:
            direction = self.player_direction 
            sprite_to_draw = config.ASSETS["player_sprites"][direction]
            offset_x = (config.PLAYER_VISUAL_SIZE - config.PLAYER_SIZE) // 2
            offset_y = config.PLAYER_VISUAL_SIZE - config.PLAYER_SIZE
            self.screen.blit(sprite_to_draw, (player_draw_x - offset_x, player_draw_y - offset_y))
        else:
            pygame.draw.rect(self.screen, config.PLAYER_COLOR, (player_draw_x, player_draw_y, config.PLAYER_SIZE, config.PLAYER_SIZE))

        pygame.display.flip()