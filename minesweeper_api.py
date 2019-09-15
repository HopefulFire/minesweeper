from colored import fg as fg_color
from colored import bg as bg_color
from colored import attr as style
from random import shuffle
from pprint import pprint

class game():
    def reveal_all(self):
        for y in range(self.y):
            for x in range(self.x):
                if not self.is_mine(x, y):
                    self.probe_tile(x, y)
        self.printout('board')
                
    def place_tile(self, x, y, mines_nearby):
        #
        # places tile on board
        #
        if not mines_nearby:
            tile = '  '
        else:
            tile = ' ' + str(mines_nearby)
        self.board[y][x] = tile
    
    def probe_tile(self, x, y):
        #
        # finds if there are nearby bombs, then searches further if there are not
        # also calls place_tile to update board
        #
        mines_nearby = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.is_inbounds(x+j, y+i):
                    if self.is_mine(x+j, y+i):
                        mines_nearby += 1
        self.place_tile(x, y, mines_nearby)
    
    def is_inbounds(self, x, y):
        #
        # finds if x, y location is a valid location on field/ board
        #
        if 0 <= x < self.x and 0 <= y < self.y:
            return True
        else:
            return False
        
    def is_mine(self, x, y):
        #
        # finds if tile is a mine at x, y location on field
        #
        if self.field[y][x] == ' *':
            return True
        else:
            return False
        
    def printout(self, name='field'):
        #
        # prints out field or gameboard
        #
        if name == 'field':
            board = self.field
        elif name == 'board':
            board = self.board
        output = []
        for row in board:
            line = []
            for tile in row:
                line += [colored(tile)]
            output += [''.join(line + ['\n'])]
        print(''.join(output))
        
    def generate_field(self):
        #
        # generates a field
        #
        temporary_field = ['  '] * self.num_tiles
        for i in range(self.num_mines):
            temporary_field[i] = ' *'
        shuffle(temporary_field)
        for y in range(self.y):
            row = []
            for x in range(self.x):
                row += [temporary_field.pop()]
            self.field += [row]
        self.printout('field')
        
    def generate_board(self):
        #
        # generates an empty board
        #
        temporary_board = ['||'] * self.num_tiles
        for y in range(self.y):
            row = []
            for x in range(self.x):
                row += [temporary_board.pop()]
            self.board += [row]
        self.printout('board')
        
    def __init__(self, x=10, y=10, num_mines=20):
        print(self)
        self.x = x
        self.y = y
        self.num_tiles = self.x * self.y
        self.num_mines = num_mines
        self.board = []
        self.generate_board()
        self.field = []
        self.generate_field()

class gui():
    def __init__(self):
        pass

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
    elif tile == ' P' or tile == ' ?' or tile == ' *':
        return ''.join((bg_color('dark_gray'), fg_color('red'), style('bold'), tile, style('reset')))
