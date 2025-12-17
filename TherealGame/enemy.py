import pygame
import random
import config

class Enemy:
    def __init__(self, x, y, map_data, is_boss=False):
        # We gebruiken hier ENEMY_SIZE (125) uit config
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
        
        # Kijkrichting (voor sprites)
        self.facing_right = True 

    def change_direction(self):
        possible_directions = [(self.speed, 0), (-self.speed, 0), (0, self.speed), (0, -self.speed), (0, 0)]
        self.direction = random.choice(possible_directions)
        self.move_timer = random.randint(30, 120)

    def take_damage(self, amount):
        if self.is_cured: return
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False 
            self.is_cured = True 

    def update(self, player_rect):
        if self.is_cured:
            return

        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        distance = (dx ** 2 + dy ** 2) ** 0.5

        move_x = 0
        move_y = 0

        if distance < self.chase_radius:
            if distance != 0:
                dx /= distance
                dy /= distance
            move_x = dx * self.speed
            move_y = dy * self.speed
        else:
            self.move_timer -= 1
            if self.move_timer <= 0:
                self.change_direction()
            move_x = self.direction[0]
            move_y = self.direction[1]

        # Richting updaten voor de sprite
        if move_x > 0:
            self.facing_right = True
        elif move_x < 0:
            self.facing_right = False

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

            # 2. TEKEN DE HEALTH BAR (NIEUW!)
            # We tekenen dit alleen als ze nog niet genezen zijn
            max_hp = config.BOSS_HP if self.is_boss else config.NORMAL_HP
            hp_percent = self.hp / max_hp
            if hp_percent < 0: hp_percent = 0

            bar_width = self.rect.width
            bar_height = 8 # Hoogte van het balkje
            
            # Positie: 15 pixels boven de vijand
            bar_x = draw_x
            bar_y = draw_y - 15

            # Achtergrond (Rood)
            pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            # Voorgrond (Groen)
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * hp_percent, bar_height))
            # Zwart randje eromheen
            pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 1)