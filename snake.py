import pygame  
from collisions import Collisiions
from keyboard_inputs import MovementDirection 

class Snake:
    def __init__(self, surface, game_rect, collisions, food, is_ai = False, is_second_ai = False): 
        self.surface = surface
        self.game_rect = game_rect
        self.color = (0, 0, 255) 
        self.DRAWING_OFFSET_X = self.game_rect.x
        self.DRAWING_OFFSET_Y = self.game_rect.y
        self.COORDS_WIDTH = game_rect.width // 10
        self.COORDS_HEIGHT = game_rect.height // 10
        self.snake_spawn_x = self.COORDS_WIDTH // 2
        self.snake_spawn_y = self.COORDS_HEIGHT // 2 
        self.snake_head_pos = [self.snake_spawn_x, self.snake_spawn_y] 
        self.snake_ai = None
        self.is_ai = is_ai 
        self.food = food
        self.collisions = collisions
        if self.is_ai == True: 
            if is_second_ai:
                self.snake_head_pos = [10, 10]
            else:
                self.snake_head_pos = [self.COORDS_WIDTH-10, 10]
            self.color = (255, 125, 125)  
        self.snake_body = [self.snake_head_pos, [self.snake_head_pos[0], self.snake_head_pos[1]-1], [self.snake_head_pos[0], self.snake_head_pos[1]-1] ]  
        self.direction = MovementDirection.RIGHT
        self.change_to = self.direction
        self.score = 0  
        self.boss = None
        self.boss_mode = False
        self.time_tick = 0
        self.damage_immune_mode = False
        self.damage_immune_is_after_hit = False
        self.damage_immune_time = 0
        self.base_ms = 1
        self.current_ms = self.base_ms
        self.damage_immune_ability_cd = 120
        self.damage_immune_ability_current_cd = 0
        #---------
        self.snake_lives = 1511
    
    def respawn(self):
        self.snake_head_pos = [self.snake_spawn_x, self.snake_spawn_y]
        self.snake_body = [self.snake_head_pos]  
        self.direction = MovementDirection.RIGHT
        self.change_to = self.direction

    def validate_direction_and_change(self):
        if any((
            self.change_to == MovementDirection.UP and not self.direction == MovementDirection.DOWN, 
            self.change_to == MovementDirection.DOWN and not self.direction == MovementDirection.UP, 
            self.change_to == MovementDirection.LEFT and not self.direction == MovementDirection.RIGHT, 
            self.change_to == MovementDirection.RIGHT and not self.direction == MovementDirection.LEFT, 
        )): 
            self.direction = self.change_to

    def change_head_position(self):
        if self.direction == MovementDirection.RIGHT:
            self.snake_head_pos[0] += self.current_ms
        elif self.direction == MovementDirection.LEFT:
            self.snake_head_pos[0] -= self.current_ms
        elif self.direction == MovementDirection.UP:
            self.snake_head_pos[1] -= self.current_ms
        elif self.direction == MovementDirection.DOWN:
            self.snake_head_pos[1] += self.current_ms

    def snake_body_mechanism(self, food): 
        new_head_pos = self.snake_head_pos[:]  
        if (
            abs(new_head_pos[0] - food.food_pos[0]) < 1 and
            abs(new_head_pos[1] - food.food_pos[1]) < 1  
        ):  
            food.food_pos = food.renew_pos()
            self.score += 1
            if self.boss != None:
                self.boss.injury()
                #если змейка больше 12 то при поедании яблока в босс моде расти не надо дальше
                if len(self.snake_body) >= 12:
                    self.snake_body.pop()
        else: 
            self.snake_body.pop()
        self.snake_body.insert(0, new_head_pos) 


    def draw_snake(self): 
        for pos in self.snake_body: 
            pygame.draw.rect(
                self.surface, self.color, 
                pygame.Rect
                ( 
                    self.DRAWING_OFFSET_X + (pos[0] * 10), 
                    self.DRAWING_OFFSET_Y + (pos[1] * 10), 
                    10, 10
                )
            )
  
    def check_for_boundaries(self, game_over):
        if any((
            self.snake_head_pos[0] > self.COORDS_WIDTH  or self.snake_head_pos[0] < 0,
            self.snake_head_pos[1] > self.COORDS_HEIGHT or self.snake_head_pos[1] < 0
        )):
            if self.boss_mode == False:
                game_over = True
                return game_over
            else:
                #в босс моде мы крч если с границей сталкиваемся то не подыхаемся
                #а тпшимся с обратной стороны 
                if self.snake_head_pos[0] >= self.COORDS_WIDTH:
                    self.snake_head_pos[0] = -1 
                elif self.snake_head_pos[0] <= -1: 
                    self.snake_head_pos[0] = self.COORDS_WIDTH  
                elif self.snake_head_pos[1] >= self.COORDS_HEIGHT:
                    self.snake_head_pos[1] = -1 
                elif self.snake_head_pos[1] <= -1:
                    self.snake_head_pos[1] = self.COORDS_HEIGHT 
        return game_over

    def check_for_snakes_bodies_collision(self, game_over):
        obstacles = self.collisions.get_obstacles()
        for block in obstacles:  
            if (
                abs(block[0] - self.snake_head_pos[0]) < 1 and
                abs(block[1] - self.snake_head_pos[1]) < 1  
            ):  
                if self.boss == None:
                    game_over = True
                    return game_over 
                else:
                    if self.damage_immune_mode == False:
                        if len(self.snake_body) >= 2:
                            self.snake_body.pop()
                        self.damage_immune_after_hit()
                        self.snake_lives -= 1
                        self.boss.boss_snake_eat_himself_emotion()
        return game_over

    def actions(self, food): 
        if self.boss != None:
            if self.boss_mode == False:
                self.boss_mode = True

        if self.is_ai == True:
            self.change_to = self.ai_movement()
        self.validate_direction_and_change()
        self.change_head_position()
        self.snake_body_mechanism(food)
        game_over = False
        if game_over == False:
            game_over = self.check_for_boundaries(game_over)
        if game_over == False:
            game_over = self.check_for_snakes_bodies_collision(game_over) 
        if game_over == False:
            game_over = self.collisions.check_other_snakes_collisions(self)
        return game_over
  
    def ai_movement(self): 
        self.create_path()

    def create_path(self):  
        s_x = self.snake_head_pos[0]
        s_y = self.snake_head_pos[1]
        start = (s_x, s_y)

        e_x = self.food.food_pos[0]
        e_y = self.food.food_pos[1]
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
        #змейка иногда входит в границы и надо её развернуть  
        if self.direction == MovementDirection.RIGHT and self.COORDS_WIDTH - self.snake_head_pos[0] < 1:
            if self.snake_head_pos[1] >= self.COORDS_HEIGHT//2:
                self.direction = MovementDirection.DOWN
            else:
                self.direction = MovementDirection.UP
        if self.direction == MovementDirection.LEFT and self.snake_head_pos[0] < 1:
            if self.snake_head_pos[1] >= self.COORDS_HEIGHT//2:
                self.direction = MovementDirection.DOWN
            else:
                self.direction = MovementDirection.UP
 
        if self.direction == MovementDirection.DOWN and self.COORDS_HEIGHT - self.snake_head_pos[1] < 1:
            if self.snake_head_pos[0] >= self.COORDS_WIDTH//2:
                self.direction = MovementDirection.LEFT
            else:
                self.direction = MovementDirection.RIGHT
        if self.direction == MovementDirection.UP and self.snake_head_pos[1] < 1:
            if self.snake_head_pos[0] >= self.COORDS_WIDTH//2:
                self.direction = MovementDirection.LEFT
            else:
                self.direction = MovementDirection.RIGHT
