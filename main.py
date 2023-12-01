import random
import sys
import pygame

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (200, 0, 0)
GREEN = (0, 200, 0)

WINDOW_HEIGHT = 375
WINDOW_WIDTH = 1180
XBLOCKS = 41
YBLOCKS = 12
blockSize = 28

MAXSCORE = -100   #IT IS DEADROCKET-PASSEDROCKET
DEADROCKET = 0
PASSEDROCKET = 0

rocketImg = pygame.image.load("rocket.png")
wallImg = pygame.image.load("wall.png")

class Ball:
    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.health = health

    def drawself(self):
        SCREEN.blit(rocketImg, (self.x * blockSize, self.y * blockSize))
    def startOver(self):
        self.health = 100
        self.y = random.randint(1, 10)
        self.x = 0
    def move(self):
        moveRandom = random.randint(0, 4) # MOVE RANDOMLY %25UP %25DOWN %50FORWARD
        self.health -= 1 #LOSE 1 HEALTH ON EVERY MOVE
        match moveRandom:
            case 0:
                self.x += 1
                return
            case 1:
                self.y += 1
                if (self.y >= YBLOCKS - 1): #IF IT HITS UPPERBOUND
                    self.startOver()
                return
            case 2:
                self.y -= 1
                if (self.y == 0): #IF IT HITS LOWERBOUND
                    self.startOver()
                return
            case 3:
                self.x += 1
                return



def main():
    global SCREEN, CLOCK
    global DEADROCKET, PASSEDROCKET,MAXSCORE
    DEADROCKET = 0
    PASSEDROCKET = 0
    finalDeadRocket = 0 #JUST FOR THE PRINTING AT THE END
    finalPassedRocket = 0 #SAME
    TRYAMOUNT=1000 # BRUTE FORCE TRY AMOUNT
    bestWallList=[]

    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)
    ballList = []
    wallList = []

    #createWalls(wallList)
    #createBalls(ballList)
    time_counter = 0
    score=0
    desiredScore=35
    while True:
        SCREEN.fill(BLACK)
        drawGrid()
        #DRAW WALLS
        for wall in wallList:
            SCREEN.blit(wallImg, (wall[0] * blockSize, wall[1] * blockSize))
        #DRAW BALLS
        for ball in ballList:
            if (ball.health >= 0): #CHECK BALL HEALTH BEFORE DRAW
                ball.drawself()
            else:
                DEADROCKET += 1
                #print("dead rocket number ", DEADROCKET)
                ballList.remove(ball)
        time_counter += CLOCK.tick()
        #MOVE AND CHECK FOR COLLİSİON EVERY X TICKS (MADE IT FOR BETTER VISUALIZATION)
        if time_counter > 0:
            for ball in ballList:
                ball.move()
                if (ball.x >= 40):
                    PASSEDROCKET += 1
                    #print("ball passed", PASSEDROCKET)
                    #print(ball.health)
                    ballList.remove(ball)
                for wall in wallList:
                    if ball.x == wall[0] and ball.y == wall[1]:
                        ball.health -= 2   # -1 ALREADY COMES FROM MOVING SO JUST MINUS 2
            time_counter = 0
        #IF THERE IS NO BALLS LEFT START OVER
        if not ballList and score<desiredScore:
            score=DEADROCKET-PASSEDROCKET
            print(score)
            if(score>MAXSCORE):
                bestWallList=wallList
                MAXSCORE=score
                finalDeadRocket=DEADROCKET
                finalPassedRocket = PASSEDROCKET
            DEADROCKET=0
            PASSEDROCKET=0
            wallList.clear()
            createWalls(wallList)
            createBalls(ballList)
        #PRINT RESULT
        elif score>=desiredScore:
            print("final dead rocket: ", finalDeadRocket," final passed rocket: ", finalPassedRocket)
            print(MAXSCORE)
            print(bestWallList)
            pygame.time.wait(50000)
            sys.exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

def createWalls(wallist):
    for x in range(4):
        for y in range(4):
            wallist.append([x*10+(random.randint(0,9)), (random.randint(1, 10))])
def createBalls(ballist):
    for x in range(100):
        ball = Ball(0, random.randint(1, 10), 100)
        ballist.append(ball)

def drawGrid():
    for x in range(0, XBLOCKS):
        for y in range(0, YBLOCKS):
            rect = pygame.Rect(x * blockSize, y * blockSize, blockSize, blockSize)
            if (x == 40):
                pygame.draw.rect(SCREEN, GREEN, rect, 1)
            elif (y == 0 or y == 11):
                pygame.draw.rect(SCREEN, RED, rect, 1)
            else:
                pygame.draw.rect(SCREEN, WHITE, rect, 1)


if __name__ == '__main__':
    main()