import pygame
from snake import Snake
from food import Food
from keyboard_inputs import KeyboardHandler
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game") 
        self.surface = pygame.display.set_mode((720, 460))
        self.snake = Snake(self.surface)
        self.food = Food()
        self.score = 0
        self.clock = pygame.time.Clock()
        self.keyboard = KeyboardHandler(self.snake)

    def play(self):
        game_over = False
        while not game_over:

            self.surface.fill((0,0,0))  
            
            events = pygame.event.get()
            self.keyboard.handle_events(events)
 

            self.snake.validate_direction_and_change()
            self.snake.change_head_position()
            self.score, self.food.food_pos = self.snake.snake_body_mechanism(
                self.score, self.food.food_pos)
            self.snake.draw_snake()  

            self.food.draw_food(self.surface)
            self.score = self.display_score() 
            game_over, self.score = self.snake.check_for_boundaries(game_over, self.score)
            game_over, self.score = self.snake.check_for_self_body_collision(game_over, self.score)
            
            # Установка максимальной частоты кадров (60 fps)
            self.clock.tick(10) 

            pygame.display.flip()
        pygame.quit()
        quit()

    def display_score(self):
        font = pygame.font.SysFont('arial', 20)
        score = font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.surface.blit(score, (600, 10))
        return self.score
