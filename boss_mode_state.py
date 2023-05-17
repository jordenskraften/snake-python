import sys
import pygame
from snake import Snake
from boss import Boss
from food import Food
from renderer import Renderer
from keyboard_inputs import KeyboardHandler
from game_state import GameState
from collisions import Collisiions
from global_timer import GlobalTimer


class BossModeState(GameState):
    def __init__(self, context):   
        self.context = context
        self.WIDTH = self.context.WIDTH
        self.HEIGHT = self.context.HEIGHT
        self.surface = self.context.surface
        self.clock = self.context.clock 
        self.playable_area_rect = pygame.Rect(25, 50, self.WIDTH -50, self.HEIGHT-75)  
        self.collisions = Collisiions() 
        self.food = Food(self.playable_area_rect, self.collisions) 
        self.renderer = Renderer(self.surface, self.food)
 
        self.timer = GlobalTimer()
        self.snake = Snake(self.surface, self.playable_area_rect, self.collisions, self.food) 
        self.boss = Boss(self.surface, self.playable_area_rect, self.collisions, self.snake, self.renderer, self.timer)
        self.snake.boss = self.boss
        self.collisions.add_snake_to_list(self.snake) 
 
        self.keyboard = KeyboardHandler(self.snake) 
        self.renderer.add_snake(self.snake)
        self.renderer.set_boss(self.boss)  
        self.timer.attach(self.boss) 
        self.timer.attach(self.snake) 

    def enter(self, context): 
        self.context = context
        self.WIDTH = self.context.WIDTH
        self.HEIGHT = self.context.HEIGHT
        self.surface = self.context.surface
        self.clock = self.context.clock 
        self.playable_area_rect = pygame.Rect(25, 50, self.WIDTH -50, self.HEIGHT-75)   
        self.collisions = Collisiions() 
        self.food = Food(self.playable_area_rect, self.collisions) 
        self.renderer = Renderer(self.surface, self.food)
 
        self.timer = GlobalTimer()
        self.snake = Snake(self.surface, self.playable_area_rect, self.collisions, self.food) 
        self.boss = Boss(self.surface, self.playable_area_rect, self.collisions, self.snake, self.renderer, self.timer)
        self.snake.boss = self.boss
        self.collisions.add_snake_to_list(self.snake) 
 
        self.keyboard = KeyboardHandler(self.snake) 
        self.renderer.add_snake(self.snake)
        self.renderer.set_boss(self.boss)  
        self.timer.attach(self.boss) 
        self.timer.attach(self.snake) 
        pygame.mixer.init()
        pygame.mixer.music.load("sounds/boss_mode_music.mp3")
        pygame.mixer.music.play(-1)

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
        self.timer = None
        pygame.mixer.music.stop()


    def action(self): 

        self.surface.fill((0,0,0))   
        pygame.draw.rect(self.surface, (25,25,25), self.playable_area_rect)

        events = pygame.event.get() 
        self.timer.tick()
        
        self.keyboard.handle_events(events) 
 

        self.collisions.update_obstacles()
 
        self.boss.actions()  

        game_over = self.snake.actions(self.food) 
        if self.snake.snake_lives <= 0:
            game_over = True
        if game_over == True:
            self.context.change_state(self.context.game_state_list.main_menu)
            return  

        self.renderer.draw_game_objects( 
                                        0, None, False, 
                                        self.boss.boss_lives, 
                                        self.snake.snake_lives, 
                                        self.snake.damage_immune_ability_current_cd
                                        )
        #------------выход в меню 
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.context.change_state(self.context.game_state_list.main_menu)
                    return  
        # Установка максимальной частоты кадров   
        self.clock.tick(10) 

        pygame.display.flip() 
 
