import pygame
import constants
import game


def main():

    #Initialize the screen
    pygame.init()
    screen = pygame.display.set_mode((constants.WIDTH,constants.HEIGHT))
    pygame.display.set_caption("Clue-Less") 
    clock = pygame.time.Clock()
    running_game = game.Game(screen)
    running = True

    while running:

        clock.tick(constants.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        running_game.grid_draw()
        running_game.rooms_draw()
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
