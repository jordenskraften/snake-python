import pygame 
from random import randrange 
 
pygame.init()
pygame.display.set_caption("Snake Game")
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
  
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
 
    screen.fill((255, 255, 255))
    pygame.display.update()
    clock.tick(60)
