#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
SCORE_MAX = 0x7fffffff
SCORE_MIN = -1 * SCORE_MAX
# 棋型的评估分数
shape_score_5 = [
    (200, (1, 0, 1, 0, 0)),
    (200, (0, 0, 1, 0, 1)),
    (400, (1, 1, 0, 0, 0)),
    (400, (0, 0, 0, 1, 1)),
    (600, (0, 1, 0, 1, 0)),
    (800, (0, 1, 1, 0, 0)),
    (800, (0, 0, 1, 1, 0)),
    (2500, (1, 1, 0, 1, 0)),
    (2500, (0, 1, 0, 1, 1)),
    (2500, (1, 0, 1, 1, 0)),
    (2500, (0, 1, 1, 0, 1)),
    (3000, (0, 0, 1, 1, 1)),
    (3000, (1, 1, 1, 0, 0)),
    (4000, (0, 1, 1, 1, 0)),
    (8000, (1, 1, 1, 0, 1)),
    (8000, (1, 1, 0, 1, 1)),
    (8000, (1, 0, 1, 1, 1)),
    (12000, (1, 1, 1, 1, 0)),
    (12000, (0, 1, 1, 1, 1)),
    (99999999, (1, 1, 1, 1, 1))]

shape_score_6 = [
    (3500, (0, 1, 0, 1, 1, 0)),
    (3500, (0, 1, 1, 0, 1, 0)),
    (9000, (1, 1, 1, 0, 1, 0)),
    (9000, (0, 1, 0, 1, 1, 1)),
    (9000, (0, 1, 1, 1, 0, 1)),
    (9000, (1, 0, 1, 1, 1, 0)),
    (30000, (0, 1, 1, 1, 1, 0))
]

score_table = {
    'five': 10000000,
    'live_four': 100000,
    'jump_four': 40000,
    'jump_four_2': 35000,
    'dead_four': 35000,
    'live_three': 35000,
    'jump_three': 7000,
    'jump_three_2': 5000,
    'dead_three': 5000,
    'live_two': 1000,
    'jump_two': 700,
    'dead_two': 500
}