#------------------
#работа с таймерами

    def timer_tick(self):
        self.time_tick += 1 
        self.damage_immune_ability_current_cd -= 1
        if self.damage_immune_ability_current_cd <= 0:
            self.damage_immune_ability_current_cd = 0
        self.damage_immune_event()

    def damage_immune_event(self):
        self.damage_immune_time -= 1
        if self.damage_immune_mode == True: 
            self.current_ms = self.base_ms + 0.5
            if self.damage_immune_time %3 == 0: 
                self.color = (255, 255, 255)   
            else:
                if self.damage_immune_is_after_hit == False:
                    self.color = (0, 0, 0)  
                else:
                    self.color = (255, 255, 0)   
        else:
            self.color = (0, 0, 255)  
        if self.damage_immune_time <= 0:
            self.damage_immune_time = 0
            self.damage_immune_mode = False
            self.current_ms = self.base_ms  
            self.damage_immune_is_after_hit = False

    def damage_immune_ability(self):  
        if self.damage_immune_ability_current_cd <= 0 and self.damage_immune_mode == False:
            self.damage_immune_ability_current_cd = self.damage_immune_ability_cd  
            self.damage_immune_mode = True
            self.damage_immune_time = 30

    def damage_immune_after_hit(self): 
        self.damage_immune_mode = True
        self.damage_immune_time = 30
        self.damage_immune_is_after_hit = True

    def set_new_space_ability_cd(self, value):
        self.damage_immune_ability_cd = value
        self.damage_immune_ability_current_cd = 0  

