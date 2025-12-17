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
PLAYER_SIZE = 40
PLAYER_VISUAL_SIZE = 80 # Groter gemaakt voor meer detail
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
        "speed": 5,
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
BOSS_SIZE = 128 # Boss is nu echt groot en gedetailleerd
BOSS_HP = 100
NORMAL_HP = 30
ZOMBIE_SPAWN_RATE = 300 

# =========================
# COLORS & PATHS
# =========================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (255, 0, 0)
BUBBLE_COLOR = (0, 200, 255) 
GREEN = (0, 255, 0)  # <--- DEZE WAS IK VERGETEN!
GOLD = (255, 215, 0)

BASE_PATH = os.path.dirname(__file__)
IMAGE_PATH = os.path.join(BASE_PATH, "images")
MENU_BACKGROUND = os.path.join(IMAGE_PATH, "Poster_loadingScreen.png")

# =========================
# 🎨 HIGH-RES PIXEL ART ENGINE
# =========================
def create_pixel_art(art_data, palette, pixel_scale):
    rows = len(art_data)
    cols = len(art_data[0])
    surface = pygame.Surface((cols * pixel_scale, rows * pixel_scale), pygame.SRCALPHA)
    
    for r, row in enumerate(art_data):
        for c, char in enumerate(row):
            if char in palette and palette[char] is not None:
                color = palette[char]
                pygame.draw.rect(surface, color, 
                                 (c * pixel_scale, r * pixel_scale, pixel_scale, pixel_scale))
    return surface

# --- UITGEBREID KLEURENPALET (Voor 3D effect) ---
# Transparant
TR = None 

# Huidtinten
SKIN_L = (255, 220, 180) # Licht
SKIN_M = (210, 160, 120) # Midden
SKIN_D = (160, 100, 80)  # Schaduw

# Haar / Zwart
BLK_L  = (80, 80, 80)
BLK_M  = (40, 40, 40)
BLK_D  = (10, 10, 10)

# Kleding (Speler - Grijs/Zwart zoals in je plaatje)
GRY_L  = (180, 180, 180)
GRY_M  = (120, 120, 120)
GRY_D  = (80, 80, 80)
JEAN_L = (60, 80, 100)
JEAN_D = (30, 40, 60)

# Zombie / Boss Kleuren
ZGR_L  = (140, 190, 100) # Zombie Groen Licht
ZGR_D  = (80, 120, 60)   # Zombie Groen Donker
RED_L  = (255, 50, 50)   # Bloed Licht
RED_D  = (150, 0, 0)     # Bloed Donker
GOLD_L = (255, 215, 0)
GOLD_D = (180, 140, 0)
VAMP_CLOAK = (80, 20, 40) # Vampier mantel

# --- TEKENINGEN (24x24 en 32x32 GRIDS) ---

# SPELER (24x24) - Met rugzak en gedetailleerd haar
ART_PLAYER = [
    "         BBBBBB         ",
    "       BBBBBBBBBB       ",
    "      BBBBBBBBBBBB      ",
    "      BBssBBBBssBB      ", # Haar met highlights
    "      BBssBBBBssBB      ",
    "      sssHHHHhhsss      ", # Hoofd
    "      ssHH.HH.hhss      ", # Ogen
    "      ssHH...Hhhss      ",
    "      sshhhhhhhhss      ",
    "      sshhhhhhhhss      ",
    "     GGGGGGGGGGGGGG     ", # Jas (Grey)
    "    GGGGGGGGGGGGGGGG    ",
    "    GGGGGGGGGGGGGGGG    ",
    "   GGGG  GGGG  GGGGGG   ", # Armen los
    "   GGGG  GGGG  GGGGGG   ",
    "   hhGG  GGGG  GGGGhh   ", # Handen
    "         JJJJ           ", # Broek
    "         JJJJ           ",
    "        JJJJJJ          ",
    "        JJ  JJ          ",
    "        JJ  JJ          ",
    "       LL    LL         ", # Schoenen
    "       LL    LL         ",
    "                        "
]

