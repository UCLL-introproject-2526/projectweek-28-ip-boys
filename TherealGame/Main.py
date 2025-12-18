import pygame
import config
import os
import story
import game

def create_main_surface():
    return config.create_screen()

def draw_menu(screen, background, options, selected_index):
    screen.blit(background, (0, 0))
    button_width = 400
    button_height = 60
    spacing = 20
    total_height = len(options) * (button_height + spacing)
    start_y = (config.SCREEN_HEIGHT - total_height) // 2 + 50 
    center_x = config.SCREEN_WIDTH // 2

    buttons_rects = []
    font = pygame.font.Font(None, 48)

    for i, option_text in enumerate(options):
        y = start_y + (i * (button_height + spacing))
        rect = pygame.Rect(center_x - (button_width // 2), y, button_width, button_height)
        buttons_rects.append(rect)

        if i == selected_index:
            color = config.HIGHLIGHT_COLOR
            text_col = (0, 0, 0) 
            pygame.draw.rect(screen, (255, 255, 255), rect.inflate(6, 6), border_radius=12)
        else:
            color = config.BUTTON_COLOR
            text_col = config.TEXT_COLOR

        pygame.draw.rect(screen, color, rect, border_radius=10)
        text_surf = font.render(option_text, True, text_col)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    pygame.display.flip()
    return buttons_rects


def main():
    pygame.init()
    # BELANGRIJK: Mixer starten voor geluid
    pygame.mixer.init()

    screen = create_main_surface()
    pygame.display.set_caption("Campus Creatures")

    config.load_assets()

    # --- MUZIEK LADEN EN STARTEN ---
    if os.path.exists(config.MUSIC_FILE):
        try:
            pygame.mixer.music.load(config.MUSIC_FILE)
            pygame.mixer.music.set_volume(0.5) # Volume (0.0 tot 1.0)
            pygame.mixer.music.play(-1) # -1 zorgt voor oneindige loop
            print(f"[INFO] Muziek gestart: {config.MUSIC_FILE}")
        except Exception as e:
            print(f"[FOUT] Kon muziek niet laden: {e}")
    else:
        print(f"[LET OP] Geen muziekbestand gevonden op: {config.MUSIC_FILE}")
    # -------------------------------

    if os.path.exists(config.MENU_BACKGROUND):
        background = pygame.image.load(config.MENU_BACKGROUND)
    else:
        background = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        background.fill(config.WHITE)

    background = pygame.transform.scale(
        background,
        (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
    )

    clock = pygame.time.Clock()
    running = True
    
    state = "MENU"
    story_instance = None
    game_instance = None 
    
    main_menu_index = 1 
    settings_menu_index = 0
    
    difficulties = ["EASY", "NORMAL", "HARD"]
    current_difficulty_index = 1 
    is_fullscreen = config.FULLSCREEN

    next_state_after_story = "GAME"

    while running:
        main_options = ["Continue", "New Game", "Settings", "Backstory", "Quit"]
        diff_name = difficulties[current_difficulty_index]
        scr_name = "ON" if is_fullscreen else "OFF"
        settings_options = [
            f"Difficulty: {diff_name}", 
            f"Fullscreen: {scr_name}", 
            "Back"
        ]

        # ---------------------------------------------
        # EVENT LOOP
        # ---------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # MENU INPUT
            if state == "MENU":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        main_menu_index = (main_menu_index - 1) % len(main_options)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        main_menu_index = (main_menu_index + 1) % len(main_options)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        choice = main_options[main_menu_index]
                        if choice == "Continue":
                            if os.path.exists(config.SAVE_FILE):
                                state = "GAME"
                                game_instance = game.Game(screen, load_saved=True)
                            else: print("[INFO] Geen savegame gevonden!")
                        elif choice == "New Game":
                            state = "STORY"
                            next_state_after_story = "GAME"
                            story_instance = story.Story(screen)
                            game_instance = None 
                        elif choice == "Settings":
                            state = "SETTINGS"
                            settings_menu_index = 0
                        elif choice == "Backstory":
                            state = "STORY"
                            next_state_after_story = "MENU"
                            story_instance = story.Story(screen)
                        elif choice == "Quit": running = False

            # SETTINGS INPUT
            elif state == "SETTINGS":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        settings_menu_index = (settings_menu_index - 1) % len(settings_options)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        settings_menu_index = (settings_menu_index + 1) % len(settings_options)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE or event.key == pygame.K_RIGHT:
                        if settings_menu_index == 0:
                            current_difficulty_index = (current_difficulty_index + 1) % len(difficulties)
                        elif settings_menu_index == 1:
                            is_fullscreen = not is_fullscreen
                            config.FULLSCREEN = is_fullscreen
                            if is_fullscreen: screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.FULLSCREEN)
                            else: screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
                            background = pygame.transform.scale(background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
                        elif settings_menu_index == 2: state = "MENU"
                    elif event.key == pygame.K_ESCAPE: state = "MENU"

            # STORY INPUT
            elif state == "STORY" and story_instance:
                if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT):
                    story_instance.handle_click()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = next_state_after_story
                    if state == "GAME" and game_instance is None:
                        game_instance = game.Game(screen, difficulty=difficulties[current_difficulty_index])

        # ---------------------------------------------
        # DRAW & UPDATE LOOPS
        # ---------------------------------------------
        if state == "MENU":
            draw_menu(screen, background, main_options, main_menu_index)

        elif state == "SETTINGS":
            draw_menu(screen, background, settings_options, settings_menu_index)

        elif state == "STORY":
            if story_instance:
                story_instance.draw()
                if story_instance.finished():
                    state = next_state_after_story
                    if state == "GAME":
                        game_instance = game.Game(screen, difficulty=difficulties[current_difficulty_index])

        elif state == "GAME":
            if game_instance:
                game_instance.handle_input() 
                game_instance.draw()
                
                if game_instance.state == "MENU":
                    state = "MENU"
                    game_instance = None 

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__": 
    main()