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

# MOEILIJKHEIDSGRADEN
DIFFICULTY_SETTINGS = {
    "EASY": {
        "spawn_rate": 450,
        "darkness": False,
        "color": (0, 255, 0)
    },
    "NORMAL": {
        "spawn_rate": 300,
        "darkness": False,
        "color": (255, 255, 0)
    },
    "HARD": {
        "spawn_rate": 120,
        "darkness": True, 
        "color": (255, 0, 0)
    }
}

# SPELER & XP
PLAYER_SPEED = 4
PLAYER_SIZE = 60         
PLAYER_VISUAL_SIZE = 125 
PLAYER_HP_MAX = 100

XP_PER_ZOMBIE = 10      
BASE_ATTACK_DAMAGE = 15 
DAMAGE_PER_XP = 0.5     

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
# AANGEPAST: Bellen zijn groter dan kogels!
BULLET_SIZE = 32 

# ITEMS
ITEM_SIZE = 40          
ITEM_VISUAL_SIZE = 64   
HEALTH_REGEN = 30
AMMO_PACK_AMOUNT = 10
SHOTGUN_AMMO_AMOUNT = 5

# VIJAND
ENEMY_SPEED = 2
ENEMY_SIZE = 64
BOSS_SIZE = 128
BOSS_HP = 500
NORMAL_HP = 30
ZOMBIE_SPAWN_RATE = 300 