# BOSS: VAMPIER (32x32) - Met Schedel en Glas Bloed
ART_BOSS_VAMPIRE = [
    "           BBBBBBBBB            ",
    "         BBBBBBBBBBBBB          ",
    "        BBBBBBBBBBBBBBB         ",
    "       ZGZZZZZZZZZZZZZGZ        ", # Oren (G)
    "      ZGZZZZZZZZZZZZZZZGZ       ",
    "      ZZRRZZZZZZZZZZRRZZZ       ", # Rode Ogen (R)
    "      ZZRRZZZZZZZZZZRRZZZ       ",
    "      ZZZZZZZZ..ZZZZZZZZZ       ", # Neus
    "      ZZZZZZZ....ZZZZZZZZ       ", # Mond
    "      ZZZZZWWWWWWWWZZZZZZ       ", # Tanden
    "       ZZZZWWWWWWWWZZZZZ        ",
    "       MMMMMMMMMMMMMMMMM        ", # Kraag (M)
    "      MMMMMMMMMMMMMMMMMMM       ",
    "     RRRRRRRRRRRRRRRRRRRRR      ", # Rood Vest
    "    RRRRRRR   RR   RRRRRRRR     ",
    "    RRRRRR    RR    RRRRRRR     ",
    "   GGGGGG     RR     GGGGGGG    ", # Armen (Groen)
    "  GGGGGGG     RR     GGGGGGGG   ",
    "  G rrr G     RR     G WWWW G   ", # Glas (r) en Schedel (W)
    "  G rrr G     RR     WW.WW.WW   ",
    "  G rrr G     RR     WW....WW   ",
    "   G G G      RR      WWWWWW    ",
    "    G G      JJJJ      WWWW     ",
    "     G       JJJJ               ",
    "            JJJJJJ              ", # Broek
    "            JJ  JJ              ",
    "           JJ    JJ             ",
    "          LL      LL            ",
    "          LL      LL            ",
    "         LL        LL           ",
    "                                ",
    "                                "
]

# ZOMBIE (24x24) - Gescheurd en eng
ART_ZOMBIE = [
    "         ZZZZZZ         ",
    "       ZZZZZZZZZZ       ",
    "      ZZZZZZZZZZZZ      ",
    "      ZZRRZZZZRRZZ      ", # Rode ogen
    "      ZZZZZZZZZZZZ      ",
    "      ZZZZWWWWZZZZ      ", # Tanden
    "      zzzzzzzzzzzz      ", # Nek (donker)
    "     GGGGGGGGGGGGGG     ", # Shirt
    "    GGGGGGGGGGGGGGGG    ",
    "    GGrrGGGGGGGGrrGG    ", # Bloedvlekken (r)
    "   ZZ GGGGGGGGGG ZZ     ", # Armen
    "   ZZ GGGGGGGGGG ZZ     ",
    "   ZZ  GGGGGGGG  ZZ     ",
    "       JJJJJJJJ         ", # Broek
    "       JJJJJJJJ         ",
    "       JJ    JJ         ",
    "       JJ    JJ         ",
    "      L L    LL         ", # 1 Schoen mist
    "                LL      ",
    "                        "
]

# LERAAR (24x24) - Witte jas
ART_TEACHER = [
    "         MMMMMM         ", # Grijs haar
    "       MMMMMMMMMM       ",
    "      HHHHHHHHHHHH      ",
    "      HH00HHHH00HH      ", # Bril
    "      HHHHHHHHHHHH      ",
    "      hhhhhhhhhhhh      ",
    "     WWWWWWWWWWWWWW     ", # Witte jas
    "    WWWWWWWWWWWWWWWW    ",
    "    WWWWWWWWWWWWWWWW    ",
    "   HH WWWWWWWWWWWW HH   ",
    "   HH WWWWWWWWWWWW HH   ",
    "      TTTTTTTTTTTT      ", # Das (T)
    "      BBBBBBBBBBBB      ", # Broek
    "      BBBBBBBBBBBB      ",
    "      BB        BB      ",
    "     LL          LL     ",
    "                        "
]

# ITEMS
ART_KEY = [
    "      KKKK      ",
    "     K....K     ",
    "     K....K     ",
    "      KKKK      ",
    "       KK       ",
    "       KK       ",
    "      KKK       ",
    "       KK       ",
    "      KKK       ",
    "       KK       ",
    "                "
]

