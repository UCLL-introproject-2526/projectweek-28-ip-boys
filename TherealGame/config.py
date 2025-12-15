import os
import pygame

# =========================
# SCREEN CONFIG
# =========================

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FULLSCREEN = False  # 👉 zet op True voor fullscreen

# =========================
# COLORS
# =========================

GREEN = (0, 180, 0)
BLACK = (0, 0, 0)

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