import pygame as pg
from misc.constants import CELL_SIZE
from objects.character_base import Character
from misc.animator import Animator


class BaseGhost(Character):
    action = {
        pg.K_UP: 'up',
        pg.K_LEFT: 'left',
        pg.K_DOWN: 'down',
        pg.K_RIGHT: 'right'
    }

    def __init__(self, game, animator: Animator, start_pos: tuple, animations, enable_collision=True, max_count_eat_seeds_in_home=0):
        super().__init__(game, animator, start_pos)
        self.animations = animations
        self.enable_collision = enable_collision
        self.count_eat_seeds_in_home = 0
        self.max_count_eat_seeds_in_home = max_count_eat_seeds_in_home
        self.timer = pg.time.get_ticks()

    def process_event(self, event):
        if event.type == pg.KEYDOWN and event.key in self.action.keys():
            self.go()
            self.feature_direction = self.action[event.key]


    def process_logic(self):
        self.animator.timer_check()
        if self.in_center() and self.enable_collision:
            if self.move_to(self.rotate):
                self.go()
            else:
                self.stop()
            c = self.direction[self.feature_direction][2]
            if self.move_to(c):
                self.set_direction(self.feature_direction)
        if self.rotate is None:
            self.rotate = 0
        self.animator = self.animations[self.rotate]
        super().process_logic()

    def collision_check(self, object): #pacman only
        return self.rect.centerx//CELL_SIZE == object.rect.centerx//CELL_SIZE and self.rect.centery//CELL_SIZE == object.rect.centery//CELL_SIZE and self.enable_collision

    def counter(self):
        self.count_eat_seeds_in_home += 1

    def can_leave_home(self):
        #print(self.max_count_eat_seeds_in_home, ': ', pg.time.get_ticks()-self.timer)
        return self.count_eat_seeds_in_home >= self.max_count_eat_seeds_in_home or pg.time.get_ticks()-self.timer >= 4000

    def update_timer(self):
        self.timer = pg.time.get_ticks()

    def invisible(self):
        pass
