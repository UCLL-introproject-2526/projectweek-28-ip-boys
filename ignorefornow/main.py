import pygame
import sys
from ignorefornow.config import *

# We importeren de manager (die gaan we in de volgende stap maken)
# In het voorbeeldproject zaten alle classes in een package 'models'
from models.game_state_manager import GameStateManager

class GameApp:
    """ 
    Main class van de UCLL Battle Game. 
    Vergelijkbaar met 'App' class uit je voorbeeld.
    """
    def __init__(self):
        # 1. Pygame starten
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("UCLL: Battle for the Campus")
        self.clock = pygame.time.Clock()
        self.running = True

        # 2. De State Manager aanmaken
        # Deze regelt of we in het Menu, Gevecht of Pokedex zitten.
        self.state_manager = GameStateManager(self)
        
        # We beginnen in het 'welcome' scherm (net als in het voorbeeld)
        self.state_manager.set_state("welcome")

    def run(self):
        """ De Game Loop """
        while self.running:
            # A. Events checken (kruisje klikken, etc)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                # Geef events door aan de huidige state (Menu of Battle)
                if self.state_manager.get_state():
                    self.state_manager.get_state().handle_input(event)

            # B. Tekenen
            self.screen.fill(WHITE) # Schoonvegen
            
            if self.state_manager.get_state():
                self.state_manager.get_state().update()
                self.state_manager.get_state().draw()

            # C. Verversen
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = GameApp()
    game.run()