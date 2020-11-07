# Prog-11: Tetris
# Fill in your ID & Name
# ...
# Declare that you do this by yourself

import pygame
import copy
import random


def make_shape():
    shape = [[[1, 1, 1], [1, 0, 0]], [[2, 2, 2], [0, 0, 2]], [[3, 3, 3], [0, 3, 0]], [
        [4, 4, 4, 4]], [[5, 5, 0], [0, 5, 5]], [[6, 0], [6, 6], [0, 6]], [[7, 7], [7, 7]]]
    return shape[random.randrange(len(shape))]


def show_text(x, y, size, text, screen):
    text_surface = pygame.font.Font(pygame.font.match_font(
        'arial'), size).render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


def top(board):
    row = min([i for i in range(len(board)) if board[i]
               != [0]*len(board[0])], default=0)-1
    return 60*(2+(row-1)//6) if row > 6 else 120


def scoring(board):
    count = len([i for i in board if 0 not in i])
    return 50*count*(count-1)*max(1, (count-2)) if count > 1 else 40*count


def pgame():
    width, height, FPS = 480, 720, 60
    all_color = [(255, 128, 0), (0, 0, 255), (255, 0, 255),
                 (0, 255, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0)]
    board = [[0]*10 for i in range(23)]
    shape = make_shape()
    score, time, end, column = 0, 0, 0, 0
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("ComProg-10: Tetris")

    while end == 0:
        screen.fill((0, 0, 0))
        time_cap = top(board)
        clock.tick(FPS)
        frame = [board]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    frame = animate_drop(shape, board, column)
                    if len(frame) != 0:
                        score += scoring(frame[-1])
                        frame = frame + animate_clear(frame[-1])
                        board = frame[-1]
                        shape = make_shape()
                        column, time = 0, 0
                    else:
                        end = 1
                elif event.key == pygame.K_LEFT:
                    column = column-1 if column > 0 else column
                elif event.key == pygame.K_RIGHT:
                    column = column + \
                        1 if column < len(board[0])-len(shape[0]) else column
                elif event.key == pygame.K_z:
                    shape = rotateL(shape)
                    column = min(column, len(board[0])-len(shape[0]))
                elif event.key == pygame.K_x:
                    shape = rotateR(shape)
                    column = min(column, len(board[0])-len(shape[0]))
        time += 1
        if time >= time_cap:
            frame = animate_drop(shape, board, column)
            if len(frame) != 0:
                score += scoring(frame[-1])
                frame = frame + animate_clear(frame[-1])
                board = frame[-1]
                shape = make_shape()
                column, time = 0, 0
            else:
                end = 1
        for i in frame:
            screen.fill((0, 0, 0))
            clock.tick(FPS)
            board_row, board_column = len(i), len(i[0])
            shape_row, shape_column = len(shape), len(shape[0])
            for j in range(shape_row):
                for k in range(shape_column):
                    if shape[j][k] != 0:
                        pygame.draw.rect(
                            screen, all_color[shape[j][k]-1], [30+column*24+k*24, 20+j*24, 20, 20], 0)
            for j in range(board_row):
                for k in range(board_column):
                    if i[j][k] != 0:
                        pygame.draw.rect(
                            screen, all_color[i[j][k]-1], [30+k*24, 124+j*24, 20, 20], 0)
            for i in range(board_column+1):
                if i >= column and i <= column + shape_column:
                    pygame.draw.line(screen, (255, 255, 255), [
                                     28+i*24, 672], [28+i*24, 116], 3)
                else:
                    pygame.draw.line(screen, (128, 128, 128), [
                                     28+i*24, 672], [28+i*24, 116])
            show_text(380, 120, 50, "TIME", screen)
            show_text(380, 500, 50, "SCORE", screen)
            show_text(
                240, 685, 15, "Z/X for rotating      Right/Left Arrow Key for moving      Spacebar for dropping", screen)
            pygame.display.flip()
        show_text(380, 180, 150, str(time//60)+"."+str((time//6) % 10), screen)
        show_text(380, 550, 75, str(score), screen)
        pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.quit()
                    return
        screen.fill((0, 0, 0))
        show_text(240, 150, 50, "TOTAL SCORE", screen)
        show_text(240, 250, 250, str(score), screen)
        show_text(240, 550, 25, "press enter to exit the game", screen)
        pygame.display.flip()

# -------------------------------------------------------


def findInList(list, platform):
    for i in range(len(list)):
        if list[i] == platform:
            return True
    return False


def rotateR(shape):
    cols = len(shape[0])
    return [[m[i] for m in reversed(shape)] for i in range(cols)]


def rotateL(shape):
    newgrid = list(map(list, zip(*shape)))[::-1]
    return newgrid


def animate_drop(shape, board, c):
    # print("shape :",shape)
    print("board :", board)
    # print("c :",c)

    n = len(board)
    m = len(board[0])
    # ! 4 - 1 = 3

    # for i in range(1):
    #     lenSS = len(shape[i])
    #     for j in range(lenSS):
    #         new_board[0][0, 1, 2, 3] = shape[i][j]
    #         print(shape[i][j])
    stack_board = []

    if(c != 0):
        for a in range(len(board)):
            if (board[a][c] != 0):
                break
            print("round ------------ ", a+1)
            new_board = [[x for x in y] for y in board]
            # ? 3

            # check_em = []
            for k in range(len(shape)):
                for q in range(len(shape[0])):
                    if ((k+a+1) < n and shape[k][q] != 0 and new_board[k+a+1][q+c] != 0):
                        for i in range(len(shape)):
                            for j in range(len(shape[0])):
                                if(shape[i][j] != 0):
                                    new_board[a+i][j+c] = shape[i][j]
                        print("new_board :", new_board)
                        stack_board.append(new_board)
                        return stack_board

            # ? c = 1
            for i in range(len(shape)):
                for j in range(len(shape[0])):
                    if(shape[i][j] != 0):
                        try:
                            new_board[a+i][j+c] = shape[i][j]
                        except:
                            return stack_board

            print("new_board :", new_board)
            stack_board.append(new_board)
        return stack_board
    else:
        return []


def addValueToList(elem, count):
    temp = []
    for i in range(count):
        temp.append(elem)
    return temp


def checkAllClear(listTemp):
    for i in range(len(listTemp)-1):
        if(listTemp[i] == 1 and listTemp[i+1] == 0):
            return False
    return True


def checkPosition(board):
    countCheck = []
    for i in range(len(board)):
        if(all(elem == 0 for elem in board[i])):
            countCheck.append(0)
        else:
            countCheck.append(1)
    return countCheck


def wtfIsGoingOn(temp):
    print(temp)


def animate_clear(board):
    n = len(board)
    listCheckFull = []
    countCheck = 0
    temp_board = board
    # ! ลบแถวที่เต็มออก
    for i in range(n):
        if(all(elem != 0 for elem in board[i])):
            countCheck += 1
            for j in range(len(board[i])):
                temp_board[i][j] = 0
    # ! เลื่อนแถว
    listCheckFull = checkPosition(temp_board)
    stackBoard = []
    if (countCheck == 0):
        return []
    else:
        fisrtRound = True
        while(True):
            if (fisrtRound):
                new_board = temp_board
                stackBoard.append(new_board[:])
                countCheckSlide = listCheckFull
                fisrtRound = False
            for i in range(len(temp_board)-1):
                if (countCheckSlide[i] == 1 and countCheckSlide[i+1] == 0):
                    new_board[i+1] = new_board[i]
                    new_board[i] = addValueToList(0, len(new_board[i]))
            countCheckSlide = checkPosition(new_board)
            stackBoard.append(new_board[:])
            if(checkAllClear(countCheckSlide)):
                return stackBoard


# ----------------------------------------------
# board_test = [[0, 0, 0, 0, 0],
#               [2, 0, 0, 0, 0],
#               [2, 3, 3, 4, 4]]
# check = [
#     [[3, 3, 0, 0], [0, 0, 0, 0], [0, 5, 5, 4], [0, 0, 0, 0], [0, 0, 0, 0], [4, 0, 1, 1]],
#     [[0, 0, 0, 0], [3, 3, 0, 0], [0, 0, 0, 0], [0, 5, 5, 4], [0, 0, 0, 0], [4, 0, 1, 1]],
#     [[0, 0, 0, 0], [0, 0, 0, 0], [3, 3, 0, 0], [0, 0, 0, 0], [0, 5, 5, 4], [4, 0, 1, 1]],
#     [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [3, 3, 0, 0], [0, 5, 5, 4], [4, 0, 1, 1]]]
# checkTemp = [1, 0, 1, 0, 0, 1]
# checkTemp = [0, 0, 1, 1, 1, 1]
# print(checkAllClear(checkTemp))
# shape_test = [[1,1,1], [0,1,0]]
# shape_test = [[1,2,3,4]]
# print(rotateR(shape_test))
# print(rotateL(shape_test))
# print(animate_clear(board_test))
# print(animate_drop(shape_test, board_test, c_test))
# pgame()
