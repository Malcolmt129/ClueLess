import pygame
import constants
import game
from mainMenu import MainMenu
from turnMenu import TurnMenu


#Initialize the screen
pygame.init()
SCREEN = pygame.display.set_mode((constants.WIDTH,constants.HEIGHT))
pygame.display.set_caption("Clue-Less") 
CLOCK = pygame.time.Clock()
running_game = game.Game(SCREEN)


def main():

    running = True
    
    while running:
        SCREEN.fill("Black")
        CLOCK.tick(constants.FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        running_game.grid_draw()
        running_game.rooms_draw()

        pygame.display.update()
    pygame.quit()



    
    
if __name__ == "__main__":
    mainMenu = MainMenu(SCREEN)
    mainMenu.display()

    turnMenu = TurnMenu(SCREEN, "player1")
    turnMenu.run()


    main()


    
    
