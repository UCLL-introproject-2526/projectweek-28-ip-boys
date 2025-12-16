import pygame
import config
FLOOR_COLOR_1 = (60, 60, 60)
FLOOR_COLOR_2 = (50, 50, 50)
TILE_SIZE = 100

class Game:
    def __init__(self, screen):
        self.screen = screen
        
        # Maak de speler (een rode vierkant voor nu)
        # De speler begint in het midden van de GROTE MAP
        self.player_rect = pygame.Rect(
            config.MAP_WIDTH // 2, 
            config.MAP_HEIGHT // 2, 
            config.PLAYER_SIZE, 
            config.PLAYER_SIZE
        )

    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Beweeg de speler in de wereld (x en y)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_rect.x -= config.PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_rect.x += config.PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player_rect.y -= config.PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player_rect.y += config.PLAYER_SPEED

        # Zorg dat speler niet van de map af valt (Clamping)
        self.player_rect.left = max(0, self.player_rect.left)
        self.player_rect.right = min(config.MAP_WIDTH, self.player_rect.right)
        self.player_rect.top = max(0, self.player_rect.top)
        self.player_rect.bottom = min(config.MAP_HEIGHT, self.player_rect.bottom)

    def draw(self):
        self.screen.fill(config.BLACK) # Schoonmaken

        # --- CAMERA BEREKENING ---
        # We willen dat de speler in het midden van het SCHERM staat.
        # Camera Offset = Speler Positie - Halve Scherm Grootte
        camera_x = self.player_rect.centerx - (config.SCREEN_WIDTH // 2)
        camera_y = self.player_rect.centery - (config.SCREEN_HEIGHT // 2)

        # Optioneel: Zorg dat de camera niet buiten de zwarte randen van de map kijkt
        camera_x = max(0, min(camera_x, config.MAP_WIDTH - config.SCREEN_WIDTH))
        camera_y = max(0, min(camera_y, config.MAP_HEIGHT - config.SCREEN_HEIGHT))

        # --- TEKENEN VAN DE WERELD ---
        # We tekenen alles op: (Wereld Positie - Camera Positie)
        
        # 1. Teken een grid (zodat je ziet dat je beweegt)
        grid_size = 100
        for x in range(0, config.MAP_WIDTH, grid_size):
            pygame.draw.line(self.screen, (50, 50, 50), (x - camera_x, 0 - camera_y), (x - camera_x, config.MAP_HEIGHT - camera_y))
        
        for y in range(0, config.MAP_HEIGHT, grid_size):
            pygame.draw.line(self.screen, (50, 50, 50), (0 - camera_x, y - camera_y), (config.MAP_WIDTH - camera_x, y - camera_y))

        # 2. Teken de rand van de wereld (Witte lijn)
        border_rect = pygame.Rect(0 - camera_x, 0 - camera_y, config.MAP_WIDTH, config.MAP_HEIGHT)
        pygame.draw.rect(self.screen, (255, 255, 255), border_rect, 2)

        # 3. Teken de speler
        # De speler wordt getekend op zijn positie MINUS de camera
        draw_rect = pygame.Rect(
            self.player_rect.x - camera_x,
            self.player_rect.y - camera_y,
            self.player_rect.width,
            self.player_rect.height
        )
        pygame.draw.rect(self.screen, config.PLAYER_COLOR, draw_rect)

        pygame.display.flip()

        import pygame
import config

class Game:
    def __init__(self, screen):
        self.screen = screen

        # 🌍 Wereld
        self.MAP_WIDTH = 2000
        self.MAP_HEIGHT = 2000

        # 🔴 Speler
        self.player_rect = pygame.Rect(
            1000, 1000, config.PLAYER_SIZE, config.PLAYER_SIZE
        )

        wall_thickness = 20  # dikke schoolmuur

        # ✅ DIT MOET HIER STAAN
        self.walls = [
            # BOVEN
            pygame.Rect(0, 0, self.MAP_WIDTH, wall_thickness),

            # ONDER
            pygame.Rect(
                0,
                self.MAP_HEIGHT - wall_thickness,
                self.MAP_WIDTH,
                wall_thickness
            ),

            # LINKS
            pygame.Rect(0, 0, wall_thickness, self.MAP_HEIGHT),

            # RECHTS
            pygame.Rect(
                self.MAP_WIDTH - wall_thickness,
                0,
                wall_thickness,
                self.MAP_HEIGHT
            ),
        ]

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = dy = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= config.PLAYER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += config.PLAYER_SPEED
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= config.PLAYER_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += config.PLAYER_SPEED

        self.move_and_collide(dx, dy)

    def move_and_collide(self, dx, dy):
        # X-as
        self.player_rect.x += dx
        for wall in self.walls:
            if self.player_rect.colliderect(wall):
                if dx > 0:
                    self.player_rect.right = wall.left
                elif dx < 0:
                    self.player_rect.left = wall.right

        # Y-as
        self.player_rect.y += dy
        for wall in self.walls:
            if self.player_rect.colliderect(wall):
                if dy > 0:
                    self.player_rect.bottom = wall.top
                elif dy < 0:
                    self.player_rect.top = wall.bottom

    def draw(self):
        # 🎥 Camera
        camera_x = self.player_rect.centerx - config.SCREEN_WIDTH // 2
        camera_y = self.player_rect.centery - config.SCREEN_HEIGHT // 2

        camera_x = max(0, min(camera_x, self.MAP_WIDTH - config.SCREEN_WIDTH))
        camera_y = max(0, min(camera_y, self.MAP_HEIGHT - config.SCREEN_HEIGHT))

        # achtergrond
        self.screen.fill((0, 0, 0))

        # grid
        grid = 100
        for x in range(0, self.MAP_WIDTH, grid):
            pygame.draw.line(
                self.screen, (40, 40, 40),
                (x - camera_x, 0 - camera_y),
                (x - camera_x, self.MAP_HEIGHT - camera_y)
            )
        for y in range(0, self.MAP_HEIGHT, grid):
            pygame.draw.line(
                self.screen, (40, 40, 40),
                (0 - camera_x, y - camera_y),
                (self.MAP_WIDTH - camera_x, y - camera_y)
            )

        # muren tekenen
        for wall in self.walls:
            draw_wall = pygame.Rect(
                wall.x - camera_x,
                wall.y - camera_y,
                wall.width,
                wall.height
            )
            pygame.draw.rect(self.screen, (220, 220, 220), draw_wall)

        # speler
        draw_player = pygame.Rect(
            self.player_rect.x - camera_x,
            self.player_rect.y - camera_y,
            self.player_rect.width,
            self.player_rect.height
        )
        pygame.draw.rect(self.screen, config.PLAYER_COLOR, draw_player)

        pygame.display.flip()
