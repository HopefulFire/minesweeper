from random import randint

class Field:


    def __init__(self, dimensions = [1, 1], num_mines = 0,
            is_hidden = True):

        self.dimensions = dimensions
        self.num_mines = num_mines
        self.is_hidden = is_hidden
        self.tiles = dict()
        self._create_tiles()
        self._add_mines()
        self._update_tiles()


    def _create_tiles(self):
        # create field of tiles
        for y in range(self.dimensions[1]):
            for x in range(self.dimensions[0]):
                self.tiles[(x, y)] = Tile(self.is_hidden)


    def _add_mines(self):
        if self.num_mines >= self.dimensions[0] * self.dimensions[1]:
            raise ZeroDivisionError
        chosen_locations = set()
        for i in range(self.num_mines):
            #this will loop forever if above is true!
            choice = None
            while choice is None or choice in chosen_locations:
                choice = (randint(0, self.dimensions[0] - 1), randint(0, self.dimensions[1] - 1))
            chosen_locations.update((choice, ))
        for location in chosen_locations:
            self.tiles[location].is_mined = True


    def _update_tiles(self):
        for tile_location in self.tiles:
            self.tiles[tile_location].mine_status = self._find_nearby_mines(tile_location)

    def _find_nearby_mines(self, tile_location):
        num_mines = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                x = tile_location[0] + dx
                y = tile_location[1] + dy
                if not self.in_field(x, y):
                    pass 
                elif self.tiles[(x, y)].is_mined:
                    num_mines += 1
        return num_mines

    
    def in_field(self, x, y):
        if x < 0 or y < 0 or x >= self.dimensions[0] or y >= self.dimensions[1]:
            return False
        else:
            return True

    
    def __str__(self):
        string = ''
        for y in range(self.dimensions[1]):
            for x in range(self.dimensions[0]):
                string += str(self.tiles[(x, y)])
            string += '\n'
        string += ''
        return string

            
    def __repr__(self):
        string = 'Field(' + str(self.dimensions) + ', ' + str(self.num_mines) + ', ' + str(self.is_hidden) +')'
        return string



class Tile:

    def __init__(self, is_hidden = True, is_mined = False,
            mine_status = 0):

        self.is_mined = is_mined
        self.is_hidden = is_hidden
        self.mine_status = mine_status


    def __str__(self):
        if self.is_hidden:
            string = '~'
        elif self.is_mined:
            string = 'M'
        else:
            string = str(self.mine_status)
        return string


    def __repr__(self):
        string = 'Tile(' + str(self.is_hidden) + ', ' + str(self.is_mined) + ', ' + str(self.mine_status) + ')'
        return string



# test code

tile = Tile(True, False, 0)
print(tile.__repr__())
print(tile)

field = Field((40, 40), 200, False)
print(field.__repr__())
print(field)
