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

# =========================
# COLORS (Nog steeds nodig voor de achtergrond)
# =========================
GREEN = (0, 180, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PLAYER_COLOR = (255, 0, 0) # Fallback als plaatje niet werkt

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
    """
    Laadt tegels EN de 4 richtingen van de speler.
    """
    try:
        # Helper functie voor tegels (64x64)
        def load_tile(filename):
            path = os.path.join(IMAGE_PATH, filename)
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        
        # Helper functie voor speler sprites (40x40)
        def load_player_sprite(filename):
            path = os.path.join(IMAGE_PATH, filename)
            img = pygame.image.load(path).convert_alpha()
            # HIER GEBRUIKEN WE NU DE VISUAL SIZE
            return pygame.transform.scale(img, (PLAYER_VISUAL_SIZE, PLAYER_VISUAL_SIZE))

        # --- LAAD DE OMGEVING ---
        # Zorg dat deze bestanden bestaan als je ze wilt zien, anders zie je gekleurde blokjes
        if os.path.exists(os.path.join(IMAGE_PATH, "wall.png")): ASSETS["wall"] = load_tile("wall.png")
        if os.path.exists(os.path.join(IMAGE_PATH, "floor.png")): ASSETS["floor"] = load_tile("floor.png")
        if os.path.exists(os.path.join(IMAGE_PATH, "door.png")): ASSETS["door"] = load_tile("door.png")
        if os.path.exists(os.path.join(IMAGE_PATH, "stairs.png")): ASSETS["stairs"] = load_tile("stairs.png")

        # --- LAAD DE SPELER SPRITES (NIEUW!) ---
        # We maken een nieuw woordenboekje binnen ASSETS
        ASSETS["player_sprites"] = {}

        # Laad Omlaag, Omhoog en Links
        img_down = load_player_sprite("player_down.png")
        img_up = load_player_sprite("player_up.png")
        img_left = load_player_sprite("player_left.png")

        # Maak Rechts door Links te spiegelen (flip horizontaal=True, verticaal=False)
        img_right = pygame.transform.flip(img_left, True, False)

        # Stop ze in het woordenboek
        ASSETS["player_sprites"]["down"] = img_down
        ASSETS["player_sprites"]["up"] = img_up
        ASSETS["player_sprites"]["left"] = img_left
        ASSETS["player_sprites"]["right"] = img_right
        
        print("Assets en speler sprites succesvol geladen!")

    except Exception as e:
        print(f"FOUT BIJ LADEN PLAATJES: {e}")
        print("Zorg dat player_down.png, player_up.png en player_left.png in de 'images' map staan!")

def create_screen():
    if FULLSCREEN:
        return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Speler instellingen
<<<<<<< HEAD
PLAYER_SPEED = 4 
PLAYER_SIZE = 40
PLAYER_VISUAL_SIZE = 120 # NIEUW: DIT IS JE PLAATJE (even groot als een tegel)
=======
PLAYER_SPEED = 4 # Iets langzamer voor preciezere beweging
PLAYER_SIZE = 40 # Iets kleiner dan de TILE_SIZE zodat je makkelijk door deuren past
<<<<<<< HEAD
PLAYER_COLOR = (255, 0, 0)
=======
PLAYER_COLOR = (255, 0, 0)



>>>>>>> e5c5492f288df5311fc0b810c68700be973df898
>>>>>>> cc1388f6c1163c40d5550069cc465d21ee75ff4e
