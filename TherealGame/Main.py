import pygame
import asyncio
import os
import sys

# We importeren nu vanuit de 'data' map
from data import config
from data import game
from data import story

async def main():
    pygame.init()
    pygame.mixer.init()

    # Scherm aanmaken
    screen = config.create_screen()
    pygame.display.set_caption("Campus Creatures")

    # Assets laden (config regelt nu de juiste paden naar ../assets)
    config.load_assets()

    # Muziek starten
    if config.MUSIC_FILE and os.path.exists(config.MUSIC_FILE):
        try:
            pygame.mixer.music.load(config.MUSIC_FILE)
            pygame.mixer.music.set_volume(0.5)
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
    
    # States
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

    while running:
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # --- MENU INPUT ---
            if state == "MENU":
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_w]:
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
                game_instance.handle_input()
                game_instance.draw()
                
                if game_instance.state == "MENU":
                    state = "MENU"
                    game_instance = None
        
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main())