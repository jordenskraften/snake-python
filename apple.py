import pygame 

class Apple:
    def __init__(self, x, y):
        self.x = x
        self.y = y 

    def death(self, snake):
        pass
        #каждый фрейм проверяем не равно ли координаты голове змейки
        #если равно знач коснулись, змейку дергаем чтоб выросла
        #яблоко убиваем и респавним
        self.respawn()
        snake.growth()
 
    def respawn():
        pass
 
    def render(surface, apple, SIZE):
        pygame.draw.rect(surface, pygame.Color('red'), (*apple, SIZE, SIZE))