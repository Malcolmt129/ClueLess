import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from board import Board
import game
from spritesheet import Spritesheet
from tile import TileMap
def main():
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ClueLess")
    clock = pygame.time.Clock()
    running_game = game.Game(screen) 
    running = True
    
    

    spritesheet  = Spritesheet('./assets/Pixel Crawler - Free Pack/Environment/Tilesets/Floors_Tiles.png')



    map = TileMap("./assets/board.csv", spritesheet)

    while running:
       
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        running_game.handle_events() 
        map.map_draw(screen)
        running_game.board.draw_characters()  

        pygame.display.flip() 

    pygame.quit()

if __name__ == "__main__":
    main()
