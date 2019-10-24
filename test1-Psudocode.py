FUNCTION evaluation(self, chessboard, color):
    score_all_arr <- []
    score_all_arr_enemy <- []
    my_score <- 0
    enemy_score <- 0
    direction <- [(0, 1), (1, 0), (1, 1), (-1, 1)]
    FUNCTION cal_score(m, n, x_direction, y_direction, curr_score_arr, color):
        max_score_shape <- (0, None)
        for shape in score_all_arr:
            IF shape[0] > 1000 AND (m, n) in shape[1] AND (x_direction, y_direction) = shape[2]:
                RETURN 0
            ENDIF
        ENDFOR
        pos <- []
        coord <- []
        for i in range(-5, 6):
            x <- m + i * x_direction
            y <- n + i * y_direction
            coord.append((x, y))
            IF x >=  chessboard_size OR x < 0 OR y >=  chessboard_size OR y < 0:
                pos.append(2)
            ELSEIF chessboard[x][y] = 0:
                pos.append(0)
            ELSEIF chessboard[x][y] = color:
                pos.append(1)
            ELSE:
                pos.append(2)
            ENDIF
        ENDFOR
        for j in range(0, 6):
            shape_5 <- (pos[j], pos[j + 1], pos[j + 2], pos[j + 3], pos[j + 4])
            shape_6 <- (pos[j], pos[j + 1], pos[j + 2], pos[j + 3], pos[j + 4], pos[j + 5])
            for (score, shape) in shape_score_6:
                IF score > max_score_shape[0] AND shape_6 = shape:
                    max_score_shape <- (
                        score, (coord[j], coord[j + 1], coord[j + 2], coord[j + 3], coord[j + 4], coord[j + 5]),
                        (x_direction, y_direction))
                ENDIF
            ENDFOR
            for (score, shape) in shape_score_5:
                IF score > max_score_shape[0] AND shape_5 = shape:
                    max_score_shape <- (
                        score, (coord[j], coord[j + 1], coord[j + 2], coord[j + 3], coord[j + 4]),
                        (x_direction, y_direction))
                ENDIF
        ENDFOR
            ENDFOR
        shape_tmp <- (pos[6], pos[7], pos[8], pos[9], pos[10])
        for (score, shape) in shape_score_5:
            IF score > max_score_shape[0] AND shape_tmp = shape:
                max_score_shape <- (
                    score, (coord[6], coord[7], coord[8], coord[9], coord[10]),
                    (x_direction, y_direction))
            ENDIF
        ENDFOR
        add_score <- 0
        IF max_score_shape[1] is not None:
            for shape in curr_score_arr:
                for pt1 in shape[1]:
                    for pt2 in max_score_shape[1]:
                        IF pt1 = pt2:
                            IF shape[0] >= 2000 AND max_score_shape[0] >= 2000:
                                add_score <- max(shape[0], max_score_shape[0])
                            ELSE:
                                add_score <- min(shape[0], max_score_shape[0])
                            ENDIF
                            break
                        ENDIF
                    ELSE:
                        continue
                    ENDFOR
                    break
            ENDFOR
                ENDFOR
            curr_score_arr.append(max_score_shape)
        ENDIF
        RETURN add_score + max_score_shape[0]
    ENDFUNCTION

    for x in range(0,  chessboard_size):
        for y in range(0,  chessboard_size):
            IF chessboard[x][y] = color:
                for i in range(4):
                    my_score += cal_score(x, y, direction[i][0], direction[i][1], score_all_arr,
                                          color)
                ENDFOR
            ELSEIF chessboard[x][y] = -color:
                for i in range(4):
                    enemy_score += cal_score(x, y, direction[i][0], direction[i][1],
                                             score_all_arr_enemy, -color)
            ENDIF
    ENDFOR
        ENDFOR
                ENDFOR
    total_score <- my_score -  defence_factor * enemy_score
                                  ENDFUNCTION

    RETURN total_scOR
