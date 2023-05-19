import pygame
import math
from global_timer import TimedObject
class BossLaserSpell(TimedObject):
    def __init__(self, laser_distance, circles_count, map_center_pos, boss, snake, spell_level = 1) -> None:
        self.lifetime = 0
        self.laser_distance = laser_distance
        self.circles_count = circles_count
        self.circles_count_current = 0
        self.map_center_pos = map_center_pos  
        self.boss = boss
        self.snake = snake  
        self.boss.global_timer.attach(self)
        self.boss.in_active_spell_action = True 
        self.boss_in_map_center = False
        self.next_boss_pos = self.map_center_pos 
        self.angle_in_rad = 0
        self.spell_level = spell_level
        self.emotion_was_sayed = False
        self.angle_per_tick_speed = 5
        self.first_laser_is_done = False
        self.second_laser_is_done = False
        self.third_laser_is_done = False

        
    def timer_tick(self):
        self.boss.in_active_spell_action = True 
        if (
            self.first_laser_is_done == True and
            self.second_laser_is_done == True and
            self.third_laser_is_done == True
            ): 
            self.circles_count_current = 99999
            self.lifetime = -1111

        if self.boss_in_map_center == True:
            self.lifetime -= 1 
            if self.lifetime <= 0 or self.circles_count_current >= self.circles_count:
                self.death()   
            else: 
                self.laser_rounding_action()
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
                    self.boss.create_floating_text("casting Laser!", True) 
                    self.boss.boss_laser.play()
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
        self.boss.active_abilities_cd = 0  
        self.boss.boss_ultimate_ability_cd = self.boss.boss_ultimate_ability_cd_full - (self.boss.boss_ultimate_ability_cd_full // 3) 
        self.boss.minions_cd = 130
        del(self)

    def laser_rounding_action(self): 
        if self.angle_in_rad >= 360:
            self.circles_count_current += 1 
            self.angle_in_rad = 0 
        self.angle_in_rad += self.angle_per_tick_speed  
        if self.spell_level <= 1:
            self.create_laser(0, 1)
            self.second_laser_is_done = True
            self.third_laser_is_done = True
        if self.spell_level == 2:
            self.create_laser(0, 1)
            self.create_laser(180, 2)
            self.third_laser_is_done = True
        if self.spell_level >= 3:
            self.create_laser(0, 1)
            self.create_laser(120, 2)
            self.create_laser(240, 3)

    def create_laser(self, bonus_angle, laser_number):
        if laser_number == 1:
            if self.first_laser_is_done == True:
                return
        if laser_number == 2:
            if self.second_laser_is_done == True:
                return
        if laser_number == 3:
            if self.third_laser_is_done == True:
                return
        radius = self.laser_distance
        center_x = self.map_center_pos[0]
        center_y = self.map_center_pos[1]
        angle2 = math.radians(self.angle_in_rad + bonus_angle) 
        x = center_x + radius * math.cos(angle2)
        y = center_y + radius * math.sin(angle2)
        edge_pos = (x,y)    
        pygame.draw.line(self.boss.surface, (255, 0, 0),  
                    ( 
                        self.boss.DRAWING_OFFSET_X + (self.boss.center_pos[0] * 10), 
                        self.boss.DRAWING_OFFSET_Y + (self.boss.center_pos[1] * 10) 
                    ), 
                    ( 
                        self.boss.DRAWING_OFFSET_X + (edge_pos[0] * 10), 
                        self.boss.DRAWING_OFFSET_Y + (edge_pos[1] * 10) 
                    ), 
                    2)  
        pygame.draw.rect(
            self.boss.surface, (255, 255, 255), 
            pygame.Rect
            ( 
                self.boss.DRAWING_OFFSET_X + (edge_pos[0] * 10), 
                self.boss.DRAWING_OFFSET_Y + (edge_pos[1] * 10), 
                10, 10
            ) 
        )   
        laser_points = self.get_points_on_line(
                    edge_pos[0], edge_pos[1],
                    self.map_center_pos[0], self.map_center_pos[1]
                )   
        #коллизии 
        self.check_for_snakes_bodies_collision(laser_points, laser_number)

    def check_for_snakes_bodies_collision(self, laser_points, laser_number): 
        obstacles = self.boss.collisions.get_obstacles()
        for point in laser_points:
            for block in obstacles:  
                d_x = point[0] - block[0]  
                d_y = point[1] - block[1]
                distance = abs(math.sqrt(d_x**2 + d_y**2))
                if distance <= 0.8: 
                    if self.snake.damage_immune_mode == False:
                        self.boss.collision_with_snake() 
                    #если лазер коснулся змейки то пусть уничтожится
                    #а то читерный лазер какой-то, пусть его неуяз тоже контрит
                    if laser_number == 1: 
                        self.first_laser_is_done = True 
                    if laser_number == 2: 
                        self.second_laser_is_done = True 
                    if laser_number == 3: 
                        self.third_laser_is_done = True 

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