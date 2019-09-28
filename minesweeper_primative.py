import logging
import minesweeper_api as minesweeper
from os import system
from time import sleep
from curtsies import Input

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s.%(levelname)s.%(name)s.%(message)s.')
file_handler = logging.FileHandler('minesweeper.log')
file_handler.setFormatter(formatter)
log.addHandler(file_handler)

log.info('minesweeper_primative LOADED')

log.info('Getting size')
size = int(input('Enter a size: '))
log.debug(f'Size is {size}')

log.info('Getting number of mines')
num_mines = int(input('Enter # of mines: '))
log.debug(f'There are {num_mines} mines')

log.info('Initializing game')
game = minesweeper.game(size, size, num_mines)

xpos = 0
ypos = 0
    
def flip():
    log.info('Flipping')
    global xpos, ypos
    game.view = []
    for y in game.board:
        row = []
        for x in y:
            row += [x]
        game.view += [row]
    game.view[ypos][xpos] = 'XX'
    system('clear')
    minesweeper.printout(game.view)

def move():
    global xpos, ypos, alive
    log.info('Getting move direction/action')
    
    with Input(keynames='curses') as key_presses:
        for key in key_presses:
            log.debug(f'{key} pressed')
            
            if key == 'w' or key == 'KEY_UP' and ypos > 0:
                ypos -= 1
            elif key == 's' or key == 'KEY_DOWN' and ypos < game.y:
                ypos += 1
            elif key == 'a' or key == 'KEY_LEFT' and xpos > 0:
                xpos -= 1
            elif key == 'd' or key == 'KEY_RIGHT' and xpos < game.x:
                xpos += 1
                
            elif key == '/':
                game.board[ypos][xpos] = ' ?'
            elif key == 'f' or key == 'p':
                game.board[ypos][xpos] = ' P'
            elif key == 'x' or key == '\n':
                if not game.is_mine(xpos, ypos):
                    game.probe_tile(xpos, ypos)
                else:
                    alive = False
            else:
                log.warn('Bad value!')
            break
            
alive = True
while alive:
    flip()
    move()
    if len(game.probed_tiles) + game.num_mines == game.num_tiles:
        log.info('Game won')
        print('Game won!')
        alive = False
log.info('Game over')
print('Game Over')
