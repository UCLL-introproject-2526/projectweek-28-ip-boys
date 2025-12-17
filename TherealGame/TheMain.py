import pygame
import config
import os
import story
import game

def create_main_surface():
    return config.create_screen()

def draw_menu(screen, background, options, selected_index):
    # Teken achtergrond
    screen.blit(background, (0, 0))

    # Instellingen voor de knoppen
    button_width = 300
    button_height = 60
    spacing = 20
    start_y = config.SCREEN_HEIGHT - (len(options) * (button_height + spacing)) - 50
    center_x = config.SCREEN_WIDTH // 2

    buttons_rects = []

    font = pygame.font.Font(None, 48)

    for i, option_text in enumerate(options):
        # Bereken positie
        y = start_y + (i * (button_height + spacing))
        rect = pygame.Rect(center_x - (button_width // 2), y, button_width, button_height)
        buttons_rects.append(rect)

        # Kleur bepalen: Geselecteerd = HIGHLIGHT, anders = BUTTON_COLOR
        if i == selected_index:
            color = config.HIGHLIGHT_COLOR
            text_col = (0, 0, 0) # Zwarte tekst op lichte knop
            pygame.draw.rect(screen, (255, 255, 255), rect.inflate(6, 6), border_radius=12)
        else:
            color = config.BUTTON_COLOR
            text_col = config.TEXT_COLOR

        # Teken de knop
        pygame.draw.rect(screen, color, rect, border_radius=10)

        # Teken de tekst
        text_surf = font.render(option_text, True, text_col)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    pygame.display.flip()
    return buttons_rects


def main():
    pygame.init()
    screen = create_main_surface()
    pygame.display.set_caption("Campus Creatures")

    config.load_assets()

    # Achtergrond laden
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
    
    # STATUS VARIABELEN
    state = "MENU"
    story_instance = None
    game_instance = None 
    
    # MENU OPTIES
    menu_options = ["Continue", "New Game", "Backstory", "Quit"]
    selected_index = 1 # Start standaard op "New Game"
    
    next_state_after_story = "GAME"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # --- INPUT IN MENU ---
            if state == "MENU":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        selected_index = (selected_index - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        selected_index = (selected_index + 1) % len(menu_options)
                    
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        choice = menu_options[selected_index]
                        
                        if choice == "Continue":
                            if os.path.exists(config.SAVE_FILE):
                                state = "GAME"
                                game_instance = game.Game(screen, load_saved=True)
                            else:
                                print("[INFO] Geen savegame gevonden!")
                        
                        elif choice == "New Game":
                            state = "STORY"
                            next_state_after_story = "GAME"
                            story_instance = story.Story(screen)
                            game_instance = None 
                        
                        elif choice == "Backstory":
                            state = "STORY"
                            next_state_after_story = "MENU"
                            story_instance = story.Story(screen)
                        
                        elif choice == "Quit":
                            running = False

            # --- INPUT IN STORY ---
            elif state == "STORY" and story_instance:
                if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT):
                    story_instance.handle_click()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = next_state_after_story
                    if state == "GAME" and game_instance is None:
                        game_instance = game.Game(screen)

            # --- INPUT IN GAME ---
            elif state == "GAME" and game_instance:
                pass 


        # --- DRAW LOOP ---
        if state == "MENU":
            draw_menu(screen, background, menu_options, selected_index)

        elif state == "STORY":
            if story_instance:
                story_instance.draw()
                if story_instance.finished():
                    state = next_state_after_story
                    if state == "GAME":
                        game_instance = game.Game(screen)

        elif state == "GAME":
            if game_instance:
                game_instance.handle_input()
                game_instance.draw()
                
                # Terug naar menu als game stopt
                if game_instance.state == "MENU":
                    state = "MENU"
                    game_instance = None 

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__": 
    main()