import sys
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

        self.food = Food(self.playable_area_rect, self.collisions) 
        self.snake = Snake(self.surface, self.playable_area_rect, self.collisions, self.food)  
        self.collisions.add_snake_to_list(self.snake) 
 
        self.keyboard = KeyboardHandler(self.snake)
        self.renderer = Renderer(self.surface, self.food)
        self.renderer.add_snake(self.snake)  

    def enter(self, context): 
        self.context = context
        self.WIDTH = self.context.WIDTH
        self.HEIGHT = self.context.HEIGHT
        self.surface = self.context.surface
        self.clock = self.context.clock 
        self.playable_area_rect = pygame.Rect(25, 50, self.WIDTH -50, self.HEIGHT-75)   
        self.collisions = Collisiions() 

        self.food = Food(self.playable_area_rect, self.collisions) 
        self.snake = Snake(self.surface, self.playable_area_rect, self.collisions, self.food)  
        self.collisions.add_snake_to_list(self.snake) 
 
        self.keyboard = KeyboardHandler(self.snake)
        self.renderer = Renderer(self.surface, self.food)
        self.renderer.add_snake(self.snake)  

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


    def action(self): 

        self.surface.fill((0,0,0))   
        pygame.draw.rect(self.surface, (25,25,25), self.playable_area_rect)

        events = pygame.event.get()

        self.keyboard.handle_events(events) 
 

        self.collisions.update_obstacles()
  
        game_over = self.snake.actions(self.food) 
        if game_over == True:
            self.snake.respawn()

            
        self.renderer.draw_game_objects(self.snake.score) 
        #------------выход в меню 
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.context.change_state(self.context.game_state_list.main_menu)
                    return  
        # Установка максимальной частоты кадров (60 fps)
        self.clock.tick(10) 

        pygame.display.flip() 
 
