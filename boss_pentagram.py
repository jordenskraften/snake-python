import pygame
import math
from global_timer import TimedObject
class BossPentagram(TimedObject):
    def __init__(self, pentagram_distance, map_center_pos, boss, snake) -> None:
        self.lifetime = 0
        self.pentagram_distance = pentagram_distance
        self.map_center_pos = map_center_pos  
        self.boss = boss
        self.snake = snake  
        self.boss.global_timer.attach(self)
        self.boss.in_active_spell_action = True 
        self.boss_in_map_center = False
        self.next_boss_pos = self.map_center_pos 
        self.angle_in_rad = 0 
        self.emotion_was_sayed = False  
        #--------------
        self.pentagram_points = []
        self.point_A = map_center_pos
        self.point_B = map_center_pos
        self.point_C = map_center_pos
        self.point_D = map_center_pos
        self.point_E = map_center_pos  
        self.road_A = []
        self.road_B = []
        self.road_C = []
        self.road_D = []
        self.road_E = []
        self.all_roads = []
        self.road_to_visualization = []
        self.pentagram_visualisation_pointer = 0
        self.pentagram_points_created = False
        self.pentagram_visuzlized_full = False
        self.pentagram_explosed = False

        
    def timer_tick(self):
        self.boss.in_active_spell_action = True  

        if self.boss_in_map_center == True:
            self.lifetime -= 1 
            if self.lifetime <= 0:  
                self.death()   
            else: 
                #рисуем пентаграмму
                if self.pentagram_points_created == False:
                    self.create_pentagram_road()
                elif self.pentagram_visuzlized_full == False:
                    self.pentagram_vizualization()
                elif self.pentagram_explosed == False:
                    self.pentagram_explosion() 
                    self.lifetime = 15  
                #взрываем её
        else:
            #если босс дошел до центра
            if (
                abs(self.boss.center_pos[0] - self.map_center_pos[0]) <= 1 and
                abs(self.boss.center_pos[1] - self.map_center_pos[1]) <= 1
            ):
                self.boss_in_map_center = True
                self.lifetime = 150
                if self.emotion_was_sayed == False:
                    self.emotion_was_sayed = True
                    self.boss.create_floating_text("casting Pentagram!", True) 
                    self.boss.boss_pentagram.play()
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
        self.draw_obj()
 
    def draw_obj(self, red = False):     
        pass

    def enter():
        pass  

    def death(self):
        self.boss.global_timer.detach(self) 
        self.boss.in_active_spell_action = False  
        self.boss.base_abilities_cd = 0  
        self.boss.active_abilities_cd = self.boss.active_abilities_cd - (self.boss.active_abilities_cd_full // 2)  
        self.boss.boss_ultimate_ability_cd = 0
        self.boss.minions_cd = 130
        del(self)
    
    def pentagram_explosion(self):
        for r in self.all_roads: 
            #по всем пяти дорогам проходимся до их n точек  
            for p in r:
                self.boss.boss_create_single_voidzone(p)
        self.pentagram_explosed = True  

    def draw_road(self, road):
        if self.pentagram_visualisation_pointer >= len(road) -1:
            self.pentagram_visualisation_pointer = len(road) -1
            self.pentagram_visuzlized_full = True
            #костыль, последняя точка не отрисовывается, добавим тут её
            #заебало искать причину
            if len(road) >= 1:
                self.road_to_visualization.append(road[0])
                self.road_to_visualization.append(road[-1])
        if self.pentagram_visualisation_pointer <= len(road): 
            if self.pentagram_visuzlized_full == False:
                self.road_to_visualization.append(road[self.pentagram_visualisation_pointer])
                self.pentagram_visualisation_pointer += 1 
            if len(self.road_to_visualization) >= 1:
                for poi in self.road_to_visualization:
                    pygame.draw.rect(
                        self.boss.surface, (125, 125, 125), 
                        pygame.Rect
                        ( 
                            self.boss.DRAWING_OFFSET_X + (poi[0] * 10), 
                            self.boss.DRAWING_OFFSET_Y + (poi[1] * 10), 
                            10, 10
                        ) 
                    )    
    def pentagram_vizualization(self):
        self.draw_road(self.road_A)
        self.draw_road(self.road_B)
        self.draw_road(self.road_C)
        self.draw_road(self.road_D)
        self.draw_road(self.road_E)

    def create_pentagram_road(self): 
        offset = 90
        self.point_A = self.create_edge_point(1 - offset)
        self.point_B = self.create_edge_point(72 - offset)
        self.point_C = self.create_edge_point(144 - offset)
        self.point_D = self.create_edge_point(216 - offset)
        self.point_E = self.create_edge_point(288 - offset)
        #---------------------
        x0 = self.point_A[0]
        y0 = self.point_A[1]
        x1 = self.point_D[0]
        y1 = self.point_D[1]
        x2 = self.point_C[0]
        y2 = self.point_C[1]
        AD = self.get_points_on_line(x0, y0, x1, y1)
        AC = self.get_points_on_line(x0, y0, x2, y2)
        self.road_A += AD
        self.road_A += AC
        #---------------------
        x0 = self.point_B[0]
        y0 = self.point_B[1]
        x1 = self.point_E[0]
        y1 = self.point_E[1]
        x2 = self.point_D[0]
        y2 = self.point_D[1]
        BE = self.get_points_on_line(x0, y0, x1, y1)
        BD = self.get_points_on_line(x0, y0, x2, y2)
        self.road_B += BE
        self.road_B += BD
        #---------------------
        x0 = self.point_C[0]
        y0 = self.point_C[1]
        x1 = self.point_A[0]
        y1 = self.point_A[1]
        x2 = self.point_E[0]
        y2 = self.point_E[1]
        CA = self.get_points_on_line(x0, y0, x1, y1)
        CE = self.get_points_on_line(x0, y0, x2, y2)
        self.road_C += CA
        self.road_C += CE
        #---------------------
        x0 = self.point_D[0]
        y0 = self.point_D[1]
        x1 = self.point_A[0]
        y1 = self.point_A[1]
        x2 = self.point_B[0]
        y2 = self.point_B[1]
        DA = self.get_points_on_line(x0, y0, x1, y1)
        DB = self.get_points_on_line(x0, y0, x2, y2)
        self.road_D += DA
        self.road_D += DB
        #---------------------
        x0 = self.point_E[0]
        y0 = self.point_E[1]
        x1 = self.point_B[0]
        y1 = self.point_B[1]
        x2 = self.point_C[0]
        y2 = self.point_C[1]
        EB = self.get_points_on_line(x0, y0, x1, y1)
        EC = self.get_points_on_line(x0, y0, x2, y2)
        self.road_E += EB
        self.road_E += EC
        #-----------
        self.all_roads.append(self.road_A)
        self.all_roads.append(self.road_B)
        self.all_roads.append(self.road_C)
        self.all_roads.append(self.road_D)
        self.all_roads.append(self.road_E)
        self.pentagram_points_created = True

    def create_edge_point(self, angle):
        radius = self.pentagram_distance
        center_x = self.map_center_pos[0]
        center_y = self.map_center_pos[1]
        angle3 = math.radians(angle) 
        x = center_x + radius * math.cos(angle3)
        y = center_y + radius * math.sin(angle3)
        return [x,y] 

    def get_points_on_line(self, x0, y0, x1, y1):
        points = [] 
        prev_pos = [x0,y0]
        for i in range(self.pentagram_distance):
            d_x = x1 - x0  
            d_y = y1 - y0
            distance = math.sqrt(d_x**2 + d_y**2)
            step_x = d_x / distance * 1
            step_y = d_y / distance * 1
            dir = (step_x,step_y)  
            prev_pos = [
                        prev_pos[0] + dir[0],
                        prev_pos[1] + dir[1]
                        ] 
            points.append(prev_pos) 
        return points

 
    def limit_number(self, value, limit):
        if value >= limit:
            return limit
        elif value <= -limit:
            return -limit
        else: 
            return 0