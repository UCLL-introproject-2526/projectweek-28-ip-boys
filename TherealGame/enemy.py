import pygame
import random
import config

class Enemy:
    def __init__(self, x, y, map_data, is_boss=False):
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
                    # Update: Vijanden botsen tegen Muren (W), Bankjes (b en B) en Gesloten Deuren (L)
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
            asset_key = "boss" if self.is_boss else "enemy"
            if asset_key in config.ASSETS:
                screen.blit(config.ASSETS[asset_key], (draw_x, draw_y))
            else:
                color = (100, 0, 100) if self.is_boss else (0, 255, 0)
                pygame.draw.rect(screen, color, (draw_x, draw_y, self.rect.width, self.rect.height))