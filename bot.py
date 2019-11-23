from config import *
from copy import deepcopy
from random import shuffle
from table import fill_if_empty, finished, choice, play_turn

class Bot:
    def __init__(self, player_id, algo=None, screen=None):
        self.INF = 70
        self.quanvalue = QUANVALUE
        self.player_id = player_id
        self.algo = algo

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
            return is_ending[1]+cur_point[1]+cur_point[2]-cur_point[0] if self.player_id else is_ending[1]+cur_point[0]-cur_point[2]-cur_point[1]
        return cur_point[1] + cur_point[2] - cur_point[0] if self.player_id else cur_point[0] - cur_point[2] - cur_point[1]

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
            ## checking abandoned in here
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
                pos = random.randint(7, 11)
                if state_game[pos][0] != 0:
                    break
        else:
            while True:
                pos = random.randint(1, 5)
                if state_game[pos][0] != 0:
                    break
        
        return pos, random.choice(['l', 'r'])

    def execute(self, state_game_, cur_point_, depth=3):
        state_game, cur_point = deepcopy(state_game_), deepcopy(cur_point_)

        if self.algo == None:  ## human play
            move = None
            return move
        elif self.algo == "random":
            return self.random_algo(state_game)            
        elif self.algo == "alpha_beta":
            return self.alpha_beta(state_game, cur_point, depth)
        elif self.algo == "expectimax":
            return self.expectimax(state_game, cur_point, depth=2)
