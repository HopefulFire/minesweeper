import logging
import minesweeper_api as minesweeper
from os import system
from time import sleep

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
    action = input('Enter wasd or ?fx: ')
    log.debug(f'Action is "{action}"')
    if action == 'w' and ypos > 0:
        ypos -= 1
    elif action == 's' and ypos < game.y:
        ypos += 1
    elif action == 'a' and xpos > 0:
        xpos -= 1
    elif action == 'd' and xpos < game.x:
        xpos += 1
    
    elif action == '?':
        game.board[ypos][xpos] = ' ?'
    
    elif action == 'f':
        game.board[ypos][xpos] = ' P'
        
    elif action == 'x':
        if not game.is_mine(xpos, ypos):
            game.probe_tile(xpos, ypos)
        else:
            alive = False
    else:
        print('bad value')
        sleep(5)
            
alive = True
while alive:
    flip()
    move()
log.info('Game over')
print('Game Over')
