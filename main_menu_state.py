import pygame 
from game_state import GameState

class MainMenuState(GameState):
    def __init__(self, context):   
        self.context = context
        self.WIDTH = self.context.WIDTH
        self.HEIGHT = self.context.HEIGHT
        self.surface = self.context.surface
        self.clock = self.context.clock   
        
        # Создание кнопок
        self.button1_rect = None
        self.button1_text = None
        
        self.button2_rect = None
        self.button2_text = None
        
        self.button3_rect = None
        self.button3_text = None

        self.button4_rect = None
        self.button4_text = None
        print("create main menu")
        
    def enter(self, context): 
        self.context = context
        self.WIDTH = self.context.WIDTH
        self.HEIGHT = self.context.HEIGHT
        self.surface = self.context.surface
        self.clock = self.context.clock  
        # Создание кнопок
        self.button1_rect = pygame.Rect(100, 50, 200, 50)
        self.button1_text = "Single Player"
        
        self.button2_rect = pygame.Rect(100, 150, 200, 50)
        self.button2_text = "Player versus AI"

        self.button3_rect = pygame.Rect(100, 250, 200, 50)
        self.button3_text = "AI versus AI"

        self.button4_rect = pygame.Rect(100, 350, 200, 50)
        self.button4_text = "Exit"
        print("enter in main menu")

    def exit(self): 
        self.WIDTH = None
        self.HEIGHT = None
        self.surface = None
        self.clock = None 
        self.button1_rect = None
        self.button1_text = None 
        self.button2_rect = None
        self.button2_text = None
        self.button3_rect = None
        self.button3_text = None
        self.button4_rect = None
        self.button4_text = None
        print("exit from main menu")

    def action(self): 
        self.surface.fill((125,125,125))     
        
        # Отображение кнопок
        pygame.draw.rect(self.surface, (255, 255, 255), self.button1_rect)
        events = pygame.event.get()
        font = pygame.font.SysFont(None, 30)
        text = font.render(self.button1_text, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.button1_rect.center)
        self.surface.blit(text, text_rect)
        
        pygame.draw.rect(self.surface, (255, 255, 255), self.button2_rect)
        text = font.render(self.button2_text, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.button2_rect.center)
        self.surface.blit(text, text_rect)

        pygame.draw.rect(self.surface, (255, 255, 255), self.button3_rect)
        text = font.render(self.button3_text, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.button3_rect.center)
        self.surface.blit(text, text_rect)
 
        pygame.draw.rect(self.surface, (255, 255, 255), self.button4_rect)
        text = font.render(self.button4_text, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.button4_rect.center)
        self.surface.blit(text, text_rect)
        
        # Обработка кликов на кнопках
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if self.button1_rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            self.context.change_state(self.context.game_state_list.single_player)
            return

        if self.button2_rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            self.context.change_state(self.context.game_state_list.player_versus_ai)
            return

        if self.button3_rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            self.context.change_state(self.context.game_state_list.ai_versus_ai)
            return

        if self.button4_rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            pygame.quit()
            quit() 
        
        # Установка максимальной частоты кадров (60 fps)
        self.clock.tick(15) 

        pygame.display.flip()
