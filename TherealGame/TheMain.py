import pygame
import config
import os
import story
import game

def create_main_surface():
    return config.create_screen()

def draw_menu(screen, background):
    screen.blit(background, (0, 0))

    button = pygame.Rect(
        (config.SCREEN_WIDTH // 2) - 100,
        config.SCREEN_HEIGHT - 170,
        200,
        60
    )

    pygame.draw.rect(screen, config.GREEN, button, border_radius=10)

    font = pygame.font.Font(None, 36)
    text = font.render("New Game", True, (0, 0, 0))
    screen.blit(text, (button.x + 40, button.y + 15))

    pygame.display.flip()
    return button


def main():
    pygame.init()
    screen = create_main_surface()
    pygame.display.set_caption("Campus Creatures")

    config.load_assets()

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
    start_button = None
    
    story_instance = None
    game_instance = None 

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "MENU" and start_button:
                    if start_button.collidepoint(event.pos):
                        state = "STORY"
                        story_instance = story.Story(screen)

                elif state == "STORY" and story_instance:
                    story_instance.handle_click()

            if event.type == pygame.KEYDOWN:
                if state == "STORY" and story_instance:
                    if event.key == pygame.K_RIGHT:
                        story_instance.handle_click()


        if state == "MENU":
            start_button = draw_menu(screen, background)

        elif state == "STORY":
            story_instance.draw()
            if story_instance.finished():
                state = "GAME"
                game_instance = game.Game(screen)


        elif state == "GAME":
            if game_instance:
                game_instance.handle_input()
                game_instance.draw()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__": 
    main()