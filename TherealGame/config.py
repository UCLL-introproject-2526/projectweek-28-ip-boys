import os
import pygame

# =========================
# SCREEN CONFIG
# =========================
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FULLSCREEN = False

# =========================
# GAME SETTINGS
# =========================
TILE_SIZE = 64  

# SPELER
PLAYER_SPEED = 4 
PLAYER_SIZE = 40         # Hitbox
PLAYER_VISUAL_SIZE = 125 # Plaatje

# VIJAND (NIEUW)
ENEMY_SPEED = 2          # Langzamer dan speler
ENEMY_SIZE = 64          # Even groot als een tegel

# =========================
# COLORS
# =========================
GREEN = (0, 180, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PLAYER_COLOR = (255, 0, 0)

# =========================
# PATHS
# =========================
BASE_PATH = os.path.dirname(__file__)
IMAGE_PATH = os.path.join(BASE_PATH, "images")
MENU_BACKGROUND = os.path.join(IMAGE_PATH, "Poster_loadingScreen.png")

# =========================
# ASSETS LADEN
# =========================
ASSETS = {}

def load_assets():
    try:
        def load_tile(filename):
            path = os.path.join(IMAGE_PATH, filename)
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        
        def load_player_sprite(filename):
            path = os.path.join(IMAGE_PATH, filename)
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, (PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE))

        # NIEUW: Helper voor enemy
        def load_enemy_sprite(filename):
            path = os.path.join(IMAGE_PATH, filename)
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, (ENEMY_SIZE, ENEMY_SIZE))

        # --- OMGEVING ---
        if os.path.exists(os.path.join(IMAGE_PATH, "wall.png")): ASSETS["wall"] = load_tile("wall.png")
        if os.path.exists(os.path.join(IMAGE_PATH, "floor.png")): ASSETS["floor"] = load_tile("floor.png")
        if os.path.exists(os.path.join(IMAGE_PATH, "door.png")): ASSETS["door"] = load_tile("door.png")
        if os.path.exists(os.path.join(IMAGE_PATH, "stairs.png")): ASSETS["stairs"] = load_tile("stairs.png")

        # --- SPELER ---
        ASSETS["player_sprites"] = {}
        # Zorg dat deze bestanden bestaan!
        if os.path.exists(os.path.join(IMAGE_PATH, "player_down.png")):
            ASSETS["player_sprites"]["down"] = load_player_sprite("player_down.png")
        if os.path.exists(os.path.join(IMAGE_PATH, "player_up.png")):
            ASSETS["player_sprites"]["up"] = load_player_sprite("player_up.png")
        if os.path.exists(os.path.join(IMAGE_PATH, "player_left.png")):
            img_left = load_player_sprite("player_left.png")
            ASSETS["player_sprites"]["left"] = img_left
            ASSETS["player_sprites"]["right"] = pygame.transform.flip(img_left, True, False)
        
        # --- VIJAND (NIEUW) ---
        if os.path.exists(os.path.join(IMAGE_PATH, "player_down.png")):
            ASSETS["enemy"] = load_enemy_sprite("player_down.png")

        print("Assets geladen!")

    except Exception as e:
        print(f"FOUT BIJ ASSETS: {e}")

def create_screen():
    if FULLSCREEN:
        return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))