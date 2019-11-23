'''

Author:
'''

import os
import pygame
from math import pi as PI

from config import *
from table import Table

background = pygame.image.load(os.path.join(RES, 'background.png'))   

# Properties definiton
O_DAN = (50, 50)
O_QUAN = (100, 100)  # ve hinh elipe, (x, y) nghia la truc ngan, truc dai
DAN = pygame.image.load(os.path.join(RES, 'dan.png'))
QUAN = pygame.image.load(os.path.join(RES, 'quan.png'))
QUANVALUE = 5
STATISTIC = [0, 0, 0]
TOTAL_SCORE_ = [0, 0]
HIGHEST_ = [0,0]


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

def buttonpress (marginleft, marginright, marginup, margindown, xbuttonleft, ybuttonleft, xbuttonright, ybuttonright, flag, move0, move1, point):
    if point:
        mouse = pygame.mouse.get_pos()

        move0 = (marginleft - 60)/100

        if marginleft < mouse[0] < marginright and marginup < mouse[1] < margindown:
            flag = True
        if flag:
            screen.blit(Rbutton, (xbuttonright, ybuttonright))
            screen.blit(Lbutton,(xbuttonleft, ybuttonleft))
            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN and xbuttonright < mouse[0] < xbuttonright+20 and ybuttonright < mouse[1] < ybuttonright+20:
                    print("Right Clicked!")
                    move1 = 'r'
                if e.type == pygame.MOUSEBUTTONDOWN and xbuttonleft < mouse[0] < xbuttonleft+20 and ybuttonleft < mouse[1] < ybuttonleft+20:
                    print("Left Clicked!")
                    move1 = 'l'

    flag = False
    # pygame.display.flip()
    # for e in pygame.event.get():
    #     if e.type == pygame.QUIT:
    #         pygame.quit()
    #         sys.exit()

    # move = (move0, move1)
    #  return move


