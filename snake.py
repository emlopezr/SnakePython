# Snake - Equipo #1
#Integrantes: Maria Paula Duque
#             Andrés Felipe Aparicio
#             Emmanuel López

from collections import deque as dq  #La estructura de datos principal que se usó. También era posible usar arreglos de redimensionamiento dinámico.
import random as rn #Librería para la posición de la fruta
import pygame as pg #Librería para la parte visual del juego. Ejecución continua del juego por frames

#Se trabajaron utilizando programación orientada a objetos

class Snake:     
    def __init__(self):    
        self.body = dq([(6,6), (6,7), (6,8)]) #El cuerpo de la serpiente
        self.direction = "up"  #Dirección
        self.grow = False   #Variable de control para indicar que la serpiente crece al comer
        self.score = 0  #La puntuación
    
    def changeDir(self, newDir):    #Se debe verificar que la nueva dirección de la serpiente sea válida. Se ejecuta cada vez que el usuario use una tecla
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

    def eatApple(self,apple):     #Se verifica que en la ´cima´ de la cola (cabeza serpiente) tenga la misma posición que la manzana.
                                    # Si sí, se genera una nueva manzana y hace que la serpiente crezca en el póximo movimiento
        if(self.body[0] == apple.coord):
            apple.generate()
            self.grow = True
            return True
        return False

    def draw(self):  #Muestra en pantalla la serpiente
        for block in self.body:
            pg.draw.rect(WIN,(0,255,0),(block[0]*GRIDSIZE,block[1]*GRIDSIZE,GRIDSIZE,GRIDSIZE))
           

    def moveSnake(self):  #Por cada tick se ejecuta el método. Según la dirección en la que vaya, modifica las coordenadas
        if(self.direction=="up"):
            newCoord = (self.body[0][0], self.body[0][1]-1)      
        elif(self.direction=="down"):
            newCoord = (self.body[0][0], self.body[0][1]+1)
        elif(self.direction=="right"):
            newCoord = (self.body[0][0]+1,  self.body[0][1])
        elif(self.direction=="left"):
            newCoord = (self.body[0][0]-1,  self.body[0][1])
        self.body.appendleft(newCoord)
        if (not self.grow):   #Al comer, no se debe quitar el ultimo elemento referente al movimiento
            self.body.pop()
        else:
            self.grow = False
            
    def reset(self, apple):  #Reiniciar todo a las condiciones iniciales, generando una nueva manzana
        self.body = dq([(6,6), (6,7), (6,8)])
        self.direction = "up"
        self.grow = False
        self.score = 0
        apple.reset()

    def die(self):      
        if self.body[0][0] > 12 or self.body[0][1] > 12 or self.body[0][0] <0  or self.body[0][1] < 0:  #Si la cabeza (en cualquier eje de coordenadas) es mayor que 12, muere la serpiente
            return True

        for i in range(1, len(self.body)):  #Si la cabeza tiene las mismas coordenadas que alguna otra parte del cuerpo, muere la serpiente
            if self.body[0] == self.body[i]:
                return True

class Apple:   
    def __init__(self, snake): #Genera una manzana en una coordenada especifica al inicio
        self.snake = snake
        self.coord=(10,2)
    
    def draw(self):
        pg.draw.rect(WIN,(255,0,0),(self.coord[0]*GRIDSIZE,self.coord[1]*GRIDSIZE,GRIDSIZE,GRIDSIZE)) #Muestra la manzana en pantalla

    def generate(self):  #Genera la manzana en una posición aleatoria cada vez
        self.x = rn.randint(0,12)
        self.y = rn.randint(0,12)
        self.coord = (self.x,self.y)
        if self.coord in self.snake.body:
                self.generate()
    def reset(self):
        self.coord=(10,2)

pg.init()        #Variables globales para inicializar
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

    while running:  #Mientras se ejecuta el juego
        clock.tick(8) #Controla la velocidad del juego
        for event in pg.event.get(): #La librería capta los eventos de teclado y cambia la dirección de la serpiente
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

        if(snake.die()):  #Si la serpiente muere, reset
            snake.reset(apple)

        if(snake.eatApple(apple)):  #Aumenta la puntuación si se come una manzana
            snake.score+=1
        
        text = SCORE_TEXT.render("Score: {0}".format(snake.score),1,(255,255,255))
        WIN.blit(text,(WIDTH-text.get_width()-10,10))
        pg.display.update()
        
main()





