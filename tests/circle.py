import pygame

def create_main_surface():
    return pygame.display.set_mode((800, 600))

def render_frame(surface):
    pygame.draw.circle(
        surface,
        (255, 0, 0),
        (400, 300),
        100
    )
    pygame.display.flip()

def main():
    pygame.init()
    surface = create_main_surface()
    render_frame(surface)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()