import pygame
import random
import config

class Enemy:
    def __init__(self, x, y, map_data):
        self.rect = pygame.Rect(x, y, config.ENEMY_SIZE, config.ENEMY_SIZE)
        self.map_data = map_data
        self.hp = 30
        self.alive = True
        self.chase_radius = 200  # pixels

        
        # Beweging
        self.speed = config.ENEMY_SPEED
        self.direction = (0, 0) # dx, dy
        self.move_timer = 0     # Hoe lang lopen we in deze richting?
        
        # Start meteen met lopen
        self.change_direction()

    def change_direction(self):
        """Kies willekeurig een richting (Links, Rechts, Boven, Onder, Stil)"""
        possible_directions = [
            (self.speed, 0),   # Rechts
            (-self.speed, 0),  # Links
            (0, self.speed),   # Omlaag
            (0, -self.speed),  # Omhoog
            (0, 0)             # Even stilstaan
        ]
        self.direction = random.choice(possible_directions)
        
        # Loop tussen de 30 en 120 frames (0.5 tot 2 seconden) deze kant op
        self.move_timer = random.randint(30, 120)

    def update(self, player_rect):
        if not self.alive:
            return

    # --- Afstand tot speler ---
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        distance = (dx ** 2 + dy ** 2) ** 0.5

    # --- CHASE MODE ---
        if distance < self.chase_radius:
            # Normaliseer richting
            if distance != 0:
                dx /= distance
                dy /= distance

            move_x = dx * self.speed
            move_y = dy * self.speed

    # --- RANDOM MODE ---
        else:
            self.move_timer -= 1
            if self.move_timer <= 0:
                self.change_direction()

            move_x = self.direction[0]
            move_y = self.direction[1]

    # --- Beweging + collision ---
        self.rect.x += move_x
        if self.check_collision():
            self.rect.x -= move_x

        self.rect.y += move_y
        if self.check_collision():
            self.rect.y -= move_y


    def check_collision(self):
        """Check of enemy tegen muur loopt"""
        points = [self.rect.topleft, self.rect.topright, self.rect.bottomleft, self.rect.bottomright]
        
        for point in points:
            col = int(point[0] // config.TILE_SIZE)
            row = int(point[1] // config.TILE_SIZE)
            
            if 0 <= row < len(self.map_data):
                row_len = len(self.map_data[row])
                if 0 <= col < row_len:
                    if self.map_data[row][col] == 'W': # W is muur
                        return True
        return False

    def draw(self, screen, camera_x, camera_y):
        if not self.alive:
            return

        draw_x = self.rect.x - camera_x
        draw_y = self.rect.y - camera_y
        
        if "enemy" in config.ASSETS:
            screen.blit(config.ASSETS["enemy"], (draw_x, draw_y))
        else:
            # Fallback: Groen blokje
            pygame.draw.rect(screen, (0, 255, 0), (draw_x, draw_y, config.ENEMY_SIZE, config.ENEMY_SIZE))