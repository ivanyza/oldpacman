import pygame as pg

from misc.path import get_image_path_for_animator
from objects.character_base import Character
from misc.animator import Animator


class BaseGhost(Character):
    action = {
        pg.K_UP: 'up',
        pg.K_LEFT: 'left',
        pg.K_DOWN: 'down',
        pg.K_RIGHT: 'right'
    }

    def __init__(self, game, animator: Animator, start_pos: tuple, animations, enable_collision=True):
        super().__init__(game, animator, start_pos)
        self.animations = animations
        self.enable_collision = enable_collision

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
        self.animator = self.animations[self.rotate]
        super().process_logic()