# =========================
# ASSETS LADEN
# =========================
ASSETS = {}

def load_assets():
    print("--- ASSETS GENEREREN (ULTRA DETAIL) ---")
    
    # Palet
    pal = {
        ' ': TR, 
        # Huid & Haar
        'H': SKIN_M, 'h': SKIN_D, 'B': BLK_M, 'b': BLK_D, 'M': GRY_L,
        '.': BLACK,  '0': BLACK,
        # Speler Kleding
        'G': GRY_M, 's': BLK_L, 'J': JEAN_L, 'L': BLK_D,
        # Zombie / Boss
        'Z': ZGR_L, 'z': ZGR_D, 'R': RED_L, 'r': RED_D,
        'W': WHITE, # Schedel/Jas
        # Items
        'K': GOLD_L,
        # Teacher extra
        'T': (200, 0, 0) # Rode das
    }
    
    # Boss Palet (Extra kleuren)
    pal_boss = {**pal, 'G': ZGR_L} # Groene handen

    # SCALING
    # Omdat we 24x24 en 32x32 gebruiken, moeten we minder hard schalen om op 64-80 pixels te komen.
    scale_player = 3  # 24 * 3 = 72 pixels (ongeveer)
    scale_boss = 4    # 32 * 4 = 128 pixels
    scale_item = 4    # 12 * 4 = 48 pixels

    # 1. Karakters
    ASSETS["player_sprites"] = {}
    p_img = create_pixel_art(ART_PLAYER, pal, scale_player)
    ASSETS["player_sprites"]["down"] = p_img
    ASSETS["player_sprites"]["up"] = p_img
    ASSETS["player_sprites"]["left"] = p_img
    ASSETS["player_sprites"]["right"] = pygame.transform.flip(p_img, True, False)
    
    ASSETS["enemy"] = create_pixel_art(ART_ZOMBIE, pal, scale_player)
    ASSETS["teacher"] = create_pixel_art(ART_TEACHER, pal, scale_player)
    
    # DE VAMPIER BOSS
    ASSETS["boss"] = create_pixel_art(ART_BOSS_VAMPIRE, pal_boss, scale_boss)

    # 2. Items
    ASSETS["item_key"] = create_pixel_art(ART_KEY, pal, scale_item)
    
    # Fallbacks voor omgeving (simpelere blocks is prima voor muren)
    def create_block(color, w, h):
        s = pygame.Surface((w, h))
        s.fill(color)
        # Randje
        pygame.draw.rect(s, (max(0,color[0]-50), max(0,color[1]-50), max(0,color[2]-50)), (0,0,w,h), 4)
        return s

    ASSETS["wall"] = create_block((100, 100, 100), TILE_SIZE, WALL_HEIGHT)
    
    # Vloer met textuur
    floor = pygame.Surface((TILE_SIZE, TILE_SIZE))
    floor.fill((120, 120, 120))
    pygame.draw.rect(floor, (100,100,100), (2,2,60,60))
    ASSETS["floor"] = floor

    ASSETS["door"] = create_block((0, 0, 150), TILE_SIZE, TILE_SIZE)
    ASSETS["locked_door"] = create_block((150, 0, 0), TILE_SIZE, TILE_SIZE)
    ASSETS["stairs"] = create_block((200, 200, 0), TILE_SIZE, TILE_SIZE)
    ASSETS["student_bench"] = create_block((139, 69, 19), TILE_SIZE, TILE_SIZE)
    
    # Overige items (Simpele placeholders met een letter erop)
    def create_icon_item(color, text):
        s = pygame.Surface((ITEM_SIZE, ITEM_SIZE))
        s.fill(color)
        font = pygame.font.SysFont(None, 24)
        ts = font.render(text, True, BLACK)
        s.blit(ts, (5,5))
        return s

    ASSETS["item_health"] = create_icon_item(GREEN, "HP")
    ASSETS["item_ammo"] = create_icon_item((255, 255, 0), "AM")
    ASSETS["item_shotgun"] = create_icon_item(PLAYER_COLOR, "SG")
    ASSETS["player_monster"] = p_img

    print("✅ High-End Pixel Art gegenereerd!")

def create_screen():
    if FULLSCREEN: return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else: return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))