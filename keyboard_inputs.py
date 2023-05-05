import pygame
import sys

class KeyboardHandler:
    def __init__(self, snake):
        self.keys = set()
        self.snake = snake

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != "DOWN":
                    self.snake.change_to = "UP"
                elif event.key == pygame.K_DOWN and self.snake.direction != "UP":
                    self.snake.change_to = "DOWN"
                elif event.key == pygame.K_LEFT and self.snake.direction != "RIGHT":
                    self.snake.change_to = "LEFT"
                elif event.key == pygame.K_RIGHT and self.snake.direction != "LEFT":
                    self.snake.change_to = "RIGHT"
 
