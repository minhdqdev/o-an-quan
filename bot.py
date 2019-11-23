import pygame
import os

from config import *
from copy import deepcopy
from random import shuffle, choice, randint
from table import fill_if_empty, finished, play_turn
import time
import sys
Lbutton = pygame.image.load(os.path.join(RES, 'left.png'))
Rbutton = pygame.image.load(os.path.join(RES, 'right.png'))

class Bot:
    def __init__(self, player_id, algo=None, screen=None, table=None):
        self.INF = 70
        self.quanvalue = QUANVALUE
        self.player_id = player_id
        self.algo = algo
        self.screen = screen
        self.table = table


    def checking_ending(self, state_, cur_point_):  # (bool_continue?, draw_win_lose)
        state, player_points = deepcopy(state_), deepcopy(cur_point_)

        if finished(state):
            player_points[0] += sum([i[0] for i in state[1:6]])
            player_points[1] += sum([i[0] for i in state[7:12]])

            if player_points[0] > player_points[1]:
                # print("USER_0 win !\n")
                return (True, -self.INF if self.player_id else self.INF)
            elif player_points[0] < player_points[1]:
                # print("USER_1 win !\n")
                return (True, self.INF if self.player_id else -self.INF)
            else:
                return (True, 0)

        return (False, player_points[1] if self.player_id else player_points[0])

    def get_available_move(self, state, player_id):
        list_of_action = []

        inc = 6 if player_id else 0
        for i in range(1+inc, 6+inc):
            if state[i][0]:
                list_of_action.extend([(i, 'l'), (i, 'r')])

        shuffle(list_of_action)
        return list_of_action

    def evaluationFunction(self, state, cur_point, is_ending):
        if is_ending[0]:
            return is_ending[1]+cur_point[1]-cur_point[0] if self.player_id else is_ending[1]+cur_point[0]-cur_point[1]
        return cur_point[1] - cur_point[0] if self.player_id else cur_point[0] - cur_point[1]

    def generate_next_move(self, state_, move, cur_point_, id):  # return next_state,next_point
        state, cur_point = deepcopy(state_), deepcopy(cur_point_)
        inc = 1 if move[1] == 'r' else -1
        cur_pos = move[0]
        next_pos = (cur_pos + inc) % 12

        while state[cur_pos][0]:
            state[cur_pos][0] -= 1
            state[next_pos][0] += 1
            next_pos = (next_pos + inc) % 12

        while True:
            if state[next_pos][1] or (state[next_pos][0] == 0 and state[(next_pos + inc) % 12][0] == 0 and
                                      state[(next_pos + inc) % 12][1] != 1):
                return state, cur_point
            elif state[next_pos][0] == 0 and (
                    state[(next_pos + inc) % 12][0] or state[(next_pos + inc) % 12][1] == 1):
                cur_point[id], state[(next_pos + inc) % 12][0] = cur_point[id] + state[(next_pos + inc) % 12][0], 0
                if state[(next_pos + inc) % 12][1] == 1:
                    cur_point[id] += self.quanvalue
                    state[(next_pos + inc) % 12][1] = 2

                if state[(next_pos + inc * 2) % 12][0] == 0 and state[(next_pos + inc * 2) % 12][1] != 1:
                    next_pos = (next_pos + inc * 2) % 12
            else:
                cur_pos = next_pos
                while state[cur_pos][0]:
                    state[cur_pos][0] -= 1
                    state[next_pos][0] += 1
                    next_pos = (next_pos + inc) % 12

    def alpha_beta(self, state_game, cur_point, depth=3):
        ## Depth_limited_search
        alpha, beta = -self.INF, self.INF

        def maxvalue(curState, cur_point, curDepth, alpha, beta):
            is_ending = self.checking_ending(curState, cur_point)  # (bool_continue?, draw_win_lose)
            if is_ending[0] or curDepth == 0:
                return self.evaluationFunction(curState, cur_point, is_ending)

            v = -self.INF

            curState, cur_point = fill_if_empty(curState, cur_point)

            for move in self.get_available_move(curState, self.player_id):
                next_state, next_point = self.generate_next_move(curState, move, cur_point, self.player_id)
                # print(move,next_state,next_point);input()
                v = max(v, minvalue(next_state, next_point, curDepth, alpha, beta))
                if v > beta: return v  # cut tree
                alpha = max(alpha, v)
            return v

        def minvalue(curState, cur_point, curDepth, alpha, beta):
            is_ending = self.checking_ending(curState, cur_point)  # (bool_continue?, draw_win_lose)
            if is_ending[0] or curDepth == 0:
                return self.evaluationFunction(curState, cur_point, is_ending)

            v = self.INF
            ## checking abandoned in here
            curState, cur_point = fill_if_empty(curState, cur_point)
            for move in self.get_available_move(curState, self.player_id ^ 1):
                next_state, next_point = self.generate_next_move(curState, move, cur_point, self.player_id ^ 1)
                # print(move,next_state,next_point);input()
                v = min(v, maxvalue(next_state, next_point, curDepth - 1, alpha, beta))
                if v < alpha: return v
                beta = min(beta, v)
            return v

        opt_action, score = None, -self.INF-20
        curState, cur_point = fill_if_empty(state_game, cur_point)
        for move in self.get_available_move(state_game, self.player_id):
            next_state, next_point = self.generate_next_move(curState, move, cur_point, self.player_id)  # max play
            cur_score = minvalue(next_state, next_point, depth, alpha, beta)
            # print(cur_score);input()
            if cur_score > score:
                score = cur_score
                opt_action = move
            alpha = max(alpha, score)
        # print(opt_action);input()
        return opt_action

    def expectimax(self, state_game, cur_point, depth=3):
        # number_agent = 2 # self define
        def generate_agent(state_game, cur_point, depth, idx_agent=0):
            is_ending = self.checking_ending(state_game, cur_point)
            if is_ending[0] or depth == 0:
                return "", self.evaluationFunction(state_game, cur_point, is_ending)
            else:
                maxAlpha = -self.INF-20 if idx_agent == 0 else 0
                curState, cur_point = fill_if_empty(state_game, cur_point)
                list_valid_move = self.get_available_move(curState, self.player_id ^ idx_agent)
                # print(list_valid_move)
                if idx_agent:
                    depth -= 1
                # print(idx_agent);input()

                best_move, next_agent = "", idx_agent ^ 1
                for move in list_valid_move:
                    next_state, next_point = self.generate_next_move(curState, move, cur_point,
                                                                      self.player_id ^ idx_agent)  # generate next move
                    result = generate_agent(next_state, next_point, depth, next_agent)
                    if idx_agent == 0:  # this guy playing
                        if result[1] > maxAlpha:
                            maxAlpha = result[1]
                            best_move = move
                    else:
                        maxAlpha += 1 / len(list_valid_move) * result[1]
                        best_move = move

                return (best_move, maxAlpha)

        ## return move, point,
        return generate_agent(state_game, cur_point, depth)[0]

    def random_algo(self, state_game):
        pos = 0
        if self.player_id:
            while True:
                pos = randint(7, 11)
                if state_game[pos][0] != 0:
                    break
        else:
            while True:
                pos = randint(1, 5)
                if state_game[pos][0] != 0:
                    break
        
        return pos, choice(['l', 'r'])

    def human(self, state_game, cur_point):
        move = [None, None]
        old_box = 0
        self.table.redraw()
        x, y = 0, 0
        isClicked = False

        available_boxes = []
        for i in range(1,6):
            if state_game[i][0] > 0:
                available_boxes.append(i)

        while True:
            isClicked = False
            # time.sleep(0.2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    x = mouse[0]
                    y = mouse[1]

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        isClicked = True


            if 240 < y < 340:
                if 160 < x < 260:
                    move[0] = 1
                    if move[0] not in available_boxes:
                        continue

                    if move[0] != old_box:
                        self.table.redraw()
                        self.screen.blit(Lbutton, (160, 276))
                        self.screen.blit(Rbutton, (228, 276))
                        old_box = move[0]

                    if isClicked:
                        move[1] = 'l' if x < 210 else 'r'

                elif 260 < x < 360:
                    move[0] = 2
                    if move[0] not in available_boxes:
                        continue

                    if move[0] != old_box:
                        self.table.redraw()
                        self.screen.blit(Lbutton, (260, 276))
                        self.screen.blit(Rbutton, (328, 276))
                        old_box = move[0]

                    if isClicked:
                        move[1] = 'l' if x < 310 else 'r'
                elif 360 < x < 460:
                    move[0] = 3
                    if move[0] not in available_boxes:
                        continue

                    if move[0] != old_box:
                        self.table.redraw()
                        self.screen.blit(Lbutton, (360, 276))
                        self.screen.blit(Rbutton, (428, 276))
                        old_box = move[0]

                    if isClicked:
                        move[1] = 'l' if x < 410 else 'r'
                elif 460 < x < 560:
                    move[0] = 4
                    if move[0] not in available_boxes:
                        continue

                    if move[0] != old_box:
                        self.table.redraw()
                        self.screen.blit(Lbutton, (460, 276))
                        self.screen.blit(Rbutton, (528, 276))
                        old_box = move[0]

                    if isClicked:
                        move[1] = 'l' if x < 510 else 'r'
                elif 560 < x < 660:
                    move[0] = 5
                    if move[0] not in available_boxes:
                        continue

                    if move[0] != old_box:
                        self.table.redraw()
                        self.screen.blit(Lbutton, (560, 276))
                        self.screen.blit(Rbutton, (628, 276))
                        old_box = move[0]

                    if isClicked:
                        move[1] = 'l' if x < 610 else 'r'
                else:
                    self.table.redraw()
                    old_box = 0

            else:
                self.table.redraw()
                old_box = 0

            pygame.display.flip()
            if move[0] is not None and move[1] is not None:
                break
        return move[0], move[1]

    def execute(self, state_game_, cur_point_, depth=3):
        state_game, cur_point = deepcopy(state_game_), deepcopy(cur_point_)

        if self.algo is None:  ## human play
            return self.human(state_game, cur_point)
        elif self.algo == "random":
            return self.random_algo(state_game)            
        elif self.algo == "alpha_beta":
            return self.alpha_beta(state_game, cur_point, depth)
        elif self.algo == "expectimax":
            return self.expectimax(state_game, cur_point, depth=2)
