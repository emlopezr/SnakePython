# sSnake - Equipo #1

from collections import deque as dq
import random as rn
import pygame as pg



class Snake:
    def __init__(self):
        self.body = dq([(6,6), (6,7), (6,8)])
        self.direction = "up"
        self.grow = False
        self.score = 0
    
    def changeDir(self, newDir):
        if self.direction=="up":
            if(newDir=="left" or newDir=="right" or newDir=="up"):
                self.direction=newDir
        elif self.direction=="right":
            if(newDir=="down" or newDir=="right" or newDir=="up"):
                self.direction=newDir
        elif self.direction=="down":
            if(newDir=="left" or newDir=="right" or newDir=="down"):
                self.direction=newDir
        elif self.direction=="left":
            if(newDir=="left" or newDir=="down" or newDir=="up"):
                self.direction=newDir

    def eatApple(self,apple):
        if(self.body[0] == apple.coord):
            apple.generate()
            self.grow = True
            return True
        return False

    def draw(self):
        for block in self.body:
            pg.draw.rect(WIN,(0,255,0),(block[0]*GRIDSIZE,block[1]*GRIDSIZE,GRIDSIZE,GRIDSIZE))
           

    def moveSnake(self):
        if(self.direction=="up"):
            newCoord = (self.body[0][0], self.body[0][1]-1)
           
        elif(self.direction=="down"):
            newCoord = (self.body[0][0], self.body[0][1]+1)
            
        elif(self.direction=="right"):
            newCoord = (self.body[0][0]+1,  self.body[0][1])
           
        elif(self.direction=="left"):
            newCoord = (self.body[0][0]-1,  self.body[0][1])

        self.body.appendleft(newCoord)
        if (not self.grow):
            self.body.pop()
        else:
            self.grow = False
            
    def reset(self, apple):
        self.body = dq([(6,6), (6,7), (6,8)])
        self.direction = "up"
        self.grow = False
        self.score = 0
        apple.generate()

    def die(self):
        if self.body[0][0] > 12 or self.body[0][1] > 12 or self.body[0][0] <0  or self.body[0][1] < 0:
            return True

        for i in range(1, len(self.body)):
            if self.body[0] == self.body[i]:
                return True

class Apple:
    def __init__(self, snake):
        self.snake = snake
        self.generate()
        
    
    def draw(self):
        pg.draw.rect(WIN,(255,0,0),(self.coord[0]*GRIDSIZE,self.coord[1]*GRIDSIZE,GRIDSIZE,GRIDSIZE))

    def generate(self):
        self.x = rn.randint(0,12)
        self.y = rn.randint(0,12)
        self.coord = (self.x,self.y)
        if self.coord in self.snake.body:
                self.generate()

pg.init()      
HEIGHT = 480
WIDTH = 480
GRID_WIDTH = 13
GRID_HEIGHT = 13
GRIDSIZE = HEIGHT/GRID_WIDTH
WIN = pg.display.set_mode((WIDTH,HEIGHT))
SCORE_TEXT= pg.font.SysFont("Russo One", 25)

def main():
    
    snake = Snake()
    apple = Apple(snake)
    WIN = pg.display.set_mode((WIDTH,HEIGHT), 0, 32)
    running = True
    clock = pg.time.Clock()  

    while running:
        clock.tick(10)
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    snake.changeDir("left")
                elif event.key == pg.K_UP or event.key == pg.K_w:
                    snake.changeDir("up")
                elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                    snake.changeDir("right")
                elif event.key == pg.K_DOWN or event.key == pg.K_s:
                    snake.changeDir("down")
            if event.type == pg.QUIT:
                quit()
    
        WIN.fill((0,0,0))
        snake.draw()
        apple.draw()
        snake.moveSnake()

        if(snake.die()):
            snake.reset(apple)

        if(snake.eatApple(apple)):
            snake.score+=1
        
        text = SCORE_TEXT.render("Score: {0}".format(snake.score),1,(255,255,255))
        WIN.blit(text,(WIDTH-text.get_width()-10,10))
        pg.display.update()
        
main()





