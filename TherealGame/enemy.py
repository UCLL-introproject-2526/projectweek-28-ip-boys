import pygame
import random
import config
from collections import deque # Nodig voor het slimme padzoeken

class Enemy:
    def __init__(self, x, y, map_data, is_boss=False):
        # We gebruiken hier ENEMY_SIZE (64) uit config, of BOSS_SIZE
        size = config.BOSS_SIZE if is_boss else config.ENEMY_SIZE
        self.rect = pygame.Rect(x, y, size, size)
        self.map_data = map_data
        self.is_boss = is_boss
        
        self.hp = config.BOSS_HP if is_boss else config.NORMAL_HP
        self.alive = True
        self.is_cured = False 
        
        self.chase_radius = 400 if is_boss else 200
        self.speed = config.ENEMY_SPEED
        
        self.direction = (0, 0)
        self.move_timer = 0
        self.change_direction()
        
        # Kijkrichting
        self.facing_right = True 
        
        # NIEUW: AI & Pathfinding
        self.triggered = False # Wordt True als boss je ziet
        self.path_timer = 0
        self.next_step = None  # Waar moet ik NU heen lopen?

    def change_direction(self):
        possible_directions = [(self.speed, 0), (-self.speed, 0), (0, self.speed), (0, -self.speed), (0, 0)]
        self.direction = random.choice(possible_directions)
        self.move_timer = random.randint(30, 120)

    def take_damage(self, amount):
        if self.is_cured: return
        self.hp -= amount
        
        # Als je een boss pijn doet, weet hij je direct te vinden!
        if self.is_boss:
            self.triggered = True
            
        if self.hp <= 0:
            self.alive = False 
            self.is_cured = True 

    def get_grid_pos(self, x, y):
        """Zet pixel pos om naar grid pos (rij, kolom)"""
        return int(x // config.TILE_SIZE), int(y // config.TILE_SIZE)

    def is_walkable(self, col, row):
        """Check of een tegel begaanbaar is"""
        # Binnen de kaart blijven
        if row < 0 or row >= len(self.map_data) or col < 0 or col >= len(self.map_data[0]):
            return False
        
        tile = self.map_data[row][col]
        # Lijst van blokkades (Muren, Banken, Gesloten Deuren)
        if tile in ['W', 'b', 'B', 'L']: 
            return False
        return True

    def find_next_step(self, target_rect):
        """Berekent de volgende stap om obstakels heen (BFS Algoritme)"""
        start_col, start_row = self.get_grid_pos(self.rect.centerx, self.rect.centery)
        end_col, end_row = self.get_grid_pos(target_rect.centerx, target_rect.centery)
        
        if (start_col, start_row) == (end_col, end_row):
            return None # Dichtbij genoeg

        # Breadth-First Search
        queue = deque([(start_col, start_row)])
        came_from = {(start_col, start_row): None}
        found = False
        steps = 0
        
        while queue:
            curr = queue.popleft()
            steps += 1
            if steps > 250: break # Stop als het zoeken te lang duurt (performance)
            
            if curr == (end_col, end_row):
                found = True
                break
            
            cx, cy = curr
            neighbors = [(cx, cy-1), (cx, cy+1), (cx-1, cy), (cx+1, cy)]
            
            for nx, ny in neighbors:
                if (nx, ny) not in came_from and self.is_walkable(nx, ny):
                    came_from[(nx, ny)] = curr
                    queue.append((nx, ny))
        
        if found:
            # Pad terugrekenen van doel naar start
            curr = (end_col, end_row)
            path = []
            while curr != (start_col, start_row):
                path.append(curr)
                curr = came_from[curr]
                if curr is None: return None
            
            # De laatste in de lijst is de EERSTE stap die we moeten zetten
            next_tile = path[-1]
            
            # Zet grid om naar pixel doel (midden van de tegel)
            pixel_x = next_tile[0] * config.TILE_SIZE + config.TILE_SIZE // 2
            pixel_y = next_tile[1] * config.TILE_SIZE + config.TILE_SIZE // 2
            return (pixel_x, pixel_y)
            
        return None

    def update(self, player_rect):
        if self.is_cured:
            return

        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        distance = (dx ** 2 + dy ** 2) ** 0.5

        # --- TRIGGER LOGICA ---
        if self.is_boss:
            # Als speler in zicht is, wordt boss FOREVER triggered
            if distance < self.chase_radius:
                self.triggered = True
        
        move_x = 0
        move_y = 0

        # --- BEWEGING ---
        
        # 1. BOSS PATHFINDING (Slim achtervolgen)
        if self.is_boss and self.triggered:
            self.path_timer -= 1
            
            # Elke 15 frames (0.25s) nieuwe route berekenen
            if self.path_timer <= 0 or self.next_step is None:
                self.path_timer = 15
                self.next_step = self.find_next_step(player_rect)
            
            if self.next_step:
                # Beweeg naar het tussenpunt (om de bank heen)
                tx, ty = self.next_step
                tdx = tx - self.rect.centerx
                tdy = ty - self.rect.centery
                tdist = (tdx**2 + tdy**2)**0.5
                
                if tdist > 0:
                    move_x = (tdx / tdist) * self.speed
                    move_y = (tdy / tdist) * self.speed
            else:
                # Fallback: Direct naar speler (als pad faalt of heel dichtbij)
                if distance > 0:
                    move_x = (dx / distance) * self.speed
                    move_y = (dy / distance) * self.speed

        # 2. STANDAARD ACHTERVOLGING (Domme lijn, alleen als dichtbij)
        elif distance < self.chase_radius:
            if distance > 0:
                move_x = (dx / distance) * self.speed
                move_y = (dy / distance) * self.speed
        
        # 3. IDLE (Ronddwalen)
        else:
            self.move_timer -= 1
            if self.move_timer <= 0:
                self.change_direction()
            move_x = self.direction[0]
            move_y = self.direction[1]

        # Sprite richting
        if move_x > 0: self.facing_right = True
        elif move_x < 0: self.facing_right = False

        # Bewegen met collision check (zodat ze niet door muren vliegen)
        self.rect.x += move_x
        if self.check_collision(): self.rect.x -= move_x
        self.rect.y += move_y
        if self.check_collision(): self.rect.y -= move_y

    def check_collision(self):
        points = [self.rect.topleft, self.rect.topright, self.rect.bottomleft, self.rect.bottomright]
        for point in points:
            col = int(point[0] // config.TILE_SIZE)
            row = int(point[1] // config.TILE_SIZE)
            
            if 0 <= row < len(self.map_data):
                if 0 <= col < len(self.map_data[row]):
                    tile = self.map_data[row][col]
                    if tile == 'W' or tile == 'b' or tile == 'B' or tile == 'L': 
                        return True
            else:
                return True
        return False

    def draw(self, screen, camera_x, camera_y):
        draw_x = self.rect.x - camera_x
        draw_y = self.rect.y - camera_y

        if self.is_cured:
            pygame.draw.circle(screen, config.BUBBLE_COLOR, 
                             (draw_x + self.rect.width//2, draw_y + self.rect.height//2), 
                             self.rect.width//2, 2)
            pygame.draw.circle(screen, (255, 200, 200), 
                             (draw_x + self.rect.width//2, draw_y + self.rect.height//2), 10)
        else:
            # 1. TEKEN DE SPRITE
            if self.is_boss:
                if "boss" in config.ASSETS:
                    screen.blit(config.ASSETS["boss"], (draw_x, draw_y))
                else:
                    pygame.draw.rect(screen, (100, 0, 100), (draw_x, draw_y, self.rect.width, self.rect.height))
            else:
                # Standaard Vijand
                sprite = None
                if self.facing_right:
                    sprite = config.ASSETS.get("enemy_right")
                else:
                    sprite = config.ASSETS.get("enemy_left")
                
                if not sprite: sprite = config.ASSETS.get("enemy")

                if sprite:
                    screen.blit(sprite, (draw_x, draw_y))
                else:
                    pygame.draw.rect(screen, (0, 255, 0), (draw_x, draw_y, self.rect.width, self.rect.height))

            # 2. TEKEN DE HEALTH BAR
            max_hp = config.BOSS_HP if self.is_boss else config.NORMAL_HP
            hp_percent = self.hp / max_hp
            if hp_percent < 0: hp_percent = 0

            bar_width = self.rect.width
            bar_height = 8 
            
            bar_x = draw_x
            bar_y = draw_y - 15

            pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * hp_percent, bar_height))
            pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 1)