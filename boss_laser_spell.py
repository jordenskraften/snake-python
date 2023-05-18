import pygame
import math
from global_timer import TimedObject
class BossLaserSpell(TimedObject):
    def __init__(self, duration, laser_distance, circles_count, map_center_pos, boss, snake) -> None:
        self.lifetime = duration
        self.laser_distance = laser_distance
        self.circles_count = circles_count
        self.circles_count_current = 0
        self.map_center_pos = map_center_pos 
        self.laser_edge_pos = [map_center_pos[0], map_center_pos[1] + self.laser_distance]
        self.boss = boss
        self.snake = snake  
        self.boss.global_timer.attach(self)
        self.boss.in_active_spell_action = True 
        self.boss_in_map_center = False
        self.next_boss_pos = self.map_center_pos
        self.angle_in_rad = 0

        
    def timer_tick(self):
        self.boss.in_active_spell_action = True 
        if self.boss_in_map_center == True:
            self.lifetime -= 1
            self.laser_rounding_action()
            if self.lifetime <= 0 or self.circles_count_current >= self.circles_count:
                self.death()   
        else:
            #если босс дошел до центра
            if (
                abs(self.boss.center_pos[0] - self.map_center_pos[0]) <= 1 and
                abs(self.boss.center_pos[1] - self.map_center_pos[1]) <= 1
            ):
                self.boss_in_map_center = True
                self.lifetime = 150
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
        pygame.draw.rect(
            self.boss.surface, (255, 255, 255), 
            pygame.Rect
            ( 
                self.boss.DRAWING_OFFSET_X + (self.laser_edge_pos[0] * 10), 
                self.boss.DRAWING_OFFSET_Y + (self.laser_edge_pos[1] * 10), 
                10, 10
            ) 
        )   

    def enter():
        pass  

    def death(self):
        self.boss.global_timer.detach(self) 
        self.boss.in_active_spell_action = False 
        #кд добавим а то лазер долгий сук
        self.boss.base_abilities_cd = 0 #self.boss.base_abilities_cd_full //2
        self.boss.active_abilities_cd = 0 #self.boss.active_abilities_cd_full  
        del(self)

    def laser_rounding_action(self):
        center_x = self.map_center_pos[0]
        center_y = self.map_center_pos[1]
        radius = self.laser_distance  
        angle = math.radians(self.angle_in_rad) 
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        self.laser_edge_pos = (x,y)  
        if self.angle_in_rad > 360:
            self.circles_count_current += 1 
            self.angle_in_rad = 0 
        self.angle_in_rad += 5 
        #отрисуем лазер
        pygame.draw.line(self.boss.surface, (255, 0, 0),  
                    ( 
                        self.boss.DRAWING_OFFSET_X + (self.boss.center_pos[0] * 10), 
                        self.boss.DRAWING_OFFSET_Y + (self.boss.center_pos[1] * 10) 
                    ), 
                    ( 
                        self.boss.DRAWING_OFFSET_X + (self.laser_edge_pos[0] * 10), 
                        self.boss.DRAWING_OFFSET_Y + (self.laser_edge_pos[1] * 10) 
                    ), 
                    2)
        #тут будут коллизии 
        laser_points = self.get_points_on_line(
                    self.laser_edge_pos[0], self.laser_edge_pos[1],
                    self.map_center_pos[0], self.map_center_pos[1]
                )
        #print(points)
        self.check_for_snakes_bodies_collision(laser_points)

    def check_for_snakes_bodies_collision(self, laser_points): 
        obstacles = self.boss.collisions.get_obstacles()
        for point in laser_points:
            for block in obstacles:  
                d_x = block[0] - point[0]  
                d_y = block[1] - point[1]
                distance = math.sqrt(d_x**2 + d_y**2)
                if distance <= 1:
                    if self.snake.damage_immune_mode == False:
                        self.boss.collision_with_snake() 

    def get_points_on_line(self, x0, y0, x1, y1):
        points = [] 
        prev_pos = self.boss.center_pos
        for i in range(self.laser_distance):
            d_x = x0 - x1  
            d_y = y0 - y1
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