class TableGUI(Table):
    '''
    O an quan table with GUI feature
    '''
    def __init__(self, screen=None):
        super().__init__()
        self.screen = screen
        
        if screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption(SCREEN_CAPTION)


    def __draw_table(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(background, (0, 0))
        text_to_screen(self.screen, "Player 1", 200, 60, 25, COLOR.ORANGE)
        text_to_screen(self.screen, str(self.player_points[1]), 370, 40, 50, COLOR.ORANGE)
        text_to_screen(self.screen, "Player 0", 470, 380, 25, COLOR.ORANGE)
        text_to_screen(self.screen, str(self.player_points[0]), 370, 365, 50, COLOR.ORANGE)
        # text_to_screen(self.screen, "Player " + str(self.turn) + "'s move: " + str(self.Move[0]) + "-" + str(self.Move[1]), 110, 200, 30, BLACK)
        # text_to_screen(self.screen, str(self.winner), 150, 250, 25, RED)

        # So quan trong cac o
        text_to_screen(self.screen, str(self.state[11][0]), 170, 150, 20, COLOR.ORANGE) #No. 11
        text_to_screen(self.screen, str(self.state[10][0]), 270, 150, 20, COLOR.ORANGE) #No. 10
        text_to_screen(self.screen, str(self.state[9][0]), 370, 150, 20, COLOR.ORANGE) #No. 9
        text_to_screen(self.screen, str(self.state[8][0]), 470, 150, 20, COLOR.ORANGE) #No. 8
        text_to_screen(self.screen, str(self.state[7][0]), 570, 150, 20, COLOR.ORANGE) #No. 7
        text_to_screen(self.screen, str(self.state[1][0]), 170, 250, 20, COLOR.ORANGE) #No. 1
        text_to_screen(self.screen, str(self.state[2][0]), 270, 250, 20, COLOR.ORANGE) #No. 2
        text_to_screen(self.screen, str(self.state[3][0]), 370, 250, 20, COLOR.ORANGE) #No. 3
        text_to_screen(self.screen, str(self.state[4][0]), 470, 250, 20, COLOR.ORANGE) #No. 4
        text_to_screen(self.screen, str(self.state[5][0]), 570, 250, 20, COLOR.ORANGE) #No. 5

        text_to_screen(self.screen, str(abs(self.state[0][1] - 2)), 120, 170, 30, COLOR.ORANGE)
        text_to_screen(self.screen, str(self.state[0][0]), 120, 230, 20, COLOR.ORANGE) #No. 0

        text_to_screen(self.screen, str(abs(self.state[6][1] - 2)), 670, 170, 30, COLOR.ORANGE)
        text_to_screen(self.screen, str(self.state[6][0]), 670, 230, 20, COLOR.ORANGE) #No. 6

        # Ve cac quan va Quan - Drawing the stones
        if (self.state[0][1] == 1):
            self.screen.blit(QUAN, (80, 200))

        if (self.state[6][1] == 1):
            self.screen.blit(QUAN, (685, 200))

        # Dat soi quan tren o ben trai
        if (self.state[0][0] >= 1): self.screen.blit(DAN, (130, 260))
        if (self.state[0][0] >= 2): self.screen.blit(DAN, (130, 275))
        if (self.state[0][0] >= 3): self.screen.blit(DAN, (115, 260))
        if (self.state[0][0] >= 4): self.screen.blit(DAN, (115, 275))
        if (self.state[0][0] >= 5): self.screen.blit(DAN, (100, 260))
        if (self.state[0][0] >= 6): self.screen.blit(DAN, (100, 275))
        if (self.state[0][0] >= 7): self.screen.blit(DAN, (85, 260))
        if (self.state[0][0] >= 8): self.screen.blit(DAN, (85, 275))

        # Dat soi quan tren o ben phai
        if (self.state[6][0] >= 1): self.screen.blit(DAN, (660, 260))
        if (self.state[6][0] >= 2): self.screen.blit(DAN, (660, 275))
        if (self.state[6][0] >= 3): self.screen.blit(DAN, (675, 260))
        if (self.state[6][0] >= 4): self.screen.blit(DAN, (675, 275))
        if (self.state[6][0] >= 5): self.screen.blit(DAN, (690, 260))
        if (self.state[6][0] >= 6): self.screen.blit(DAN, (690, 275))
        if (self.state[6][0] >= 7): self.screen.blit(DAN, (705, 260))
        if (self.state[6][0] >= 8): self.screen.blit(DAN, (705, 275))

        # Dat soi cho USER_0
        for i in range(1, 6):
            if (self.state[i][0] >= 1): self.screen.blit(DAN, (75 + 100*i, 285))
            if (self.state[i][0] >= 2): self.screen.blit(DAN, (75 + 100*i, 300))
            if (self.state[i][0] >= 3): self.screen.blit(DAN, (90 + 100*i, 285))
            if (self.state[i][0] >= 4): self.screen.blit(DAN, (90 + 100*i, 300))
            if (self.state[i][0] >= 5): self.screen.blit(DAN, (105 + 100*i, 285))
            if (self.state[i][0] >= 6): self.screen.blit(DAN, (105 + 100*i, 300))
            if (self.state[i][0] >= 7): self.screen.blit(DAN, (120 + 100*i, 285))
            if (self.state[i][0] >= 8): self.screen.blit(DAN, (120 + 100*i, 300))

        # Dat soi cho USER_1
        for i in range(7, 12):
            if (self.state[i][0] >= 1): self.screen.blit(DAN, (75 + 100*(12-i), 185))
            if (self.state[i][0] >= 2): self.screen.blit(DAN, (75 + 100*(12-i), 200))
            if (self.state[i][0] >= 3): self.screen.blit(DAN, (90 + 100*(12-i), 185))
            if (self.state[i][0] >= 4): self.screen.blit(DAN, (90 + 100*(12-i), 200))
            if (self.state[i][0] >= 5): self.screen.blit(DAN, (105 + 100*(12-i), 185))
            if (self.state[i][0] >= 6): self.screen.blit(DAN, (105 + 100*(12-i), 200))
            if (self.state[i][0] >= 7): self.screen.blit(DAN, (120 + 100*(12-i), 185))
            if (self.state[i][0] >= 8): self.screen.blit(DAN, (120 + 100*(12-i), 200))

        pygame.display.flip()
    
    def redraw(self):
        self.__draw_table()

if __name__ == '__main__':
    table = TableGUI()

    table.redraw()
    print(table)