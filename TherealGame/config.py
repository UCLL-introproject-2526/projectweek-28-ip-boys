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
WALL_HEIGHT = 128 

# SPELER
PLAYER_SPEED = 4
PLAYER_SIZE = 64        # Hitbox (zoals gevraagd)
PLAYER_VISUAL_SIZE = 125 # Visuele grootte (zoals gevraagd)
PLAYER_HP_MAX = 100

# WAPENS & MUNITIE
WEAPONS = {
    "pistol": {
        "damage": 10,
        "speed": 12,
        "cooldown": 20,
        "color": (255, 255, 0), 
        "start_ammo": 20,
        "name": "Pistool"
    },
    "shotgun": {
        "damage": 100, 
        "speed": 15,
        "cooldown": 60, 
        "color": (255, 0, 0), 
        "start_ammo": 0, 
        "name": "SHOTGUN"
    }
}
BULLET_SIZE = 8

# ITEMS
ITEM_SIZE = 40
HEALTH_REGEN = 30
AMMO_PACK_AMOUNT = 10
SHOTGUN_AMMO_AMOUNT = 5

# VIJAND
ENEMY_SPEED = 2
ENEMY_SIZE = 64
BOSS_SIZE = 128
BOSS_HP = 100
NORMAL_HP = 30
ZOMBIE_SPAWN_RATE = 300 

# =========================
# COLORS (Fallback)
# =========================
GREEN = (0, 180, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PLAYER_COLOR = (255, 0, 0)
GOLD = (255, 215, 0) 
BUBBLE_COLOR = (0, 200, 255) 

# =========================
# PATHS
# =========================
BASE_PATH = os.path.dirname(__file__)
IMAGE_PATH = os.path.join(BASE_PATH, "images")

if os.path.exists(os.path.join(IMAGE_PATH, "Poster_loadingScreen.png")):
    MENU_BACKGROUND = os.path.join(IMAGE_PATH, "Poster_loadingScreen.png")
else:
    MENU_BACKGROUND = os.path.join(IMAGE_PATH, "Poster_loadingScreen.jpg")

# =========================
# ASSETS LADEN
# =========================
ASSETS = {}

def load_assets():
    print("--- ASSETS LADEN (TEXT MODE) ---")
    
    def load_smart(filename_base, w, h, color):
        # 1. Probeer PNG
        full_path = os.path.join(IMAGE_PATH, filename_base + ".png")
        if not os.path.exists(full_path):
            # 2. Probeer JPG
            full_path = os.path.join(IMAGE_PATH, filename_base + ".jpg")
        
        if os.path.exists(full_path):
            try:
                img = pygame.image.load(full_path).convert_alpha()
                return pygame.transform.scale(img, (w, h))
            except Exception as e:
                print(f"[FOUT] Fout bij laden {full_path}: {e}")
        else:
            # Alleen printen als het geen optionele animatie is
            if "walking" not in filename_base: 
                print(f"[LET OP] Plaatje niet gevonden: {filename_base}")
        
        # 3. Fallback
        s = pygame.Surface((w, h))
        s.fill(color)
        pygame.draw.rect(s, (0,0,0), (0,0,w,h), 2)
        return s

    # --- 1. SPELER SPRITES ---
    ASSETS["player_sprites"] = {}
    
    # BASIS (STILSTAAN)
    p_down = load_smart("player_down", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, PLAYER_COLOR)
    ASSETS["player_sprites"]["down"] = p_down
    
    if os.path.exists(os.path.join(IMAGE_PATH, "player_up.png")):
        ASSETS["player_sprites"]["up"] = load_smart("player_up", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, PLAYER_COLOR)
    else:
        ASSETS["player_sprites"]["up"] = p_down

    p_left = load_smart("player_left", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, PLAYER_COLOR)
    ASSETS["player_sprites"]["left"] = p_left
    ASSETS["player_sprites"]["right"] = pygame.transform.flip(p_left, True, False)

    # WALKING ANIMATIES (LINKS / RECHTS)
    p_walk_right = load_smart("player_walking", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, PLAYER_COLOR)
    p_walk_left = pygame.transform.flip(p_walk_right, True, False)
    
    ASSETS["player_sprites"]["walk_right"] = p_walk_right
    ASSETS["player_sprites"]["walk_left"] = p_walk_left
    
    # WALKING ANIMATIES (BOVEN / ONDER)
    # Check of player_walking_up.png bestaat
    if os.path.exists(os.path.join(IMAGE_PATH, "player_walking_up.png")):
         ASSETS["player_sprites"]["walk_up"] = load_smart("player_walking_up", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, PLAYER_COLOR)
    else:
         # Fallback: gebruik gewone 'up' sprite
         ASSETS["player_sprites"]["walk_up"] = ASSETS["player_sprites"]["up"]

    # Check of player_walking_down.png bestaat
    if os.path.exists(os.path.join(IMAGE_PATH, "player_walking_down.png")):
         ASSETS["player_sprites"]["walk_down"] = load_smart("player_walking_down", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, PLAYER_COLOR)
    else:
         # Fallback: gebruik gewone 'down' sprite
         ASSETS["player_sprites"]["walk_down"] = ASSETS["player_sprites"]["down"]

    # --- 2. VIJANDEN & NPC ---
    ASSETS["enemy"] = load_smart("zombie", ENEMY_SIZE, ENEMY_SIZE, GREEN)
    ASSETS["boss"] = load_smart("boss", BOSS_SIZE, BOSS_SIZE, (100, 0, 100))
    ASSETS["teacher"] = load_smart("teacher", TILE_SIZE, TILE_SIZE, WHITE)
    ASSETS["player_monster"] = load_smart("player_monster", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, (50, 0, 0))

    # --- 3. OMGEVING ---
    ASSETS["wall"] = load_smart("wall", TILE_SIZE, WALL_HEIGHT, (100, 100, 100))
    ASSETS["floor"] = load_smart("floor", TILE_SIZE, TILE_SIZE, (50, 50, 50))
    ASSETS["door"] = load_smart("door", TILE_SIZE, TILE_SIZE, (0, 0, 150))
    ASSETS["locked_door"] = load_smart("locked_door", TILE_SIZE, TILE_SIZE, (150, 0, 0))
    ASSETS["stairs"] = load_smart("stairs", TILE_SIZE, TILE_SIZE, (200, 200, 0))
    ASSETS["student_bench"] = load_smart("bench", TILE_SIZE, TILE_SIZE, (139, 69, 19))

    # --- 4. ITEMS ---
    ASSETS["item_health"] = load_smart("item_health", ITEM_SIZE, ITEM_SIZE, GREEN)
    ASSETS["item_ammo"] = load_smart("item_ammo", ITEM_SIZE, ITEM_SIZE, (255, 255, 0))
    ASSETS["item_shotgun"] = load_smart("item_shotgun", ITEM_SIZE, ITEM_SIZE, (255, 0, 0))
    ASSETS["item_key"] = load_smart("item_key", ITEM_SIZE, ITEM_SIZE, GOLD)

    print("[KLAAR] Assets geladen!")

def create_screen():
    if FULLSCREEN: return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else: return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))