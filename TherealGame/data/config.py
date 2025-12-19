import os
import pygame

# =========================
# SCHERM INSTELLINGEN
# =========================
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FULLSCREEN = False

# =========================
# GAME SETTINGS
# =========================
TILE_SIZE = 64
WALL_HEIGHT = 128 

# KEYWORD: DIFFICULTY SETTINGS
# [NL] Hier configureren we de moeilijkheidsgraden in een dictionary.
# [NL] Elke graad heeft zijn eigen instellingen voor spawn_rate (hoe vaak zombies komen) en duisternis.
# [NL] Door dit hier centraal op te slaan, kunnen we het makkelijk aanpassen zonder de game code te veranderen.
DIFFICULTY_SETTINGS = {
    "EASY": {"spawn_rate": 450, "darkness": False, "color": (0, 255, 0)},
    "NORMAL": {"spawn_rate": 300, "darkness": False, "color": (255, 255, 0)},
    "HARD": {"spawn_rate": 120, "darkness": True, "color": (255, 0, 0)}
}

# SPELER
PLAYER_SPEED = 4
PLAYER_SIZE = 60         
PLAYER_VISUAL_SIZE = 125 
PLAYER_HP_MAX = 100
XP_PER_ZOMBIE = 10      

# WAPENS
WEAPONS = {
    "pistol": {"damage": 10, "speed": 12, "cooldown": 20, "color": (255, 255, 0), "start_ammo": 100, "name": "PISTOL"},
    "shotgun": {"damage": 100, "speed": 15, "cooldown": 60, "color": (255, 0, 0), "start_ammo": 15, "name": "SHOTGUN"}
}
BULLET_SIZE = 32 

# --- DEFINITIES VOOR DE GEREDDE STUDENT ---
STUDENT_ICON_SIZE = 126
BUBBLE_LARGE_SIZE = 489 

# ITEMS
ITEM_SIZE = 40          
ITEM_VISUAL_SIZE = 64   
HEALTH_REGEN = 30
AMMO_PACK_AMOUNT = 10
SHOTGUN_AMMO_AMOUNT = 15

# VIJAND
ENEMY_SPEED = 2
ENEMY_SIZE = 125
BOSS_SIZE = 128
BOSS_HP = 500
NORMAL_HP = 30
ZOMBIE_SPAWN_RATE = 300 

DIRECTOR_SIZE = 128 

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

# =========================
# PATHS
# =========================
# KEYWORD: FILE PATHS
# [NL] We bouwen hier de paden naar de bestanden op een slimme manier.
# [NL] os.path.join zorgt ervoor dat het werkt op zowel Windows (met backslash \) als Mac (met slash /).
# [NL] We starten vanaf de map waar dit bestand staat en gaan zo naar de assets map.
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CURRENT_DIR) 

ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
IMAGE_PATH = os.path.join(ASSETS_DIR, "images")
SOUND_PATH = os.path.join(ASSETS_DIR, "sounds")

SAVE_FILE = os.path.join(ROOT_DIR, "savegame.json")
MUSIC_FILE = os.path.join(SOUND_PATH, "music.mp3")
MENU_BACKGROUND = os.path.join(IMAGE_PATH, "Poster_loadingScreen.png")

# =========================
# ASSETS LADEN
# =========================
ASSETS = {}

