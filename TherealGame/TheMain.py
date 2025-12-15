import os
import pygame


def create_main_surface():
    return pygame.display.set_mode((1024, 768))


def draw_menu(screen, background):
    screen.blit(background, (0, 0))

    button = pygame.Rect(412, 600, 200, 60)
    pygame.draw.rect(screen, (0, 180, 0), button, border_radius=10)

    font = pygame.font.Font(None, 36)
    text = font.render("New Game", True, (0, 0, 0))
    screen.blit(text, (button.x + 40, button.y + 15))

    pygame.display.flip()
    return button


def main():
    pygame.init()
    screen = create_main_surface()
    pygame.display.set_caption("Campus Creatures")

    base_path = os.path.dirname(__file__)
    image_path = os.path.join(base_path, "images", "Poster_loadingScreen.png")

    background = pygame.image.load(image_path)
    background = pygame.transform.scale(background, (1024, 768))


    clock = pygame.time.Clock()
    running = True
    state = "MENU"

    start_button = None  # ✅ BELANGRIJK

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
            screen.fill((0, 0, 0))
            pygame.display.flip()

        clock.tick(60)

    pygame.quit()


main()