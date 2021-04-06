import numpy
import requests

def checkPlacement(row, column, number):
    global board
    for x in range(9):
        if board[x][column] == number or board[row][x] == number:
            return False
    for y in range(row//3*3,row//3*3+3):
        for z in range(column//3*3,column//3*3+3):
            if board[y][z] == number:
                
                return False
                
    return True

def solveBoard():
    global board
    for row in range(9):
        for column in range(9):
            if board[row][column] == 0:
                for number in range(1,10):
                    if checkPlacement(row, column, number):
                        board[row][column] = number
                        solveBoard()
                        board[row][column] = 0
                return
    print(numpy.matrix(board))
    print("\n")

response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
board = response.json()['board']
print("Not solved board:")
print(numpy.matrix(board))
print(" \n Solved board (or boards if more than one exist)")
solveBoard()