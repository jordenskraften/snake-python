import pygame
import math
from global_timer import TimedObject
class BossWaveSpell(TimedObject):
    def __init__(self, map_center_pos, boss, snake) -> None:
        self.lifetime = 0 
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
        self.first_wave_spawned = False
        self.second_wave_spawned = False
        self.third_wave_spawned = False
        #---------
        self.wave_points = []
        self.wave_segment_size = 3

        
    def timer_tick(self):
        self.boss.in_active_spell_action = True  

        if self.boss_in_map_center == True:
            self.lifetime -= 1 
            if self.lifetime <= 0:  
                self.death()   
            else: 
                #рисуем пентаграмму
                if self.lifetime <= 105 and self.first_wave_spawned == False: 
                    self.first_wave_spawned = True
                    self.boss.boss_wave.play()
                    self.boss.create_floating_text("Taste my wave!", True)  
                    self.spawn_wave()
                if self.lifetime <= 65 and self.second_wave_spawned == False: 
                    self.second_wave_spawned = True
                    self.boss.boss_wave.play()
                    self.boss.create_floating_text("Uuuh, i like it!", True)  
                    self.spawn_wave()
                if self.lifetime <= 30 and self.third_wave_spawned == False: 
                    self.third_wave_spawned = True
                    self.boss.boss_wave.play()
                    self.boss.create_floating_text("Okay, that's the last one...", True)  
                    self.spawn_wave()
                #взрываем её
        else:
            #если босс дошел до центра
            if (
                abs(self.boss.center_pos[0] - self.map_center_pos[0]) <= 1 and
                abs(self.boss.center_pos[1] - self.map_center_pos[1]) <= 1
            ):
                self.boss_in_map_center = True
                self.lifetime = 115
                if self.emotion_was_sayed == False:
                    self.emotion_was_sayed = True
                    self.boss.create_floating_text("casting Wave!", True)  
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
        if len(self.wave_points) >= 1:
            for p in self.wave_points:
                self.move_wave_segment(p)
                self.draw_wave_segment(p)
                self.check_for_snakes_bodies_collision(p)
 
    def move_wave_segment(self, point): 
        point[1] += 2

    def draw_wave_segment(self, point):     
        new_points = self.get_all_surrounding_points(point, self.wave_segment_size)
          
        for point in new_points:
            pygame.draw.rect(
                self.boss.surface, (255, 125, 125),
                pygame.Rect
                ( 
                    self.boss.DRAWING_OFFSET_X + (point[0] * 10), 
                    self.boss.DRAWING_OFFSET_Y + (point[1] * 10), 
                    10, 10
                )
            ) 

    def get_all_surrounding_points(self, start_point, max_step_length):
        x = start_point[0]
        y = start_point[1] 
        all_surrounding_points = [] 
        for i in range(-self.wave_segment_size -1, self.wave_segment_size +1, 1):
            for j in range(-self.wave_segment_size -1, self.wave_segment_size +1, 1):
                all_surrounding_points.append([x+i,y+j])
        all_surrounding_points.append([x,y]) 
        return all_surrounding_points

    def check_for_snakes_bodies_collision(self, pos): 
        obstacles = self.boss.collisions.get_obstacles()
        for block in obstacles: 
            if (
                abs(block[0] - pos[0]) <= self.wave_segment_size and
                abs(block[1] - pos[1]) <= self.wave_segment_size 
            ): 
                if self.snake.damage_immune_mode == False:
                    self.boss.collision_with_snake()  

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
    
    def spawn_wave(self): 
        self.wave_points.clear() 
        for i in range(0, 11):
            self.wave_points.append([3 + (6 * i), -3])  
        

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