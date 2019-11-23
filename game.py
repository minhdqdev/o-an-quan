'''
O an quan


Version: 0.4.*
Authors: 
'''
import random
import copy
import pygame
import math
import time
import concurrent.futures


from tablegui import TableGUI
from bot import Bot
from config import *


class Game:
    def __init__(self, algo_0=None, algo_1=None):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(SCREEN_CAPTION)
        
        self.table = TableGUI(self.screen)

        self.bots = [Bot(0, algo_0, self.screen), Bot(1, algo_1, self.screen)]
        self.move = None

    def redraw(self):
        self.table.redraw()
    
    def finished(self):
        return self.table.finished()

    def update(self, move):
        self.table.play(move)

    def run(self):
        # setup
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        turn = 0 if USER_GO_FIRST else 1
        running = True

        # loop
        self.redraw()
        while not self.finished():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

            # find the best move
            future = executor.submit(self.bots[turn].execute, self.table.state, self.table.player_points)
            move = future.result()
            self.update(move)

            print(f"USER_{turn}'s move: {move[0]} {move[1]}")

            turn ^= 1
            self.redraw()
            # executor.submit(self.redraw)

        if running:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        break
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break