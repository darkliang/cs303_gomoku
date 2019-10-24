def evaluation(self, chessboard, color):
    score_all_arr = []
    score_all_arr_enemy = []

    my_score = 0
    enemy_score = 0
    direction = [(0, 1), (1, 0), (1, 1), (-1, 1)]

    def cal_score(m, n, x_direction, y_direction, curr_score_arr, color):

        max_score_shape = (0, None)

        for shape in score_all_arr:
            if shape[0] > 1000 and (m, n) in shape[1] and (x_direction, y_direction) == shape[2]:
                return 0

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

        add_score = 0
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
                        continue
                    break
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