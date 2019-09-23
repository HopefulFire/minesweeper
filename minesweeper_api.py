import logging
from colored import fg as fg_color
from colored import bg as bg_color
from colored import attr as style
from random import shuffle
from pprint import pformat

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s.%(levelname)s.%(name)s.%(message)s.')
file_handler = logging.FileHandler('minesweeper_api.log')
file_handler.setFormatter(formatter)
log.addHandler(file_handler)

class game():
    def reveal_all(self):
        log.info('Revealing all tiles')
        for y in range(self.y):
            for x in range(self.x):
                if not self.is_mine(x, y):
                    self.probe_tile(x, y)
        log.debug(f'\n{pformat(self.board)}')
        self.printout('board')
                
    def place_tile(self, x, y, mines_nearby):
        #
        # places tile on board
        #
        if not mines_nearby:
            log.debug(f'No mines near ({x}, {y}), placing \"  \"')
            tile = '  '
        else:
            log.debug(f'{mines_nearby} mines near ({x}, {y}), placing \"{mines_nearby}\"')
            tile = ' ' + str(mines_nearby)
        self.board[y][x] = tile
    
    def was_probed(self, x, y):
        if (x, y) in self.probed_tiles:
            log.debug(f'({x}, {y}) was already probed')
            return True
        else:
            log.debug(f'({x}, {y}) has not been probed, adding to probed_tiles')
            self.probed_tiles.add((x, y))
            return False
    
    def probe_tile(self, x, y):
        #
        # finds if there are nearby bombs, then searches further if there are not
        # also calls place_tile to update board
        #
        log.debug(f'Probing ({x}, {y}):')
        if self.was_probed(x, y):
            return None
            
        mines_nearby = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.is_inbounds(x+j, y+i):
                    if self.is_mine(x+j, y+i):
                        mines_nearby += 1
                        
        if not mines_nearby:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if self.is_inbounds(x+j, y+i):
                        self.probe_tile(x+j, y+i)
            
        self.place_tile(x, y, mines_nearby)
    
    def is_inbounds(self, x, y):
        #
        # finds if x, y location is a valid location on field/ board
        #
        if 0 <= x < self.x and 0 <= y < self.y:
            log.debug(f'({x}, {y}) is inbounds')
            return True
        else:
            log.debug(f'({x}, {y}) is out of bounds')
            return False
        
    def is_mine(self, x, y):
        #
        # finds if tile is a mine at x, y location on field
        #
        if self.field[y][x] == ' *':
            log.debug(f'({x}, {y}) is a mine')
            return True
        else:
            log.debug(f'({x}, {y}) is not a mine')
            return False
        

        
    def generate_field(self):
        #
        # generates a field
        #
        log.info('Generating minefield')
        temporary_field = ['  '] * self.num_tiles
        for i in range(self.num_mines):
            temporary_field[i] = ' *'
        shuffle(temporary_field)
        for y in range(self.y):
            row = []
            for x in range(self.x):
                row += [temporary_field.pop()]
            self.field += [row]
        log.debug(f'\n{pformat(self.field)}')
        
    def generate_board(self):
        #
        # generates an empty board
        #
        log.info('Generating player board')
        temporary_board = ['||'] * self.num_tiles
        for y in range(self.y):
            row = []
            for x in range(self.x):
                row += [temporary_board.pop()]
            self.board += [row]
        log.debug(f'\n{pformat(self.board)}')
        
    def __init__(self, x=10, y=10, num_mines=20):
        log.info('Initializing game')
        log.debug(f'Dimensions are ({x}, {y})')
        self.x = x
        self.y = y
        self.num_tiles = self.x * self.y
        log.debug(f'There are {num_mines} mines')
        self.num_mines = num_mines
        self.board = []
        self.generate_board()
        self.field = []
        self.generate_field()
        log.debug('Setting probed_tiles to empty set()')
        self.probed_tiles = set()

def printout(grid):
    #
    # prints out field or gameboard
    #
    log.debug(f'Printing grid:\n{pformat(grid)}')
    output = []
    for row in grid:
        line = []
        for tile in row:
            line += [colored(tile)]
        output += [''.join(line + ['\n'])]
    log.debug(f'Printing output:\n{pformat(output)}')
    print(''.join(output))

def colored(tile):
    #
    # sets tile colors for terminal
    #
    if tile == '||': # replaces tile with dark_gray blank space variant
        return ''.join((bg_color('dark_gray'), '  ', style('reset')))
    elif tile == '  ':
        return ''.join((bg_color('light_gray'), tile, style('reset')))
    elif tile == ' 1':
        return ''.join((bg_color('light_gray'), fg_color('green'), style('bold'), tile, style('reset')))
    elif tile == ' 2':
        return ''.join((bg_color('light_gray'), fg_color('yellow'), style('bold'), tile, style('reset')))
    elif tile == ' 3':
        return ''.join((bg_color('light_gray'), fg_color('blue'), style('bold'), tile, style('reset')))
    elif tile == ' 4':
        return ''.join((bg_color('light_gray'), fg_color('magenta'), style('bold'), tile, style('reset')))
    elif tile == ' 5':
        return ''.join((bg_color('light_gray'), fg_color('cyan'), style('bold'), tile, style('reset')))
    elif tile == ' 6':
        return ''.join((bg_color('light_gray'), fg_color('black'), style('bold'), tile, style('reset')))
    elif tile == ' 7':
        return ''.join((bg_color('light_gray'), fg_color('light_red'), style('bold'), tile, style('reset')))
    elif tile == ' 8':
        return ''.join((bg_color('light_gray'), fg_color('red'), style('bold'), tile, style('reset')))
    elif tile == ' P' or tile == ' ?' or tile == ' *' or tile == 'XX':
        return ''.join((bg_color('dark_gray'), fg_color('red'), style('bold'), tile, style('reset')))