def create_screen():
    if FULLSCREEN: return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else: return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def load_assets():
    print("--- ASSETS LADEN ---")
    
    # KEYWORD: SMART LOADING
    # [NL] Dit is een robuuste laad-functie.
    # [NL] Eerst probeert hij het plaatje te laden als .png of .jpg.
    # [NL] Als het bestand NIET gevonden wordt, crasht het spel niet.
    # [NL] In plaats daarvan tekent hij een gekleurd vierkantje (placeholder) zodat je toch kunt testen.
    def load_smart(filename_base, w, h, color):
        full_path = os.path.join(IMAGE_PATH, filename_base + ".png")
        if not os.path.exists(full_path):
            full_path = os.path.join(IMAGE_PATH, filename_base + ".jpg")
        
        if os.path.exists(full_path):
            try:
                img = pygame.image.load(full_path).convert_alpha()
                return pygame.transform.scale(img, (w, h))
            except:
                pass
        
        s = pygame.Surface((w, h))
        s.fill(color)
        pygame.draw.rect(s, (0,0,0), (0,0,w,h), 2)
        return s

    ASSETS["player_sprites"] = {}
    
    # Player directions
    ASSETS["player_sprites"]["down"] = load_smart("player_down", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, PLAYER_COLOR)
    ASSETS["player_sprites"]["up"] = load_smart("player_up", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, PLAYER_COLOR)
    
    p_left = load_smart("player_left", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, PLAYER_COLOR)
    ASSETS["player_sprites"]["left"] = p_left
    ASSETS["player_sprites"]["right"] = pygame.transform.flip(p_left, True, False)

    # Player walking
    ASSETS["player_sprites"]["walk_up"] = load_smart("player_walking_up", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, PLAYER_COLOR)
    ASSETS["player_sprites"]["walk_down"] = load_smart("player_walking_down", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, PLAYER_COLOR)
    
    p_walk_right = load_smart("player_walking", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, PLAYER_COLOR)
    ASSETS["player_sprites"]["walk_right"] = p_walk_right
    ASSETS["player_sprites"]["walk_left"] = pygame.transform.flip(p_walk_right, True, False)

    # Player footsteps
    ASSETS["player_sprites"]["walk_up_l"] = load_smart("player_walking_up_leftfoot", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, PLAYER_COLOR)
    ASSETS["player_sprites"]["walk_up_r"] = load_smart("player_walking_up_rightfoot", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, PLAYER_COLOR)
    ASSETS["player_sprites"]["walk_down_l"] = load_smart("player_walking_down_leftfoot", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, PLAYER_COLOR)
    ASSETS["player_sprites"]["walk_down_r"] = load_smart("player_walking_down_rightfoot", PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE, PLAYER_COLOR)

    # Enemies & NPCs
    monster = load_smart("monster", 125, 125, GREEN)
    ASSETS["enemy_right"] = monster
    ASSETS["enemy_left"] = pygame.transform.flip(monster, True, False)
    ASSETS["enemy"] = monster 

    ASSETS["enemy"] = monster 

    ASSETS["boss"] = load_smart("boss", 250, 250, (100, 0, 100))
    # VOEG DEZE REGEL TOE: Laad de speciale director boss sprite
    ASSETS["director_boss"] = load_smart("director_boss", 250, 250, (50, 0, 50))
    
    # --- NIEUW: APARTE SPRITES VOOR LERAAR EN DIRECTEUR ---
    ASSETS["teacher"] = load_smart("teacher", TILE_SIZE *2, TILE_SIZE *2, WHITE)
    # Zorg dat je director.png hebt, anders krijg je een zwart blokje
    ASSETS["director"] = load_smart("director", TILE_SIZE *2, TILE_SIZE *2, (0, 0, 0))
    ASSETS["director"] = load_smart("director", DIRECTOR_SIZE, DIRECTOR_SIZE, (0, 0, 0))

    # Bubbels
    ASSETS["projectile"] = load_smart("bubble", BULLET_SIZE, BULLET_SIZE, (0, 255, 255))
    ASSETS["bubble_large"] = load_smart("bubble", BUBBLE_LARGE_SIZE, BUBBLE_LARGE_SIZE, (0, 200, 255))
    ASSETS["student_icon"] = load_smart("student_icon", STUDENT_ICON_SIZE, STUDENT_ICON_SIZE, (0, 0, 255))

    # Environment
    ASSETS["wall"] = load_smart("wall", TILE_SIZE, WALL_HEIGHT, (100, 100, 100))
    ASSETS["floor"] = load_smart("floor", TILE_SIZE, TILE_SIZE, (50, 50, 50))
    ASSETS["door"] = load_smart("door", TILE_SIZE, TILE_SIZE, (0, 0, 150))
    ASSETS["locked_door"] = load_smart("locked_door", TILE_SIZE, TILE_SIZE, (150, 0, 0))
    ASSETS["stairs"] = load_smart("stairs", TILE_SIZE, TILE_SIZE, (200, 200, 0))
    ASSETS["student_bench"] = load_smart("bench", TILE_SIZE, TILE_SIZE, (139, 69, 19))

    # Items
    ASSETS["item_health"] = load_smart("item_health", ITEM_VISUAL_SIZE, ITEM_VISUAL_SIZE, GREEN)
    ASSETS["item_ammo"] = load_smart("item_ammo", ITEM_VISUAL_SIZE, ITEM_VISUAL_SIZE, (255, 255, 0))
    ASSETS["item_shotgun"] = load_smart("item_shotgun", ITEM_VISUAL_SIZE, ITEM_VISUAL_SIZE, (255, 0, 0))
    ASSETS["item_key"] = load_smart("item_key", ITEM_VISUAL_SIZE, ITEM_VISUAL_SIZE, GOLD)

    print("[KLAAR] Assets geladen!")