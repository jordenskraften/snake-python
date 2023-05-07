import pygame
from snake import Snake
from food import Food
from renderer import Renderer
from keyboard_inputs import KeyboardHandler
from game_state import GameState
from collisions import Collisiions


class SingleGameState(GameState):
    def __init__(self, context):   
        self.context = context
        self.WIDTH = self.context.WIDTH
        self.HEIGHT = self.context.HEIGHT
        self.surface = self.context.surface
        self.clock = self.context.clock 
        self.playable_area_rect = pygame.Rect(25, 50, self.WIDTH -50, self.HEIGHT-75)  
        self.collisions = Collisiions() 

        self.snake = Snake(self.surface, self.playable_area_rect, self.collisions) 
        self.snake_AI = Snake(self.surface, self.playable_area_rect, self.collisions, True) 
        self.collisions.add_snake_to_list(self.snake)
        self.collisions.add_snake_to_list(self.snake_AI)

        self.food = Food(self.snake.snake_body, self.playable_area_rect) 
        self.keyboard = KeyboardHandler(self.snake)
        self.renderer = Renderer(self.surface, self.food)
        self.renderer.add_snake(self.snake)
        self.renderer.add_snake(self.snake_AI)
        print("create single player")

    def enter(self, context): 
        self.context = context
        self.WIDTH = self.context.WIDTH
        self.HEIGHT = self.context.HEIGHT
        self.surface = self.context.surface
        self.clock = self.context.clock 
        self.playable_area_rect = pygame.Rect(25, 50, self.WIDTH -50, self.HEIGHT-75)   
        self.collisions = Collisiions() 

        self.snake = Snake(self.surface, self.playable_area_rect, self.collisions) 
        self.snake_AI = Snake(self.surface, self.playable_area_rect, self.collisions, True) 
        self.collisions.add_snake_to_list(self.snake)
        self.collisions.add_snake_to_list(self.snake_AI)

        self.food = Food(self.snake.snake_body, self.playable_area_rect) 
        self.keyboard = KeyboardHandler(self.snake)
        self.renderer = Renderer(self.surface, self.food)
        self.renderer.add_snake(self.snake)
        self.renderer.add_snake(self.snake_AI)
        print("enter in single player")

    def exit(self): 
        self.WIDTH = None
        self.HEIGHT = None
        self.surface = None
        self.clock = None
        self.snake = None
        self.snake_AI = None
        self.food = None
        self.playable_area_rect = None
        self.keyboard = None
        self.renderer = None 
        print("exit from single player")


    def action(self): 

        self.surface.fill((0,0,0))   
        pygame.draw.rect(self.surface, (25,25,25), self.playable_area_rect)

        events = pygame.event.get()

        self.keyboard.handle_events(events) 
 

        self.collisions.update_obstacles()

        if self.snake_AI:
            ai_fall = self.snake_AI.actions(self.food) 
            if ai_fall == True:
                self.renderer.remove_sname(self.snake_AI)
                self.collisions.remove_snake_from_list(self.snake_AI)
                del self.snake_AI
                self.snake_AI = None

        game_over = self.snake.actions(self.food) 
        if game_over == True:
            self.context.change_state(self.context.game_state_list.main_menu)
            return

            
        self.renderer.draw_game_objects(self.snake.score) 
        # Установка максимальной частоты кадров (60 fps)
        self.clock.tick(10) 

        pygame.display.flip() 
 
