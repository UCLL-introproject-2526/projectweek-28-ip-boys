import pygame
import asyncio
import os
import sys

# KEYWORD: MODULE IMPORTS
# [NL] Hier importeren we de code uit onze eigen mappenstructuur ('data').
# [NL] Dit zorgt ervoor dat dit hoofdbestand niet te rommelig wordt.
# [NL] We halen config (instellingen), game (het spel zelf) en story (het verhaal) op.
from data import config
from data import game
from data import story

async def main():
    pygame.init()
    pygame.mixer.init()

    # KEYWORD: SCREEN INITIALIZATION
    # [NL] We roepen de functie uit config aan om het schermvenster te maken.
    # [NL] Dit stelt de breedte en hoogte in (bv. 1024x768) en eventueel Fullscreen.
    # [NL] De variabele 'screen' is nu het canvas waar we alles op gaan tekenen.
    screen = config.create_screen()
    pygame.display.set_caption("Campus Creatures")

    # KEYWORD: ASSET LOADING
    # [NL] Voordat het spel begint, laden we alle plaatjes en geluiden in het geheugen.
    # [NL] Dit doen we nu al, zodat het spel niet hapert (lagged) tijdens het spelen.
    # [NL] De functie 'load_assets' vult de grote 'ASSETS' dictionary in config.py.
    config.load_assets()

    # Muziek starten
    if config.MUSIC_FILE and os.path.exists(config.MUSIC_FILE):
        try:
            pygame.mixer.music.load(config.MUSIC_FILE)
            pygame.mixer.music.set_volume(0.5)
            # KEYWORD: BACKGROUND MUSIC
            # [NL] We starten de achtergrondmuziek.
            # [NL] Het argument -1 is heel belangrijk: dit betekent 'infinite loop'.
            # [NL] Hierdoor stopt de muziek nooit, maar begint hij opnieuw als hij klaar is.
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Muziek fout: {e}")

    # Achtergrond menu laden
    if os.path.exists(config.MENU_BACKGROUND):
        background = pygame.image.load(config.MENU_BACKGROUND)
    else:
        background = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        background.fill(config.WHITE)
    
    background = pygame.transform.scale(background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    running = True
    
    # KEYWORD: STATE MACHINE
    # [NL] Dit is de kern van hoe we wisselen tussen schermen.
    # [NL] De variabele 'state' houdt bij waar we zijn: "MENU", "GAME", "SETTINGS" of "STORY".
    # [NL] Op basis van deze tekstwaarde beslist de loop beneden wat er getekend moet worden.
    state = "MENU"
    game_instance = None
    story_instance = None
    
    # Menu variabelen
    menu_options = ["Continue", "New Game", "Settings", "Backstory", "Quit"]
    selected_index = 1
    
    difficulties = ["EASY", "NORMAL", "HARD"]
    current_difficulty_index = 1
    is_fullscreen = config.FULLSCREEN

    next_state_after_story = "GAME"

    # --- MENU TEKEN FUNCTIE ---
    def draw_menu_screen():
        # KEYWORD: MENU RENDERING
        # [NL] Eerst tekenen we de achtergrondplaat over het hele scherm.
        # [NL] Daarna kijken we in welke modus we zitten (Settings of Hoofdmenu).
        # [NL] Op basis daarvan bepalen we welke tekstopties we moeten laten zien.
        screen.blit(background, (0, 0))
        
        # Instellingen menu of Hoofdmenu opties bepalen
        if state == "SETTINGS":
            diff_name = difficulties[current_difficulty_index]
            scr_name = "ON" if is_fullscreen else "OFF"
            current_options = [f"Difficulty: {diff_name}", f"Fullscreen: {scr_name}", "Back"]
            current_index = settings_index
        else:
            current_options = menu_options
            current_index = selected_index

        # Teken knoppen
        button_width = 400
        button_height = 60
        spacing = 20
        total_height = len(current_options) * (button_height + spacing)
        start_y = (config.SCREEN_HEIGHT - total_height) // 2 + 50
        center_x = config.SCREEN_WIDTH // 2
        
        font = pygame.font.Font(None, 48)

        for i, text in enumerate(current_options):
            y = start_y + (i * (button_height + spacing))
            rect = pygame.Rect(center_x - button_width//2, y, button_width, button_height)
            
            # KEYWORD: MENU SELECTION
            # [NL] We lopen door alle opties heen met een for-loop.
            # [NL] We vergelijken de huidige teller 'i' met 'selected_index'.
            # [NL] Als ze gelijk zijn, tekenen we die knop in het GOUD (geselecteerd).
            # [NL] Anders tekenen we de knop donkergrijs.
            if i == current_index:
                color = config.HIGHLIGHT_COLOR
                txt_col = (0,0,0)
                pygame.draw.rect(screen, (255,255,255), rect.inflate(6,6), border_radius=12)
            else:
                color = config.BUTTON_COLOR
                txt_col = config.TEXT_COLOR
            
            pygame.draw.rect(screen, color, rect, border_radius=10)
            text_surf = font.render(text, True, txt_col)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

    # Extra settings variabele
    settings_index = 0

    # KEYWORD: GAME LOOP
    # [NL] Dit is de 'motor' van het spel. Deze while-loop blijft oneindig draaien.
    # [NL] Elke herhaling van deze loop is één frame op je scherm (60x per seconde).
    # [NL] Hierin gebeuren 3 dingen: 1. Input lezen, 2. Spel updaten, 3. Tekenen.
    while running:
        # Event loop
        # KEYWORD: EVENT HANDLING
        # [NL] Pygame houdt een lijst bij van alles wat de gebruiker doet (toetsen, muis).
        # [NL] We lopen door die lijst heen. Als er op het kruisje is geklikt (QUIT), stoppen we.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # --- MENU INPUT ---
            if state == "MENU":
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_w]:
                        # KEYWORD: MENU NAVIGATION
                        # [NL] Als we naar boven drukken, verlagen we de index.
                        # [NL] De modulo (%) zorgt voor een 'wrap-around' effect.
                        # [NL] Voorbeeld: als index -1 wordt, springt hij automatisch naar de laatste optie.
                        selected_index = (selected_index - 1) % len(menu_options)
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        selected_index = (selected_index + 1) % len(menu_options)
                    elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                        choice = menu_options[selected_index]
                        
                        if choice == "Continue":
                            if os.path.exists(config.SAVE_FILE):
                                state = "GAME"
                                game_instance = game.Game(screen, load_saved=True)
                            else:
                                print("Geen savegame!")
                        elif choice == "New Game":
                            state = "STORY"
                            next_state_after_story = "GAME"
                            story_instance = story.Story(screen)
                            game_instance = None
                        elif choice == "Settings":
                            state = "SETTINGS"
                            settings_index = 0
                        elif choice == "Backstory":
                            state = "STORY"
                            next_state_after_story = "MENU"
                            story_instance = story.Story(screen)
                        elif choice == "Quit":
                            running = False

            # --- SETTINGS INPUT ---
            elif state == "SETTINGS":
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_w]:
                        settings_index = (settings_index - 1) % 3
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        settings_index = (settings_index + 1) % 3
                    elif event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_RIGHT]:
                        if settings_index == 0: # Difficulty
                            current_difficulty_index = (current_difficulty_index + 1) % len(difficulties)
                        elif settings_index == 1: # Fullscreen
                            is_fullscreen = not is_fullscreen
                            config.FULLSCREEN = is_fullscreen
                            if is_fullscreen: screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.FULLSCREEN)
                            else: screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
                            background = pygame.transform.scale(background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
                        elif settings_index == 2: # Back
                            state = "MENU"
                    elif event.key == pygame.K_ESCAPE:
                        state = "MENU"

            # --- STORY INPUT ---
            elif state == "STORY" and story_instance:
                if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT):
                    story_instance.handle_click()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = next_state_after_story
                    if state == "GAME" and game_instance is None:
                        game_instance = game.Game(screen, difficulty=difficulties[current_difficulty_index])

        # Draw loop
        if state in ["MENU", "SETTINGS"]:
            draw_menu_screen()
        
        elif state == "STORY":
            if story_instance:
                story_instance.draw()
                if story_instance.finished():
                    state = next_state_after_story
                    if state == "GAME" and game_instance is None:
                        game_instance = game.Game(screen, difficulty=difficulties[current_difficulty_index])

        elif state == "GAME":
            if game_instance:
                # KEYWORD: GAME UPDATE DRAW
                # [NL] Als we in de GAME state zijn, delegeren we alles naar het 'game_instance' object.
                # [NL] 'handle_input' berekent de nieuwe posities van de speler en vijanden.
                # [NL] 'draw' tekent daarna alles op het scherm.
                game_instance.handle_input()
                game_instance.draw()
                
                if game_instance.state == "MENU":
                    state = "MENU"
                    game_instance = None
        
        # KEYWORD: SCREEN FLIP
        # [NL] Pygame tekent alles eerst in een onzichtbaar geheugen (buffer).
        # [NL] Met 'flip' draaien we de buffer om en tonen we het nieuwe plaatje aan de speler.
        # [NL] Dit voorkomt flikkerend beeld (screen tearing).
        pygame.display.flip()
        
        # KEYWORD: FPS LOCK
        # [NL] We vertellen de klok dat hij moet wachten als de computer te snel is.
        # [NL] We willen dat het spel op maximaal 60 frames per seconde draait.
        # [NL] Dit zorgt ervoor dat het spel op elke computer even snel gaat.
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    # KEYWORD: ASYNCIO
    # [NL] We starten de main functie via asyncio.
    # [NL] Dit is specifiek nodig als we het spel later in een webbrowser willen draaien (via Pygbag).
    # [NL] Voor desktop gebruik werkt dit ook gewoon prima.
    asyncio.run(main())