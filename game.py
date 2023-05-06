import pygame
from snake import Snake
from food import Food
from renderer import Renderer
from keyboard_inputs import KeyboardHandler
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game") 
        self.surface = pygame.display.set_mode((720, 460)) 
        self.snake = Snake(self.surface) 
        self.food = Food(self.snake.snake_body)
        self.score = 0
        self.clock = pygame.time.Clock()
        self.keyboard = KeyboardHandler(self.snake)
        self.renderer = Renderer(self.surface, self.snake, self.food)

    def play(self):
        game_over = False
        while not game_over:

            self.surface.fill((0,0,0))  

            events = pygame.event.get()
            self.keyboard.handle_events(events)
 

            self.snake.validate_direction_and_change()
            self.snake.change_head_position()
            self.score = self.snake.snake_body_mechanism(
                self.score, self.food)

            self.renderer.draw_game_objects(self.score)
            
            game_over, self.score = self.snake.check_for_boundaries(game_over, self.score)
            game_over, self.score = self.snake.check_for_self_body_collision(game_over, self.score)
            
            # Установка максимальной частоты кадров (60 fps)
            self.clock.tick(10) 

            pygame.display.flip()
        pygame.quit()
        quit()
 
