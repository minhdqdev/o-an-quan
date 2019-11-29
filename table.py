'''

Author: minhdq99hp
'''
from config import *
import os
from copy import deepcopy
import pygame
from tkinter import *
from tkinter import messagebox
from config import *
import time

COLOR = Color()

def text_to_screen(screen, text, x, y, fontsize, color):
    try:
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', fontsize)
        textsurface = myfont.render(text, True, color)
        screen.blit(textsurface, (x, y))

    except Exception as e:
        print('Font Error')
        raise e

def ipos(pos, inc=1):
    '''get increased position'''
    return (pos + inc) % 12

def fill_if_empty(_state, _player_points):
    state, player_points = deepcopy(_state), deepcopy(_player_points)

    if not any([i[0] for i in state[1:6]]):  # USER_0's field is empty
        player_points[0] -= 5

        for i in range(1, 6):
            state[i][0] = 1

    if not any([i[0] for i in state[7:12]]):  # USER_1's field is empty
        player_points[1] -= 5

        for i in range(7, 12):
            state[i][0] = 1
    
    return state, player_points

def finished(_state):
    return  _state[0] == [0, 2] and _state[6] == [0, 2]

def play_turn(_state, _player_points, _move, quanvalue=5):
    state, player_points = deepcopy(_state), deepcopy(_player_points)
    move = _move

    player = 0 if 0 < move[0] < 6 else 1

    inc = 1 if move[1] == 'r' else -1

    cur_pos = move[0]
    next_pos = ipos(cur_pos, inc)
   
    for _ in range(state[cur_pos][0]):
        state[next_pos][0] += 1
        next_pos = ipos(next_pos, inc)
    state[cur_pos][0] //= 12

    while True:
        state, player_points = fill_if_empty(state, player_points)

        if state[next_pos][1] or (state[next_pos][0] == 0 and state[ipos(next_pos, inc)][0] == 0 and state[ipos(next_pos, inc)][1] != 1):
            # stop turn
            break
        elif state[next_pos][0] == 0 and (state[ipos(next_pos, inc)][0] or state[ipos(next_pos, inc)][1] == 1):
            # eatable
            if state[ipos(next_pos, inc)][1] == 1:
                # if isQuan: update Quan state
                player_points[player] += quanvalue
                state[ipos(next_pos, inc)][1] = 2
                            
            player_points[player] += state[ipos(next_pos, inc)][0]
            state[ipos(next_pos, inc)][0] = 0

            temp_pos = ipos(ipos(next_pos, inc), inc)
            if state[temp_pos][0] == 0 and state[temp_pos][1] != 1: # empty and not quan
                next_pos = temp_pos
            else:
                break
        else:
            # continue distribution
            cur_pos = next_pos
            next_pos = ipos(cur_pos, inc)

            for _ in range(state[cur_pos][0]):
                state[next_pos][0] += 1
                next_pos = ipos(next_pos, inc)
            state[cur_pos][0] //= 12

    return state, player_points

class Table:
    '''
    O an quan 

    '''
    def __init__(self):
        self.state = [[0, 1], [5, 0], [5, 0], [5, 0], [5, 0], [5, 0],
                      [0, 1], [5, 0], [5, 0], [5, 0], [5, 0], [5, 0]]
        self.player_points = [0, 0]
        self.quanvalue = QUANVALUE

    def __str__(self):
        return '''
            11 10  9  8  7  6 
        +--+--------------+--+
        |{:2}|{:2}|{:2}|{:2}|{:2}|{:2}|{:2}|
        |{:2}|--------------|{:2}|
        |  |{:2}|{:2}|{:2}|{:2}|{:2}|  |
        +--+--------------+--+
          0  1  2  3  4  5

        USER_0: {} USER_1: {}
        '''.format(
                " *" if self.state[0][1] == 1 else " ",
                self.state[11][0] if self.state[11][0] else '',
                self.state[10][0] if self.state[10][0] else '',
                self.state[9][0] if self.state[9][0] else '',
                self.state[8][0] if self.state[8][0] else '',
                self.state[7][0] if self.state[7][0] else '',
                " *" if self.state[6][1] == 1 else " ",  
                self.state[0][0] if self.state[0][0] else '',
                self.state[6][0] if self.state[6][0] else '',
                self.state[1][0] if self.state[1][0] else '',
                self.state[2][0] if self.state[2][0] else '',
                self.state[3][0] if self.state[3][0] else '',
                self.state[4][0] if self.state[4][0] else '',
                self.state[5][0] if self.state[5][0] else '',
                self.player_points[0], self.player_points[1])

    def finished(self):
        '''Checking whether if Game is finished'''
        if finished(self.state):
            if self.player_points[0] > self.player_points[1]:
                result = 'You win'
            elif self.player_points[0] < self.player_points[1]:
                result = 'Computer wins'
            else: result = 'Draw'
            print("END!!")
            # endscreen = pygame.display.set_mode((400, 300))
            # text_to_screen(endscreen, 'Winnwer is ' + winner, 0, 0, 20, COLOR.WHITE)
            while True:
                Tk().wm_withdraw()  # to hide the main window
                messagebox.showinfo('GAME OVER', 'Result: ' + result)
                time.sleep(1)
                break
            return True
        else:
            return False

    def play(self, move):
        self.state, self.player_points = play_turn(self.state, self.player_points, move)
        if finished(self.state):
            self.player_points[0] += sum([self.state[i][0] for i in range(1, 6)])
            self.player_points[1] += sum([self.state[i][0] for i in range(7, 12)])
            for i in range(0, 12):
                self.state[i][0] = 0
        self.redraw(1)
    
    def redraw(self):

        return

if __name__ == '__main__':
    table = Table()

    print(table)

    table.play((2, 'r'))

    print(table)