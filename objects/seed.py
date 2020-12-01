from typing import Tuple

import pygame as pg
from misc import CELL_SIZE, Color, Sounds
from objects import DrawableObject
from scenes import base


class SeedContainer(DrawableObject):
    eaten_sound = Sounds.SEED
    gameover_sound = Sounds.GAMEOVER

    def __init__(self, game, seed_data, energizer_data, x=0, y=20) -> None:
        super().__init__(game)
        self.__x = x
        self.__y = y
        self.__seeds = seed_data
        self.__energizers = energizer_data
        self.__color = {
            -1: Color.WHITE,
            1: Color.BLACK
        }
        self.__index_color = 1
        self.__seeds_on_field = 0
        for row in range(len(self.__seeds)):
            for col in range(len(self.__seeds[row])):
                if self.__seeds[row][col]:
                    self.__seeds_on_field += 1

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __draw_seeds(self) -> None:
        for row in range(len(self.__seeds)):
            for col in range(len(self.__seeds[row])):
                if self.__seeds[row][col]:
                    pg.draw.circle(self.game.screen, Color.WHITE, (self.__x + col * CELL_SIZE + CELL_SIZE // 2,
                                                                   self.y + row * CELL_SIZE + CELL_SIZE // 2), 1)

    def __draw_energizers(self) -> None:
        if pg.time.get_ticks() - self.game.animate_timer > self.game.time_out:
            self.game.animate_timer = pg.time.get_ticks()
            self.__index_color *= -1
        for energizer in self.__energizers:
            pg.draw.circle(self.game.screen, self.__color[self.__index_color],
                           (self.x + energizer[0] * CELL_SIZE + CELL_SIZE // 2,
                            self.y + energizer[1] * CELL_SIZE + CELL_SIZE // 2), 4)

    def process_draw(self) -> None:
        self.__draw_seeds()
        self.__draw_energizers()

    def process_collision(self, object) -> bool:
        """
        :param object: any class with pygame.rect
        :return: is objects in collision (bool) and self type (str)
        """
        for row in range(len(self.__seeds)):
            for col in range(len(self.__seeds[row])):
                if self.__seeds[row][col] and row * CELL_SIZE + 18 == object.rect.y:
                    if col * CELL_SIZE - 2 == object.rect.x:
                        self.__seeds[row][col] = None
                        if not pg.mixer.Channel(0).get_busy():
                            self.eaten_sound.play()
                        self.game.score.eat_seed()
                        self.__seeds_on_field -= 1
                        return True
        for energizer in self.__energizers:
            if energizer[1] * CELL_SIZE + 18 == object.rect.y:
                if energizer[0] * CELL_SIZE - 2 == object.rect.x:
                    self.__energizers.remove(energizer)
                    self.game.score.eat_energizer()
                    return True

    def is_field_empty(self) -> bool:
        print(self.__seeds_on_field)
        if self.__seeds_on_field == 0:
            return True
        return False



