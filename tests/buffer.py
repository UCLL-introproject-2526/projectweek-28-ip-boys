import pygame

def create_main_surface():
    return pygame.display.set_mode((800, 600))

def clear_surface(surface):
    surface.fill((0, 0, 0))  # maakt het scherm volledig zwart

def render_frame(surface, x):
    clear_surface(surface)

    pygame.draw.circle(
        surface,
        (255, 0, 0),
        (x, 300),
        50
    )

    pygame.display.flip()

def main():
    pygame.init()
    surface = create_main_surface()

    x = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        render_frame(surface, x)
        x += 1

    pygame.quit()

if __name__ == "__main__":
    main()