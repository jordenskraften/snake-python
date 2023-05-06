import pygame
import sys 
from enum import Enum

class MovementDirection(Enum):
    UP = 0 
    LEFT = 1
    DOWN = 2
    RIGHT = 3
class KeyboardHandler:
    def __init__(self, snake):
        self.keys = set()
        self.snake = snake

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != MovementDirection.DOWN:
                    self.snake.change_to = MovementDirection.UP
                elif event.key == pygame.K_DOWN and self.snake.direction != MovementDirection.UP:
                    self.snake.change_to = MovementDirection.DOWN
                elif event.key == pygame.K_LEFT and self.snake.direction != MovementDirection.RIGHT:
                    self.snake.change_to = MovementDirection.LEFT
                elif event.key == pygame.K_RIGHT and self.snake.direction != MovementDirection.LEFT:
                    self.snake.change_to = MovementDirection.RIGHT
 
