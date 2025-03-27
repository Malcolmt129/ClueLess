import pygame
import constants
import game
import sys 
import button
from menu import Menu


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
    mainMenu = Menu("Main Menu", SCREEN)
    mainMenu.display()
    main()
