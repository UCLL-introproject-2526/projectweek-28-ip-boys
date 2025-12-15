import pygame

# Initialize Pygame
pygame.init()

def create_main_surface():
    # Tuple representing width and height in pixels
    screen_size = (1024, 768)

    # Create window with given size
    pygame.display.set_mode(screen_size)

create_main_surface()  

def main():
    # Initialize Pygame
    pygame.init()

    # Create main surface
    screen = create_main_surface()

    # Infinite loop (later wordt dit je game loop)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


# Call main manually
main()