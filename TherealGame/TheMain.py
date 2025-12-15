import pygame
import config


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

    background = pygame.image.load(config.MENU_BACKGROUND)

    if not config.FULLSCREEN:
        background = pygame.transform.scale(
            background,
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )

    clock = pygame.time.Clock()
    running = True
    state = "MENU"
    start_button = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "MENU" and start_button:
                    if start_button.collidepoint(event.pos):
                        state = "GAME"

        if state == "MENU":
            start_button = draw_menu(screen, background)

        elif state == "GAME":
            screen.fill(config.BLACK)
            pygame.display.flip()

        clock.tick(60)

    pygame.quit()


main()
