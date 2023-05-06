import pygame
from snake import Snake
from food import Food
from renderer import Renderer
from keyboard_inputs import KeyboardHandler
from game_state import GameState


class SingleGameState(GameState):
    def __init__(self, context):   
        self.context = context
        self.WIDTH = self.context.WIDTH
        self.HEIGHT = self.context.HEIGHT
        self.surface = self.context.surface
        self.clock = self.context.clock 
        self.playable_area_rect = pygame.Rect(25, 50, self.WIDTH -50, self.HEIGHT-75)   
        self.snake = Snake(self.surface, self.playable_area_rect) 
        self.food = Food(self.snake.snake_body, self.playable_area_rect)
        self.score = 0 
        self.keyboard = KeyboardHandler(self.snake)
        self.renderer = Renderer(self.surface, self.snake, self.food)
        print("create single player")

    def enter(self, context): 
        self.context = context
        self.WIDTH = self.context.WIDTH
        self.HEIGHT = self.context.HEIGHT
        self.surface = self.context.surface
        self.clock = self.context.clock 
        self.playable_area_rect = pygame.Rect(25, 50, self.WIDTH -50, self.HEIGHT-75)   
        self.snake = Snake(self.surface, self.playable_area_rect) 
        self.food = Food(self.snake.snake_body, self.playable_area_rect)
        self.score = 0 
        self.keyboard = KeyboardHandler(self.snake)
        self.renderer = Renderer(self.surface, self.snake, self.food)
        print("enter in single player")

    def exit(self): 
        self.WIDTH = None
        self.HEIGHT = None
        self.surface = None
        self.clock = None
        self.snake = None
        self.food = None
        self.playable_area_rect = None
        self.keyboard = None
        self.renderer = None
        self.score = None
        print("exit from single player")


    def action(self): 

        self.surface.fill((0,0,0))   
        pygame.draw.rect(self.surface, (25,25,25), self.playable_area_rect)

        events = pygame.event.get()
        self.keyboard.handle_events(events)


        self.snake.validate_direction_and_change()
        self.snake.change_head_position()
        self.score = self.snake.snake_body_mechanism(
            self.score, self.food)

        self.renderer.draw_game_objects(self.score)
        
        game_over = False
        game_over, self.score = self.snake.check_for_boundaries(game_over, self.score)
        game_over, self.score = self.snake.check_for_self_body_collision(game_over, self.score)
        if game_over == True:
            self.context.change_state(self.context.game_state_list.main_menu)
            return
        # Установка максимальной частоты кадров (60 fps)
        self.clock.tick(10) 

        pygame.display.flip() 
 
