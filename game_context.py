import pygame  
from renderer import Renderer
from keyboard_inputs import KeyboardHandler
from game_state_list import GameStateList 
from game_state import GameState

class GameContext:
    def __init__(self): 
        self.WIDTH = 720
        self.HEIGHT = 460  

        pygame.init()
        pygame.display.set_caption("Snake Game") 
        self.surface = pygame.display.set_mode((self.WIDTH, self.HEIGHT)) 
        self.clock = pygame.time.Clock()   
        self.game_state_list = GameStateList(self)

        #self.state = self.game_state_list.single_state
        self.state = GameState()
 
        self.game_over = False

    def change_state(self, next_state):
        self.state.exit()
        self.state = next_state
        self.state.enter(self)

    def play(self): 
        self.change_state(self.game_state_list.main_menu)
        while not self.game_over:
             
            #тута стейт будет свой экшн на кадр делать
            self.state.action() 
 
        pygame.quit()
        quit()
 
