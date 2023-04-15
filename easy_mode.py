import numpy as np
import pygame
import sys
import math
import random

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

row_count = 6
col_count = 7

player = 0
ai = 1

empty = 0
playerPiece = 1
aiPiece = 2

windowLength = 4
def Board():
    #function that creates specific dimension of the board
    board = np.zeros((row_count,col_count))
    return board

def Drop(board , row, column, piece):
#function that will replace an empty space with a piece
    board[row][column] = piece

def validLocation(board, column):
#function that determines whether the spot chosen is allowed to be filled
    return board[row_count-1][column]==0

def nextOpenRow(board,column):
#function that determines what rows are available to be filled with a piece
    for row in range(row_count):
        if board[row][column]==0:
            return row

def printBoard(board):
#prints the updated board
    print(np.flip(board,0))

def winCondition(board, piece):
    #function to determine if a player has won
    #part of the function that determines if there is a vertical location for a win
    for column in range(col_count-3):
        for row in range(row_count):
            if board[row][column] == piece and board[row][column+1] == piece and board[row][column+2] == piece and board[row][column+3] == piece:
                return True
    #check for vertical win
    for column in range(col_count):
        for row in range(row_count-3):
            if board[row][column] == piece and board[row+1][column] == piece and board[row+2][column] == piece and board[row+3][column] == piece:
                return True
    #check for increasing slope win
    for column in range(col_count-3):
        for row in range(row_count-3):
            if board[row][column] == piece and board[row+1][column+1] == piece and board[row+2][column+2] == piece and board[row+3][column+3] == piece:
                return True
    #check for decreasing slope win
    for column in range(col_count-3):
        for row in range(3,row_count):
            if board[row][column] == piece and board[row-1][column+1] == piece and board[row-2][column+2] == piece and board[row-3][column+3] == piece:
                return True
def evaluateBoard(window,piece):
    #this function evalusates the board by stopping the user if the specifically have three in a row
    score = 0
    opp_piece = playerPiece
    if piece == playerPiece:
        opp_piece = aiPiece

    if window.count(piece) == 4:
        score += 100
    if window.count(opp_piece) == 3 and window.count(piece) == 1:
        score += 50
    elif window.count(piece) == 3 and window.count(empty) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(empty) == 2:
        score += 5

    return score
def scorePosition(board, piece):
    #this function allows the ai to focus the center of the board
    score = 0
    falsescore = 0

    # Score center column
    centerArray = [int(i) for i in list(board[:, col_count // 2])]
    centerCount = centerArray.count(piece)
    score += centerCount * 3

    ## Score Horizontal
    for row in range(row_count):
        row_array = [int(i) for i in list(board[row, :])]
        for column in range(col_count - 3):
            window = row_array[column:column + windowLength]
            score += evaluateBoard(window, piece)

    # Score Vertical
    for column in range(col_count):
        col_array = [int(i) for i in list(board[:, column])]
        for row in range(row_count - 3):
            window = col_array[row:row + windowLength]
            falsescore += evaluateBoard(window, piece)

    if falsescore > score:
        return falsescore
    else:
        return score
def terminalNode(board):
    return winCondition(board,playerPiece) or winCondition(board,aiPiece) or len(getValidLocation(board)) ==0
def getValidLocation(board):#determins valid spots ai can take
    validLocations = []
    for column in range(col_count):
        if validLocation(board,column):
            validLocations.append(column)
    return validLocations
def bestMove(board,piece):#simple determines what is the best move for AI to take
    validLocations = getValidLocation(board)
    bestScore = 1000
    bestColumn = random.choice(validLocations)
    for column in validLocations:
        row = nextOpenRow(board,column)
        tempBoard = board.copy()
        Drop(tempBoard,row,column,piece)
        score = scorePosition(tempBoard,piece)
        if score > bestScore:
            bestScore = score
            bestColumn = column
    return bestColumn
def drawBoard(board):
    for column in range(col_count):
        for row in range(row_count):
            pygame.draw.rect(screen,YELLOW,(column*square,row*square+square,square,square))
            pygame.draw.circle(screen, BLACK, (int(column*square+square/2),int(row*square+square+square/2)),radius)

    for column in range(col_count):
        for row in range(row_count):
            if board[row][column] ==1:
                pygame.draw.circle(screen,RED,(int(column*square+square/2),height-int(row*square+square/2)),radius)
            elif board[row][column] ==2:
                pygame.draw.circle(screen,BLUE,(int(column*square+square/2),height-int(row*square+square/2)),radius)
    pygame.display.update()
board = Board()
print(board)
gameOver=False
turn = 0

pygame.init()
square = 100
width = col_count*square
height = (row_count+1)*square
size = (width,height)
radius=int(square/2-5)
screen = pygame.display.set_mode(size)
drawBoard(board)
pygame.display.update()
myFont = pygame.font.SysFont("monospace",75)

while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
         sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, square))
            posx = event.pos[0]
            if turn == player:
                pygame.draw.circle(screen, RED, (posx, int(square / 2)), radius)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen,BLACK,(0,0,width,square))
            #player 1 input
            if turn == 0:
                posx = event.pos[0]
                column = int(math.floor(posx/square))

                if validLocation(board,column):
                    row = nextOpenRow(board,column)
                    Drop(board,row,column,1)

                    if winCondition(board,1):
                        label= myFont.render("Player 1 wins",1,RED)
                        screen.blit(label,(40,10))
                        gameOver = True
                    turn += 1
                    turn = turn % 2
                    printBoard(board)
                    drawBoard(board)
            if turn == ai and not gameOver:
                # allows the ai to place pieces and sees when their win condition is me
                column = bestMove(board,aiPiece)
                if validLocation(board, column):
                    row = nextOpenRow(board, column)
                    Drop(board, row, column, aiPiece)

                    if winCondition(board, aiPiece):
                        label = myFont.render("Player 2 wins", 1, BLUE)
                        screen.blit(label, (40, 10))
                        gameOver = True
                    printBoard(board)
                    drawBoard(board)

                    turn += 1
                    turn = turn % 2
            if gameOver:
                pygame.time.wait(3000)