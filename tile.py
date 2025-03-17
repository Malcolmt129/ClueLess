import pygame 
import csv
import os
import spritesheet



class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet: spritesheet.Spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.parse_sprite(image)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x,y



class TileMap():

    def __init__(self,filename, spritesheet):
        self.tile_size = 32
        self.start_x, self.start_y = 0, 0
        self.spritesheet= spritesheet
        self.tiles = self.tiles_load(filename)
        self.map_surface = pygame.Surface((self.map_w,self.map_h))
        self.map_surface.set_colorkey((0,0,0))
        self.map_load()


    def map_load(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)
    

    def map_draw(self, surface):
        surface.blit(self.map_surface, (0,0))



    def _read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map


    def tiles_load(self, filename):
        tiles = []
        map = self._read_csv(filename)
        x,y = 0,0

        for row in map:
            x = 0

            for tile in row:
                if tile == '0':
                    self.start_x, self.start_y =  x * self.tile_size, y * self.tile_size
               
                elif tile == '21':
                    tiles.append(Tile("room.png", x * self.tile_size, y * self.tile_size, self.spritesheet))
                
                elif tile == '149':
                    tiles.append(Tile("hallway.png", x * self.tile_size, y * self.tile_size, self.spritesheet))


                x += 1
            y += 1


        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles 
