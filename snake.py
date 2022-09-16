# sSnake - Equipo #1

from collections import deque as dq
import random as rn
import pygame as pg

pg.init()
score = 0
running = True
screen = pg.display.set_mode((800,800))
direction = "up"
board = [[0 for j in range(13)] for i in range(13)]
snake = dq([(6,6), (7,6), (8,6)])
for i in snake:
  board[i[0]][i[1]]=2

def updateBoard(coord,value):
    if(coord[0]>12 or coord[0]<0 or coord[1]>12 or coord[1]<0):
        return False
    board[coord[0]][coord[1]]=value
    return True

def fruitGeneration():
  i = rn.randint(0,12)
  j = rn.randint(0,12)
  if board[i][j]!=0:
    return fruitGeneration()
  coord = (i,j)
  board[i][j]=1
  return coord

def changeDir(currentDir, newDir):
    if currentDir=="up":
        if(newDir=="left" or newDir=="right" or newDir=="up"):
            return(newDir)
    elif currentDir=="right":
        if(newDir=="down" or newDir=="right" or newDir=="up"):
            return(newDir)
    elif currentDir=="down":
        if(newDir=="left" or newDir=="right" or newDir=="down"):
            return(newDir)
    elif currentDir=="left":
        if(newDir=="left" or newDir=="down" or newDir=="up"):
            return(newDir)
    return(currentDir)

def eatFruit(coord):
    score+=1
    board[coord[0]][coord[1]] = 2
    return fruitGeneration(board)

def moveSnake():
    if(direction=="up"):
        newCoord = (snake[0][0]-1, snake[0][1])
        deleted = snake.pop()
        if(updateBoard(newCoord,2)):
            updateBoard(deleted,0)        
            snake.appendleft(newCoord)
        else:
            return False
    elif(direction=="down"):
        newCoord = (snake[0][0]+1, snake[0][1])
        deleted = snake.pop()
        if(updateBoard(newCoord,2)):
            updateBoard(deleted,0)        
            snake.appendleft(newCoord)
        else:
            return False
    elif(direction=="right"):
        newCoord = (snake[0][0],  snake[0][1]+1)
        deleted = snake.pop()
        if(updateBoard(newCoord,2)):
            updateBoard(deleted,0)        
            snake.appendleft(newCoord)
        else:
            return False
    elif(direction=="left"):
        newCoord = (snake[0][0],  snake[0][1]-1)
        deleted = snake.pop()
        if(updateBoard(newCoord,2)):
            updateBoard(deleted,0)        
            snake.appendleft(newCoord)
        else:
            return False
    return True
       
fruit = fruitGeneration()
print(board)
while running:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT or event.key == pg.K_a:
                direction = changeDir(direction, "left")
            elif event.key == pg.K_UP or event.key == pg.K_w:
                direction = changeDir(direction, "up")
            elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                direction = changeDir(direction, "right")
            elif event.key == pg.K_DOWN or event.key == pg.K_s:
                direction = changeDir(direction, "down")
            if(not moveSnake()):
                running=False
            print(board)    
        if event.type == pg.QUIT:
            running = False
pg.quit()
