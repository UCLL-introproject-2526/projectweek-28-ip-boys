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
TILE_SIZE = 64  # Elke tegel (muur, vloer) is 64x64 pixels

# =========================
# COLORS
# =========================
GREEN = (0, 180, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)  # Voor de vloer
DARK_GRAY = (50, 50, 50) # Voor muren
BLUE = (0, 0, 255)      # Voor deuren
YELLOW = (255, 200, 0) # voor de trappen

# =========================
# PATHS
# =========================
BASE_PATH = os.path.dirname(__file__)
IMAGE_PATH = os.path.join(BASE_PATH, "images")
MENU_BACKGROUND = os.path.join(IMAGE_PATH, "Poster_loadingScreen.png")

def create_screen():
    if FULLSCREEN:
        return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Speler instellingen
PLAYER_SPEED = 4 # Iets langzamer voor preciezere beweging
PLAYER_SIZE = 40 # Iets kleiner dan de TILE_SIZE zodat je makkelijk door deuren past
PLAYER_COLOR = (255, 0, 0)