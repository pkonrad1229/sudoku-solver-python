import pygame
import requests


class Board:

    def __init__(self, width, height, win):
        self.width = width
        self.height = height
        self.selected = None
        self.win = win
        self.solving = False
        self.newBoard()

    def newBoard(self):
        response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
        self.model = response.json()['board']

    def click(self, xPosition, yPosition):
        
        if xPosition < self.width and yPosition < self.height:
            blockSize = self.width / 9
            x = xPosition // blockSize
            y = yPosition // blockSize
            self.selected = (int(y), int(x))
            return (int(y),int(x))
        else:
            return None

    def clear(self):
        row, column = self.selected
        self.model[row][column] = 0
        
    def place(self, value):
        row, column = self.selected
        if self.checkPlacement(row, column, value):
            self.model[row][column] = value
            return True
        else:
            return False
    def printBoard(self):
        blockSize = self.width / 9

        for i in range(10):
            if i%3==0:
                thickness = 4
            else:
                thickness = 1
            pygame.draw.line(self.win, (0,0,0), (0, i*blockSize), (self.width, i*blockSize), thickness)
            pygame.draw.line(self.win, (0,0,0), (i*blockSize, 0), (i*blockSize, self.height), thickness)
    
    def printValues(self):
        blockSize = self.width / 9
        fnt = pygame.font.SysFont('Comic Sans MS', 35)

        for row in range(9):
            for column in range(9):
                y = row * blockSize
                x = column * blockSize
                if self.model[row][column] != 0:
                    text = fnt.render(str(self.model[row][column]), 1, (0, 0, 0))
                    self.win.blit(text, (x + (blockSize/2 - text.get_width()/2), y + (blockSize/2 - text.get_height()/2)))
                if self.selected:
                    if row == self.selected[0] and column == self.selected[1]:
                        pygame.draw.rect(self.win, (255,0,0), (x,y, blockSize ,blockSize), 3)

    def printChange(self, row, column, value, wrong=False):
        fnt = pygame.font.SysFont('Comic Sans MS', 35)
        blockSize = self.width / 9
        x = column * blockSize
        y = row * blockSize
        pygame.draw.rect(self.win, (255, 255, 255), (x, y, blockSize, blockSize), 0)

        text = fnt.render(str(value), 1, (0, 0, 0))
        self.win.blit(text, (x + (blockSize / 2 - text.get_width() / 2), y + (blockSize / 2 - text.get_height() / 2)))

        if wrong:
            pygame.draw.rect(self.win, (255, 0, 0), (x, y, blockSize, blockSize), 3)
        else:
            pygame.draw.rect(self.win, (0, 255, 0), (x, y, blockSize, blockSize), 3)


    def isFinished(self):
        for row in range(9):
            for column in range(9):
                if self.model[row][column] == 0:
                    return False
        return True

    def solve(self):

        if self.isFinished():
            return True
        self.so = True
        for row in range(9):
            for column in range(9):
                if self.model[row][column] == 0:
                    for number in range(1,10):
                        if self.checkPlacement(row, column, number):
                            self.model[row][column] = number
                            self.printChange(row,column,number,False)
                            pygame.display.update()
                            pygame.time.delay(50)
                            if self.solve():
                                self.solving = False
                                return True
                            self.model[row][column] = 0
                            self.printChange(row,column,0,True)
                            pygame.display.update()
                            pygame.time.delay(50)
                    return
        return False

    def checkPlacement(self, row, column, value):
        for x in range(9):
            if self.model[x][column] == value or self.model[row][x] == value:
                return False
        for y in range(row//3*3,row//3*3+3):
            for z in range(column//3*3,column//3*3+3):
                if self.model[y][z] == value:
                    return False
        return True

def updateWindow(board, win):
    win.fill((255,255,255))
    board.printBoard()
    board.printValues()


def main():
    pygame.init()
    win = pygame.display.set_mode((540,540))
    win.fill((251, 247, 245))
    pygame.display.set_caption("Sudoku")
    board = Board(540, 540, win)
    play = True
    clock = pygame.time.Clock()

    while play:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_n:
                    board.newBoard()

                if event.key == pygame.K_SPACE:
                    key = None
                    board.solve()
            if not board.solving: # test

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    clicked = board.click(pos[0], pos[1])
                    if clicked:
                        key = None

                if board.selected and key != None:
                    board.place(key)

        updateWindow(board, win)
        pygame.display.update()

main()
pygame.quit()