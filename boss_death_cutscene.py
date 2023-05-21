import pygame
import math
from global_timer import TimedObject
class BossDeathCutscene(TimedObject):
    def __init__(self, map_center_pos, boss) -> None:
        self.lifetime = 999990 
        self.map_center_pos = map_center_pos  
        self.boss = boss 
        self.boss.global_timer.attach(self)
        self.boss.in_active_spell_action = True 
        self.boss.defeated = True
        self.boss_in_map_center = False 
        self.emotion_was_sayed = False   
        self.emotion_was_sayed2 = False   
        #---------
        self.wave_points = []
        self.wave_segment_size = 3

        
    def timer_tick(self):
        self.boss.in_active_spell_action = True  

        if self.boss_in_map_center == True:
            self.lifetime -= 1 
            if self.lifetime <= 40:  
                self.boss.center_pos = [9999,9999]  
                font = pygame.font.SysFont('arial', 40)
                score = font.render("You win!", True, (255, 255, 255))
                self.boss.surface.blit(score, (300, 200)) 
                self.boss.snake.food.hide()  
            if self.lifetime <= 15:  
                if self.emotion_was_sayed2 == False: 
                    self.emotion_was_sayed2 = True
                    self.boss.aniki.play()
                self.boss.center_pos = [9999,9999]  
                font = pygame.font.SysFont('arial', 20)
                score = font.render("Thank you for your attention", True, (255, 255, 255))
                self.boss.surface.blit(score, (300, 260))   
                #-------- 
                self.boss.center_pos = [9999,9999]  
                font = pygame.font.SysFont('arial', 20)
                score = font.render("created by Jordenskraften", True, (255, 255, 255))
                self.boss.surface.blit(score, (300, 290))   
            else:    
                if self.lifetime %3 == 0:
                    self.boss.color = (255,0,0)
                else:
                    self.boss.color = (125,0,0)
            #взрываем её
        else:
            #если босс дошел до центра
            if (
                abs(self.boss.center_pos[0] - self.map_center_pos[0]) <= 1 and
                abs(self.boss.center_pos[1] - self.map_center_pos[1]) <= 1
            ):
                self.boss_in_map_center = True
                self.lifetime = 110
                if self.emotion_was_sayed == False:
                    self.emotion_was_sayed = True
                    self.boss.boss_death.play()
                    self.boss.create_floating_text("Okay, you got me!", True)  
                    self.boss.snake.food.hide() 
                #print("boss in center")
            else: 
                #тута двигаем босса к центру 
                d_x = self.map_center_pos[0] - self.boss.center_pos[0]  
                d_y = self.map_center_pos[1] - self.boss.center_pos[1]  
                distance = math.sqrt(d_x**2 + d_y**2)
                step_x = d_x / distance * 1.5
                step_y = d_y / distance * 1.5
                dir = (step_x,step_y)  
                self.boss.center_pos = [
                            self.boss.center_pos[0] + dir[0],
                            self.boss.center_pos[1] + dir[1]
                            ] 
                self.boss.snake.food.hide()
        if len(self.wave_points) >= 1:
            for p in self.wave_points:
                self.move_wave_segment(p)
                self.draw_wave_segment(p)
                self.check_for_snakes_bodies_collision(p) 

    def enter():
        pass  

    def death(self):
        self.boss.global_timer.detach(self) 
        self.boss.in_active_spell_action = True  
        self.boss.defeated = True
        self.boss.base_abilities_cd = 999999
        self.boss.active_abilities_cd = 999999
        self.boss.boss_ultimate_ability_cd = 999999
        self.boss.minions_cd = 999999
        del(self)
     