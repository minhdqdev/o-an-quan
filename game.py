'''
O an quan


Version: 0.4.*
Authors: 
'''
import random
import copy
import pygame,sys
import math
import time
import concurrent.futures
import os


from tablegui import TableGUI
from bot import Bot
from config import *

def text_to_screen(screen, text, x, y, fontsize, color):
    try:
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', fontsize)
        textsurface = myfont.render(text, True, color)
        screen.blit(textsurface, (x, y))

    except Exception as e:
        print('Font Error')
        raise e

class Game:
    def __init__(self, algo_0=None, algo_1=None):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(SCREEN_CAPTION)
        
        self.table = TableGUI(self.screen)

        self.bots = [Bot(0, algo_0, self.screen, self.table), Bot(1, algo_1, self.screen, self.table)]
        self.move = None

    def redraw(self, turn):

        self.table.redraw(turn)
    
    def finished(self):
        return self.table.finished()

    def update(self, move):
        self.table.play(move)

    def run(self):
        # setup
        # executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        turn = 0 if USER_GO_FIRST else 1
        running = True

        # loop
        self.redraw(turn)
        while not self.finished():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit();sys.exit()					
                    

            # find the best move
            # future = executor.submit(self.bots[turn].execute, self.table.state, self.table.player_points)
            # move = future.result()
            move = self.bots[turn].execute(self.table.state, self.table.player_points)
            self.update(move)

            print(f"USER_{turn}'s move: {move[0]} {move[1]}")
            # text_to_screen(self.screen, "User", 0, 0, 30, (123, 123, 123))

            turn ^= 1
            self.redraw(turn)
            print(self.table)
            # time.sleep(1)
            # executor.submit(self.redraw)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()