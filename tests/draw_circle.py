import pygame
from pygame.display import flip
from pygame.draw import circle

# Kleuren
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Resolutie
WIDTH = 800
HEIGHT = 600

def create_main_surface():
    """Maakt het hoofdvenster en geeft de surface terug."""
    return pygame.display.set_mode((WIDTH, HEIGHT))

def render_frame(surface):
    """Tekent een frame: een rode cirkel en updatet het scherm."""
    surface.fill(WHITE)  # wis het scherm door het wit te maken
    circle(surface, RED, (WIDTH // 2, HEIGHT // 2), 50)  # teken cirkel
    flip()  # toon het scherm

def main():
    pygame.init()
    surface = create_main_surface()
    pygame.display.set_caption("Draw a Circle")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        render_frame(surface)

    pygame.quit()

if __name__ == "__main__":
    main()
