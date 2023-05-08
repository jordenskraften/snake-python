import sys
import pygame
from snake import Snake
from food import Food
from renderer import Renderer 
from game_state import GameState
from collisions import Collisiions 


class AiVersusAiState(GameState):
    def __init__(self, context):   
        self.context = context
        self.WIDTH = self.context.WIDTH
        self.HEIGHT = self.context.HEIGHT
        self.surface = self.context.surface
        self.clock = self.context.clock 
        self.playable_area_rect = pygame.Rect(25, 50, self.WIDTH -50, self.HEIGHT-75)  
        self.collisions = Collisiions() 

        self.food = Food(self.playable_area_rect, self.collisions)  
        self.snake_AI = Snake(self.surface, self.playable_area_rect, self.collisions, self.food, True) 
        self.snake_AI_second = Snake(self.surface, self.playable_area_rect, self.collisions, self.food, True)  
        self.collisions.add_snake_to_list(self.snake_AI)
        self.collisions.add_snake_to_list(self.snake_AI_second) 
  
        self.renderer = Renderer(self.surface, self.food) 
        self.renderer.add_snake(self.snake_AI)
        self.renderer.add_snake(self.snake_AI_second)
        print("create ai_vs_ai")

    def enter(self, context): 
        self.context = context
        self.WIDTH = self.context.WIDTH
        self.HEIGHT = self.context.HEIGHT
        self.surface = self.context.surface
        self.clock = self.context.clock 
        self.playable_area_rect = pygame.Rect(25, 50, self.WIDTH -50, self.HEIGHT-75)   
        self.collisions = Collisiions() 

        self.food = Food(self.playable_area_rect, self.collisions) 
        self.snake_AI = Snake(self.surface, self.playable_area_rect, self.collisions, self.food, True) 
        self.snake_AI_second = Snake(self.surface, self.playable_area_rect, self.collisions, self.food, True)    
        self.collisions.add_snake_to_list(self.snake_AI)
        self.collisions.add_snake_to_list(self.snake_AI_second)
  
        self.renderer = Renderer(self.surface, self.food)
        self.renderer.add_snake(self.snake_AI)
        self.renderer.add_snake(self.snake_AI_second)
        print("enter in ai_vs_ai")

    def exit(self): 
        self.WIDTH = None
        self.HEIGHT = None
        self.surface = None
        self.clock = None 
        self.snake_AI = None
        self.snake_AI_second = None
        self.food = None
        self.playable_area_rect = None 
        self.renderer = None 
        print("exit from ai_vs_ai")


    def action(self): 

        self.surface.fill((0,0,0))   
        pygame.draw.rect(self.surface, (25,25,25), self.playable_area_rect)

        events = pygame.event.get()
  
        self.collisions.update_obstacles()

        if self.snake_AI:
            ai_fall = self.snake_AI.actions(self.food) 
            if ai_fall == True:
                self.snake_AI.respawn()

        if self.snake_AI_second:
            ai_fall = self.snake_AI_second.actions(self.food) 
            if ai_fall == True:
                self.snake_AI_second.respawn()
  
        self.renderer.draw_game_objects(self.snake_AI.score, self.snake_AI_second.score, True)  
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
 
