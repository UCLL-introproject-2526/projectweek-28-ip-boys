import pygame
import os

# Scherm configuratie
WIDTH = 1000
HEIGHT = 700
SCREEN_SIZE = (WIDTH, HEIGHT)
FPS = 60

# Kleuren definities (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
UCLL_RED = (227, 6, 19)
GREY = (50, 50, 50)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
FADE_WHITE = (255, 255, 255, 180) # Voor transparante menu's

# Paden naar mappen (zodat we assets dynamisch vinden)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE_DIR, 'assets')
DATA_FILE = os.path.join(BASE_DIR, 'data.json')

# Initialiseer fonts (we gebruiken standaard fonts als fallback)
pygame.font.init()
DEFAULT_FONT = pygame.font.Font(None, 30)
TITLE_FONT = pygame.font.Font(None, 50)