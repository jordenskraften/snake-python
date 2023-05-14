import pygame  
from collisions import Collisiions
from keyboard_inputs import MovementDirection 
from snake import Snake
from random import randrange

class Boss:
    def __init__(self, surface, game_rect, collisions, snake, renderer ): 
        self.surface = surface
        self.game_rect = game_rect
        self.color = (0, 0, 255) 
        self.snake = snake
        self.DRAWING_OFFSET_X = self.game_rect.x
        self.DRAWING_OFFSET_Y = self.game_rect.y
        self.COORDS_WIDTH = game_rect.width // 10
        self.COORDS_HEIGHT = game_rect.height // 10
        self.snake_spawn_x = 3
        self.snake_spawn_y = 3
        self.center_pos = [self.snake_spawn_x, self.snake_spawn_y] 
        self.collisions = collisions
        self.color = (255, 125, 0)   
        self.direction = MovementDirection.RIGHT
        self.change_to = self.direction 
        self._time_tick = 0  # приватное поле, начинающееся с подчеркивания 
        self.movespeed = 0.5
        self.pause_boss_timer = 0
        self.paused = False  
        self.injured = False
        self.collision_cooldown_timer = 0
        self.collision_on_cooldown = False  
        #------ 
        self.renderer = renderer
    @property
    def time_tick(self):
        return self._time_tick

    @time_tick.setter
    def time_tick(self, value):
        if value >= 35:  
            self._time_tick = 0 
            self.boss_select_ability_action()
        else: 
            self._time_tick = value
        #---------------
        if self.collision_cooldown_timer <= 0:
            self.collision_on_cooldown = False 
        else:
            self.collision_cooldown_timer -= 1 
            self.collision_on_cooldown = True

        if self.collision_on_cooldown == True:
            if self.collision_cooldown_timer %3 == 0:
                self.snake.color = (255, 255, 255)  
            else:
                self.snake.color = (0, 0, 0)  
        else:
            self.snake.color = (0, 0, 255)  
        #---------------
        if self.pause_boss_timer <= 0:
            self.paused = False
            self.injured = False
        else:
            self.pause_boss_timer -= 1
            self.paused = True 
        #--------------
        if self.injured == True:
            self.color = (255, 0, 0)  
        else:
            if self.collision_on_cooldown == True:
                self.color = (255, 225, 0)  
            else:
                self.color = (255, 125, 0)  
    
    def add_movespeed(self, val):
        self.movespeed += val
        if self.movespeed < 0.5:
            self.movespeed = 0.5 

    def create_floating_text(self, text):
        pos = (
                self.DRAWING_OFFSET_X + (self.center_pos[0] * 10),
                self.DRAWING_OFFSET_Y + (self.center_pos[1] * 10)
            ) 
        self.renderer.create_floating_text(pos, 1, text)
 
    def collision_with_snake(self):
        #реакция на то когда босс догнал змею
        self.collision_cooldown_timer, self.pause_boss_timer = 18, 21
        self.collision_on_cooldown = True  
        self.create_floating_text("haha, catched!")

    def injury(self):
        #реакция на то когда игрок съедает яблоко
        self.pause_boss_timer = 5
        self.time_tick = 6 #чтобы после дамага босс сразу не кастовал добавим к гкд паузу инжури стейта
        self.injured = True 
        self.add_movespeed(0.05)  
        self.create_floating_text("awww, i feels pain!") 

    def boss_select_ability_action(self):
        #тут нарн в зависимости от дистанции будем стрелять, телепортироваться или еще че делать 
        if self.time_tick <= 0: 
            if self.pause_boss_timer <= 0:
                r = randrange(0, 5)
                match r:
                    case 0:
                        self.teleport()
                    case 1:
                        self.clap()
                    case 2:
                        self.shoot()
                    case _:
                        pass
            else:
                self.time_tick = 0


    def teleport(self):
        self.create_floating_text("casting TELEPORT!") 

    def clap(self):
        self.create_floating_text("casting CLAP!") 

    def shoot(self):
        self.create_floating_text("SHOOTING") 

    def void_zone(self):
        self.create_floating_text("casting VOID ZONES") 
        #змейке надо будет сменить дирекшн
        #в зависимости от её горизонтального или вертикального направления
        #на нее чуть спереди от её лица будет идти войд зона от которой надо будет отбежать 

    def change_boss_center_position(self): 
        if self.direction == MovementDirection.RIGHT:
            self.center_pos[0] += self.movespeed 
        elif self.direction == MovementDirection.LEFT:
            self.center_pos[0] -= self.movespeed 
        elif self.direction == MovementDirection.UP:
            self.center_pos[1] -= self.movespeed 
        elif self.direction == MovementDirection.DOWN:
            self.center_pos[1] += self.movespeed 

    def boss_body_mechanism(self, snake): 
        pass

    def generate_boss_body_points(self, x, y):
        directions = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]

        points = []
        for direction in directions:
            new_x = x + direction[0]
            new_y = y + direction[1]
            points.append((new_x, new_y))

        return points

    def draw_boss(self, red = False):  
        #мы не будем физически создавать 7 точек в тело чтоб сделать жир боссу
        #мы йобнем иллюзию, отрисовав все соседние точки его центра на 1 шаг  
        c_x = self.center_pos[0]
        c_y = self.center_pos[1]
        new_points = self.generate_boss_body_points(c_x, c_y)
          
        for point in new_points:
            pygame.draw.rect(
                self.surface, self.color, 
                pygame.Rect
                ( 
                    self.DRAWING_OFFSET_X + (point[0] * 10), 
                    self.DRAWING_OFFSET_Y + (point[1] * 10), 
                    10, 10
                )
            ) 
  
    def check_for_snakes_bodies_collision(self):
        if self.collision_on_cooldown == False:
            obstacles = self.collisions.get_obstacles()
            for block in obstacles: 
                if (
                    abs(block[0] - self.center_pos[0]) <= 2 and
                    abs(block[1] - self.center_pos[1]) <= 2 
                ):
                    self.collision_with_snake()
            return False

    def actions(self, snake):  
        #попробуем имитировать время, когда главное окно дергает эту функцию происходит константно несколько кадров
        self.time_tick += 1 

        if self.paused == False:
            self.change_to = self.ai_movement() 
            self.change_boss_center_position()
            self.boss_body_mechanism(snake) 
            self.check_for_snakes_bodies_collision() 
  
    def ai_movement(self): 
        self.create_path()

    def create_path(self):  
        s_x = self.center_pos[0]
        s_y = self.center_pos[1]
        start = (s_x, s_y)

        e_x = self.snake.snake_head_pos[0]
        e_y = self.snake.snake_head_pos[1]
        end = (e_x, e_y)

        new_dir = (
                end[0] - start[0],
                end[1] - start[1]
        ) 
        self.ai_change_direction(new_dir)

    def ai_change_direction(self, vector):
        x, y = vector
        changed_pos = False
        if self.direction == MovementDirection.RIGHT and changed_pos == False: 
            if x != 0 or y != 0:
                if x < 1 and y > 1:
                    self.direction = MovementDirection.DOWN
                    changed_pos = True
                if x < 1 and y < 1:
                    self.direction = MovementDirection.UP  
                    changed_pos = True
                if x >= 1 and y == 0:
                    self.direction = MovementDirection.RIGHT  
                    changed_pos = True


        if self.direction == MovementDirection.LEFT and changed_pos == False:
            if x != 0 or y != 0:
                if x > 1 and y > 1:
                    self.direction = MovementDirection.DOWN
                    changed_pos = True
                if x > 1 and y < 1:
                    self.direction = MovementDirection.UP  
                    changed_pos = True 
                if x <= 1 and y == 0:
                    self.direction = MovementDirection.LEFT  
                    changed_pos = True

        if self.direction == MovementDirection.DOWN and changed_pos == False:
            if x != 0 or y != 0:
                if x > 1 and y < 1:
                    self.direction = MovementDirection.RIGHT
                    changed_pos = True
                if x < 1 and y < 1:
                    self.direction = MovementDirection.LEFT 
                    changed_pos = True 
                if y <= 1 and x == 0:
                    self.direction = MovementDirection.DOWN  
                    changed_pos = True

        if self.direction == MovementDirection.UP and changed_pos == False:
            if x != 0 or y != 0:
                if x > 1 and y > 1:
                    self.direction = MovementDirection.RIGHT
                    changed_pos = True
                if x < 1 and y > 1:
                    self.direction = MovementDirection.LEFT 
                    changed_pos = True 
                if y >= 1 and x == 0:
                    self.direction = MovementDirection.UP  
                    changed_pos = True 
 