# =========================
# COLORS
# =========================
GREEN = (0, 180, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PLAYER_COLOR = (255, 0, 0)
GOLD = (255, 215, 0) 
BUBBLE_COLOR = (0, 200, 255) 
BUTTON_COLOR = (50, 50, 50)       
HIGHLIGHT_COLOR = (255, 215, 0)   
TEXT_COLOR = (255, 255, 255)

# POKEMON BATTLE COLORS
BATTLE_BG = (240, 240, 240)
BATTLE_BOX = (40, 50, 60)
BATTLE_TEXT = (255, 255, 255)
HP_BAR_BG = (100, 100, 100)
HP_BAR_GOOD = (20, 200, 50)
HP_BAR_LOW = (200, 150, 20)
HP_BAR_CRIT = (200, 20, 20)

# =========================
# PATHS
# =========================
BASE_PATH = os.path.dirname(__file__)
IMAGE_PATH = os.path.join(BASE_PATH, "images")
SOUND_PATH = os.path.join(BASE_PATH, "sounds")
SAVE_FILE = os.path.join(BASE_PATH, "savegame.json")
MUSIC_FILE = os.path.join(SOUND_PATH, "music.mp3")

if os.path.exists(os.path.join(IMAGE_PATH, "Poster_loadingScreen.png")):
    MENU_BACKGROUND = os.path.join(IMAGE_PATH, "Poster_loadingScreen.png")
else:
    MENU_BACKGROUND = os.path.join(IMAGE_PATH, "Poster_loadingScreen.jpg")

# =========================
# ASSETS LADEN
# =========================
ASSETS = {}

def load_assets():
    print("--- ASSETS LADEN ---")
    
    def load_smart(filename_base, w, h, color):
        full_path = os.path.join(IMAGE_PATH, filename_base + ".png")
        if not os.path.exists(full_path):
            full_path = os.path.join(IMAGE_PATH, filename_base + ".jpg")
        
        if os.path.exists(full_path):
            try:
                img = pygame.image.load(full_path).convert_alpha()
                return pygame.transform.scale(img, (w, h))
            except Exception as e:
                print(f"[FOUT] Fout bij laden {full_path}: {e}")
        else:
            if "walking" not in filename_base: 
                print(f"[LET OP] Plaatje niet gevonden: {filename_base}")
        
        s = pygame.Surface((w, h))
        s.fill(color)
        pygame.draw.rect(s, (0,0,0), (0,0,w,h), 2)
        return s

    # SPELER
    ASSETS["player_sprites"] = {}
    p_down = load_smart("player_down", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, PLAYER_COLOR)
    ASSETS["player_sprites"]["down"] = p_down
    
    if os.path.exists(os.path.join(IMAGE_PATH, "player_up.png")):
        ASSETS["player_sprites"]["up"] = load_smart("player_up", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, PLAYER_COLOR)
    else:
        ASSETS["player_sprites"]["up"] = p_down

    p_left = load_smart("player_left", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, PLAYER_COLOR)
    ASSETS["player_sprites"]["left"] = p_left
    ASSETS["player_sprites"]["right"] = pygame.transform.flip(p_left, True, False)

    # WALKING
    p_walk_right = load_smart("player_walking", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, PLAYER_COLOR)
    ASSETS["player_sprites"]["walk_right"] = p_walk_right
    ASSETS["player_sprites"]["walk_left"] = pygame.transform.flip(p_walk_right, True, False)
    
    if os.path.exists(os.path.join(IMAGE_PATH, "player_walking_up.png")):
         ASSETS["player_sprites"]["walk_up"] = load_smart("player_walking_up", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, PLAYER_COLOR)
    else:
         ASSETS["player_sprites"]["walk_up"] = ASSETS["player_sprites"]["up"]

    if os.path.exists(os.path.join(IMAGE_PATH, "player_walking_down.png")):
         ASSETS["player_sprites"]["walk_down"] = load_smart("player_walking_down", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, PLAYER_COLOR)
    else:
         ASSETS["player_sprites"]["walk_down"] = ASSETS["player_sprites"]["down"]

    ASSETS["player_sprites"]["walk_up_l"] = load_smart("player_walking_up_leftfoot", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, PLAYER_COLOR)
    ASSETS["player_sprites"]["walk_up_r"] = load_smart("player_walking_up_rightfoot", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, PLAYER_COLOR)
    ASSETS["player_sprites"]["walk_down_l"] = load_smart("player_walking_down_leftfoot", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, PLAYER_COLOR)
    ASSETS["player_sprites"]["walk_down_r"] = load_smart("player_walking_down_rightfoot", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, PLAYER_COLOR)

    # NPC & ENEMY
    monster_right = load_smart("monster", 125, 125, GREEN) 
    ASSETS["enemy_right"] = monster_right
    ASSETS["enemy_left"] = pygame.transform.flip(monster_right, True, False)
    ASSETS["enemy"] = monster_right 

    ASSETS["boss"] = load_smart("boss", 250, 250, (100, 0, 100))
    ASSETS["teacher"] = load_smart("teacher", TILE_SIZE *2, TILE_SIZE *2, WHITE)
    
    if os.path.exists(os.path.join(IMAGE_PATH, "player_up.png")):
        ASSETS["player_back"] = load_smart("player_up", 200, 200, PLAYER_COLOR)
    else:
        ASSETS["player_back"] = load_smart("player_down", 200, 200, PLAYER_COLOR)

    ASSETS["player_monster"] = load_smart("player_monster", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, (50, 0, 0))

    # PROJECTILE (De Bubbel!) [NIEUW]
    # We laden bubble.png als de projectile sprite
    ASSETS["projectile"] = load_smart("bubble", BULLET_SIZE, BULLET_SIZE, (0, 255, 255))

    # OMGEVING
    ASSETS["wall"] = load_smart("wall", TILE_SIZE, WALL_HEIGHT, (100, 100, 100))
    ASSETS["floor"] = load_smart("floor", TILE_SIZE, TILE_SIZE, (50, 50, 50))
    ASSETS["door"] = load_smart("door", TILE_SIZE, TILE_SIZE, (0, 0, 150))
    ASSETS["locked_door"] = load_smart("locked_door", TILE_SIZE, TILE_SIZE, (150, 0, 0))
    ASSETS["stairs"] = load_smart("stairs", TILE_SIZE, TILE_SIZE, (200, 200, 0))
    ASSETS["student_bench"] = load_smart("bench", TILE_SIZE, TILE_SIZE, (139, 69, 19))

    # ITEMS
    ASSETS["item_health"] = load_smart("item_health", ITEM_VISUAL_SIZE, ITEM_VISUAL_SIZE, GREEN)
    ASSETS["item_ammo"] = load_smart("item_ammo", ITEM_VISUAL_SIZE, ITEM_VISUAL_SIZE, (255, 255, 0))
    ASSETS["item_shotgun"] = load_smart("item_shotgun", ITEM_VISUAL_SIZE, ITEM_VISUAL_SIZE, (255, 0, 0))
    ASSETS["item_key"] = load_smart("item_key", ITEM_VISUAL_SIZE, ITEM_VISUAL_SIZE, GOLD)

    print("[KLAAR] Assets geladen!")

def create_screen():
    if FULLSCREEN: return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else: return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))