class AI(object):
    #   chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        #   You are white or black
        self.color = color
        #   the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        #   You need add your decision into your candidate_list.
        #   System will get the end of your candidate_list as your decision .
        self.candidate_list = []
        #   last my list

        self.empty_list = []
        self.max_depth = 6 if color == COLOR_BLACK else 6
        self.search_breadth = 6

        self.defence_factor = 1 if color == COLOR_BLACK else 1.3

    #   The input is current chessboard.

    def go(self, chessboard):

        empty_list = np.where(chessboard == COLOR_NONE)
        self.empty_list = list(zip(empty_list[0], empty_list[1]))
        # Clear candidate_list
        self.candidate_list.clear()

        if len(self.empty_list) == 15 * 15:
            new_pos = (7, 7)
            self.candidate_list.append(new_pos)
            return

        start = time.time()
        self.alpha_beta(self.max_depth, chessboard, SCORE_MIN, SCORE_MAX, self.color)

        print(time.time() - start)

    def has_neighbor(self, next_step, chessboard):
        x, y = next_step[0], next_step[1]
        for i in range(-1, 2):
            for j in range(-1, 2):
                tmp_x, tmp_y = x + i, y + j
                if -1 < tmp_x < self.chessboard_size and -1 < tmp_y < self.chessboard_size and chessboard[tmp_x][tmp_y] \
                        != COLOR_NONE:
                    return True
        return False

    def is_win(self, chessboard, move, color):
        direction = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        for x_d, y_d in direction:
            line = [0 for _ in range(9)]
            for i in range(-4, 5):
                m = move[0] + i * x_d
                n = move[1] + i * y_d
                if (m < 0 or m >= self.chessboard_size or
                        n < 0 or n >= self.chessboard_size):
                    line[i + 4] = -color
                else:
                    line[i + 4] = chessboard[m][n]
            color_number = 1
            for i in range(3, -1, -1):
                if line[i] == color:
                    color_number += 1
                else:
                    break

            for i in range(5, 9):
                if line[i] == color:
                    color_number += 1
                else:
                    break
            if color_number >= 5:
                return True

        return False

    def alpha_beta(self, depth, chessboard, alpha, beta, color):
        if depth == 0 or len(self.empty_list) == 0:
            return self.evaluation(chessboard, color)

        self.search_breadth = 2 if depth != self.max_depth else 6
        moves = self.heuristic(chessboard, color)
        # if there are no moves, just return the score

        for _, (x, y) in moves:
            chessboard[x][y] = color
            self.empty_list.remove((x, y))

            if self.is_win(chessboard, (x, y), color):
                score = - self.evaluation(chessboard, -color)
            else:
                score = - self.alpha_beta(depth - 1, chessboard, -beta, -alpha, -color)
            self.empty_list.append((x, y))

            chessboard[x][y] = 0

            # alpha/beta pruning
            if score > alpha:
                if depth == self.max_depth:
                    self.candidate_list.append((x, y))
                if score >= beta:
                    return beta
                alpha = score

        return alpha

    def heuristic(self, chessboard, color):
        moves = []
        direction = [(0, 1), (1, 0), (1, 1), (-1, 1)]

        def cal(x, y, dir, cl):
            line = [0 for _ in range(9)]
            for i in range(-4, 5):
                m = x + i * dir[0]
                n = y + i * dir[1]
                if (m < 0 or m >= self.chessboard_size or
                        n < 0 or n >= self.chessboard_size):
                    line[i + 4] = -cl
                else:
                    line[i + 4] = chessboard[m][n]
            line[4] = cl
            color_number = 1
            block = 0
            left_gap, right_gap = 0, 0
            gap = 0
            for i in range(3, -1, -1):
                if line[i] == cl:
                    color_number += 1
                    if line[i + 1] == 0:
                        gap += 1
                elif line[i] == 0:
                    if line[i + 1] == 0:
                        break
                else:
                    block += 1
                    if line[i + 1] == 0:
                        left_gap += 1
                    break

            for i in range(5, 9):
                if line[i] == cl:
                    color_number += 1
                    if line[i - 1] == 0:
                        gap += 1
                elif line[i] == 0:  # 最后一个子不算gap
                    if line[i - 1] == 0:
                        break
                else:
                    block += 1
                    if line[i - 1] == 0:
                        right_gap += 1
                    break

            if color_number >= 5:
                if gap == 0:
                    return score_table['five']
                else:
                    return score_table['live_four']
            if block == 0 or (left_gap + right_gap + color_number + gap >= 5):
                if color_number == 4:  # 活四
                    if gap == 2:
                        return score_table['jump_four_2']
                    elif gap == 1:
                        return score_table['jump_four']
                    else:
                        return score_table['live_four']
                elif color_number == 3:
                    if gap == 2:
                        return score_table['jump_three_2']
                    elif gap == 1:
                        return score_table['jump_three']
                    else:
                        return score_table['live_three']
                elif color_number == 2:
                    if gap == 1:
                        return score_table['jump_two']
                    elif gap == 0:
                        return score_table['live_two']
            elif block == 1:
                if color_number == 4:  # 死四
                    return score_table['dead_four']
                elif color_number == 3:
                    return score_table['dead_three']
                elif color_number == 2:
                    return score_table['dead_two']
            return 0

        for move in self.empty_list:
            if not self.has_neighbor(move, chessboard):
                continue
            my_score = 0
            enemy_score = 0
            for i in range(4):
                my_score += cal(move[0], move[1], direction[i], color)
                enemy_score += cal(move[0], move[1], direction[i], -color)

            moves.append((my_score + 0.7 * enemy_score, move))
        moves.sort(reverse=True)
        return moves[:self.search_breadth]

    def evaluation(self, chessboard, color):
        # 算自己的得分
        score_all_arr = []  # 得分形状的位置 用于计算如果有相交 得分翻倍
        score_all_arr_enemy = []

        my_score = 0
        enemy_score = 0
        direction = [(0, 1), (1, 0), (1, 1), (-1, 1)]

        def cal_score(m, n, x_direction, y_direction, curr_score_arr, color):

            # 在一个方向上， 只取最大的得分项
            max_score_shape = (0, None)

            # 如果此方向上，该点已经有得分形状，不重复计算
            for shape in score_all_arr:
                if shape[0] > 1000 and (m, n) in shape[1] and (x_direction, y_direction) == shape[2]:
                    return 0

            # 在落子点 左右方向上循环查找得分形状
            pos = []
            coord = []
            for i in range(-5, 6):
                x = m + i * x_direction
                y = n + i * y_direction
                coord.append((x, y))
                if x >= self.chessboard_size or x < 0 or y >= self.chessboard_size or y < 0:
                    pos.append(2)
                elif chessboard[x][y] == 0:
                    pos.append(0)
                elif chessboard[x][y] == color:
                    pos.append(1)
                else:
                    pos.append(2)

            for j in range(0, 6):
                shape_5 = (pos[j], pos[j + 1], pos[j + 2], pos[j + 3], pos[j + 4])
                shape_6 = (pos[j], pos[j + 1], pos[j + 2], pos[j + 3], pos[j + 4], pos[j + 5])
                for (score, shape) in shape_score_6:
                    if score > max_score_shape[0] and shape_6 == shape:
                        max_score_shape = (
                            score, (coord[j], coord[j + 1], coord[j + 2], coord[j + 3], coord[j + 4], coord[j + 5]),
                            (x_direction, y_direction))
                for (score, shape) in shape_score_5:
                    if score > max_score_shape[0] and shape_5 == shape:
                        max_score_shape = (
                            score, (coord[j], coord[j + 1], coord[j + 2], coord[j + 3], coord[j + 4]),
                            (x_direction, y_direction))

            shape_tmp = (pos[6], pos[7], pos[8], pos[9], pos[10])
            for (score, shape) in shape_score_5:
                if score > max_score_shape[0] and shape_tmp == shape:
                    max_score_shape = (
                        score, (coord[6], coord[7], coord[8], coord[9], coord[10]),
                        (x_direction, y_direction))

            add_score = 0  # 加分项
            # 计算两个形状相交， 如两个3活 相交， 得分增加
            if max_score_shape[1] is not None:
                for shape in curr_score_arr:
                    for pt1 in shape[1]:
                        for pt2 in max_score_shape[1]:
                            if pt1 == pt2:
                                if shape[0] >= 2000 and max_score_shape[0] >= 2000:
                                    add_score = max(shape[0], max_score_shape[0])
                                else:
                                    add_score = min(shape[0], max_score_shape[0])
                                break
                        else:
                            continue  # 其中else块中的语句将在for循环完整执行过之后才会被执行，如果for循环被break，则else块将不会被执行。
                        break  # 如果有一个子对上了 就不再给这个棋形重复加分了
                curr_score_arr.append(max_score_shape)
            return add_score + max_score_shape[0]

        for x in range(0, self.chessboard_size):
            for y in range(0, self.chessboard_size):
                if chessboard[x][y] == color:
                    for i in range(4):
                        my_score += cal_score(x, y, direction[i][0], direction[i][1], score_all_arr,
                                              color)
                elif chessboard[x][y] == -color:
                    for i in range(4):
                        enemy_score += cal_score(x, y, direction[i][0], direction[i][1],
                                                 score_all_arr_enemy, -color)

        total_score = my_score - self.defence_factor * enemy_score
        return total_score
