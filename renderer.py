import pygame

class FloatingText:
    def __init__(self, pos, lifetime, text, surface):
        self.x = pos[0]
        self.y = pos[1] 
        self.lifetime = lifetime
        self.text = text
        self.surface = surface
        self.opacity = 1
class Renderer: 
    def __init__(self, surface, food):
        self.surface = surface
        self.snakes = []
        self.food = food 
        self.__boss = None
        self.floating_texts = set()
  
    def set_boss(self, boss):
        self.__boss = boss

    def add_snake(self, snake):
        self.snakes.append(snake)

    def remove_sname(self, snake):
        self.snakes.remove(snake)

    def draw_game_objects(self, score_val, score_val_ai = None, ai_vs_ai_mode = False): 
        if self.__boss != None:
            self.__boss.draw_boss()   
        for s in self.snakes: 
            s.draw_snake()   
        self.food.draw_food(self.surface) 
        self.display_tooltip()
        if ai_vs_ai_mode == False:
            self.display_score(score_val)
            if score_val_ai != None:
                self.display_score_ai(score_val_ai)
        else:
            self.display_score_ai(score_val)
            self.display_score_ai2(score_val_ai)
        self.update_floating_texts()

        
    def display_score(self, score_val):
        font = pygame.font.SysFont('arial', 20)
        score = font.render("Player score: " + str(score_val), True, (255, 255, 255))
        self.surface.blit(score, (500, 10)) 

    def display_score_ai(self, score_val):
        font = pygame.font.SysFont('arial', 20)
        score = font.render("AI score: " + str(score_val), True, (255, 255, 255))
        self.surface.blit(score, (100, 10)) 

    def display_score_ai2(self, score_val):
        font = pygame.font.SysFont('arial', 20)
        score = font.render("AI-2 score: " + str(score_val), True, (255, 255, 255))
        self.surface.blit(score, (500, 10)) 
 
    def display_tooltip(self):
        font = pygame.font.SysFont('arial', 20)
        score = font.render("Press ESC to main menu: ", True, (255, 255, 255))
        self.surface.blit(score, (250, 10))  
#------------------- 
    def create_floating_text(self, pos, lifetime, text):
        ft = FloatingText(pos, lifetime, text, self.surface)
        self.add_floating_text(ft) 

    def render_floating_text(self, ft): 
        color = (255, 255, 255)
        font = pygame.font.SysFont('arial', 20)  
        t = font.render(ft.text, True, color) 
        self.surface.blit(t, (ft.x, ft.y - 15))  

    def update_floating_texts(self): 
        texts = list(self.floating_texts)
        for ft in texts:
            ft.lifetime -= 0.1
            ft.y -= 1
            ft.opacity -= 0.1
            if ft.lifetime <= 0:
                self.remove_floating_text(ft)
            self.render_floating_text(ft)

    def add_floating_text(self, ft): 
        self.floating_texts.add(ft)

    def remove_floating_text(self, ft): 
        self.floating_texts.remove(ft)

#-------------------

    #этот парень будет еще отрисовывать абилки босса до отрисовки змеек и тушки босса 