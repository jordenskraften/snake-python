import pygame
import math 
from global_timer import TimedObject

class BossRoadSpell(TimedObject):
    def __init__(self, lifetime, boss, snake) -> None:
        self.lifetime = 0
        self.start_road_pos = [5,5] 
        self.boss = boss
        self.snake = snake  
        self.boss.global_timer.attach(self)
        self.boss.in_active_spell_action = True 
        self.boss_in_start_pos = False
        self.next_boss_pos = self.start_road_pos  
        self.emotion_was_sayed = False  
        self.road_was_created = False
        self.road_was_visualized = False
        self.ride_was_ended = False
        self.final_road = []
        self.road_len = 0
        self.current_road_point_index = 0
        self.road_point_to_draw = []
        self.current_ride_boss_point_index = 0

        
    def timer_tick(self):
        self.boss.in_active_spell_action = True  

        if self.boss_in_start_pos == True:
            self.lifetime -= 1 
            if self.lifetime <= 0:
                self.death()   
            else: 
                #тут будет сперва отрисовка потом движение босса
                if self.ride_was_ended == False:
                    if self.road_was_created == True:
                        self.draw_road()
                    if self.road_was_visualized == True:
                        self.ride_boss_to_point()
                else:
                    self.lifetime = -9999
        else:
            #если босс не дошел до старт точки 
            if (
                abs(self.boss.center_pos[0] - self.start_road_pos[0]) <= 2 and
                abs(self.boss.center_pos[1] - self.start_road_pos[1]) <= 2
            ):
                self.boss_in_start_pos = True
                self.lifetime = 500
                if self.emotion_was_sayed == False:
                    self.emotion_was_sayed = True
                    self.boss.create_floating_text("Time to ride!", True) 
                    self.boss.boss_road.play()
                    self.create_road()
                #print("boss in center")
            else:
                #тута двигаем босса к центру 
                d_x = self.start_road_pos[0] - self.boss.center_pos[0]  
                d_y = self.start_road_pos[1] - self.boss.center_pos[1]  
                distance = math.sqrt(d_x**2 + d_y**2)
                step_x = d_x / distance * 2
                step_y = d_y / distance * 2
                dir = (step_x,step_y)  
                self.boss.center_pos = [
                            self.boss.center_pos[0] + dir[0],
                            self.boss.center_pos[1] + dir[1]
                            ] 
        self.draw_obj()
         
    def ride_boss_to_point(self):
        if len(self.final_road) >= 1:
            target_pos = self.final_road[0]
            d_x = target_pos[0] - self.boss.center_pos[0]  
            d_y = target_pos[1] - self.boss.center_pos[1]  
            distance = math.sqrt(d_x**2 + d_y**2)
            step_x = d_x / distance * 3
            step_y = d_y / distance * 3
            dir = (step_x,step_y)  
            self.boss.center_pos = [
                        self.boss.center_pos[0] + dir[0],
                        self.boss.center_pos[1] + dir[1]
                        ] 
            #чек дисту           
            if (
                abs(self.boss.center_pos[0] - target_pos[0]) <= 3 and
                abs(self.boss.center_pos[1] - target_pos[1]) <= 3
            ):
                self.boss.boss_create_single_voidzone(self.final_road[0]) 

                if len(self.final_road) >= 1:
                    if target_pos in self.final_road:
                        self.final_road.remove(target_pos)

                if len(self.road_point_to_draw) >= 1:
                    if target_pos in self.road_point_to_draw:
                        self.road_point_to_draw.remove(target_pos) 
        else:
            self.ride_was_ended = True

    def draw_obj(self, red = False):     
        pass

    def enter():
        pass  

    def death(self):
        self.boss.global_timer.detach(self) 
        self.boss.in_active_spell_action = False 
        #кд добавим а то лазер долгий сук
        self.boss.base_abilities_cd = 0 #self.boss.base_abilities_cd_full //2
        self.boss.active_abilities_cd = 0 #self.boss.active_abilities_cd_full 
        self.boss.minions_cd = 130
        del(self) 
    
    def draw_road(self):
        if self.current_road_point_index >= self.road_len -1:
            self.current_road_point_index = self.road_len -1
            self.road_was_visualized = True
            #костыль, последняя точка не отрисовывается, добавим тут её
            #заебало искать причину
            if len(self.final_road) >= 1:
                self.road_point_to_draw.append(self.final_road[-1])
        if self.current_road_point_index <= self.road_len: 
            if self.road_was_visualized == False:
                self.road_point_to_draw.append(self.final_road[self.current_road_point_index])
                self.current_road_point_index += 1 
            if len(self.road_point_to_draw) >= 1:
                for poi in self.road_point_to_draw:
                    pygame.draw.rect(
                        self.boss.surface, (125, 125, 125), 
                        pygame.Rect
                        ( 
                            self.boss.DRAWING_OFFSET_X + (poi[0] * 10), 
                            self.boss.DRAWING_OFFSET_Y + (poi[1] * 10), 
                            10, 10
                        ) 
                    )   
 
    def create_road(self):
        line1 = []
        for i in range(0, 11):
            line1.append([self.start_road_pos[0] + (6 * i), self.start_road_pos[1]]) 
        for i in range(11):
            #это типа в обратном направлении отрисовка
            line1.append([self.start_road_pos[0] + ((6 * 10) - (6*i)), self.start_road_pos[1] + 7 ]) 
        for i in range(11):
            line1.append([self.start_road_pos[0] + (6 * i),  self.start_road_pos[1] + 14 ]) 
        for i in range(11):
            #это типа в обратном направлении отрисовка
            line1.append([self.start_road_pos[0] + ((6 * 10) - (6*i)), self.start_road_pos[1] + 22 ]) 
        for i in range(11):
            line1.append([self.start_road_pos[0] + (6 * i),  self.start_road_pos[1] + 28 ])
        self.final_road += line1 
        self.road_len = len(self.final_road)
        self.road_was_created = True
  
    def limit_number(self, value, limit):
        if value >= limit:
            return limit
        elif value <= -limit:
            return -limit
        else: 
            return 0