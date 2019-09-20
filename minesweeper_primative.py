import minesweeper_api as minesweeper
from os import system
from time import sleep

size = int(input('Enter a size: '))
num_mines = int(input('Enter # of mines: '))

game = minesweeper.game(size, size, num_mines)

xpos = 0
ypos = 0
    
def flip():
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
    global xpos, ypos    
    
    action = input('Enter wasd or ?fx: ')
    
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
            global alive
            alive = False
    else:
        print('bad value')
        sleep(5)
            
alive = True
while alive:
    flip()
    move()
print('Game Over')
