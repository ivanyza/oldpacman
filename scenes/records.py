import pygame as pg

from misc import Color, Font, get_image_path
from objects import Button, ButtonController, ImageObject, Text
from scenes import BaseScene


class RecordsScene(BaseScene):
    def create_objects(self) -> None:
        self.__create_title()
        self.__create_error_label()
        self.create_text_labels()
        self.__create_medals()
        self.__create_buttons()

    def create_text_labels(self) -> None:
        self.game.records.update_records()
        self.__one_text = Text(self.game, str(self.game.records.data[4]), 30, (60, 55), Color.GOLD)
        self.__two_text = Text(self.game, str(self.game.records.data[3]), 30, (60, 85), Color.SILVER)
        self.__three_text = Text(self.game, str(self.game.records.data[2]), 30, (60, 120), Color.BRONZE)
        self.__four_text = Text(self.game, str(self.game.records.data[1]), 30, (60, 155), Color.WHITE)
        self.__five_text = Text(self.game, str(self.game.records.data[0]), 30, (60, 190), Color.WHITE)

    def __create_medals(self) -> None:
        self.__gold_medal = ImageObject(self.game, get_image_path('1_golden', 'medal'), 16, 55)
        self.__gold_medal.scale(35, 35)
        self.__silver_medal = ImageObject(self.game, get_image_path('2_silver', 'medal'), 16, 85)
        self.__silver_medal.scale(35, 35)
        self.__bronze_medal = ImageObject(self.game, get_image_path('3_bronze', 'medal'), 16, 120)
        self.__bronze_medal.scale(35, 35)
        self.__stone_medal = ImageObject(self.game, get_image_path('4_stone', 'medal'), 16, 155)
        self.__stone_medal.scale(35, 35)
        self.__wooden_medal = ImageObject(self.game, get_image_path('5_wooden', 'medal'), 16, 190)
        self.__wooden_medal.scale(35, 35)

    def __create_buttons(self) -> None:
        self.back_button = Button(self.game, pg.Rect(0, 0, 180, 40),
                                  self.__start_menu, 'MENU', center=(self.game.width // 2, 250),
                                  text_size=Font.BUTTON_TEXT_SIZE)
        self.__button_controller = ButtonController(self.game, [self.back_button])
        self.objects.append(self.__button_controller)

    def __create_title(self) -> None:
        title = Text(self.game, 'RECORDS', 32, color=Color.WHITE, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)
        self.objects.append(title)

    def __create_error_label(self) -> None:
        self.__error_text = Text(self.game, 'NO RECORDS', 24, color=Color.RED)
        self.__error_text.move_center(self.game.width // 2, 100)

    def __start_menu(self) -> None:
        self.game.set_scene(self.game.scenes.SCENE_MENU)

    def on_activate(self) -> None:
        self.__button_controller.reset_state()

    def process_draw(self) -> None:
        super().process_draw()

        if self.game.records.data[4] == 0:
            self.__error_text.process_draw()

        if self.game.records.data[4] != 0:
            self.__one_text.process_draw()
            self.__gold_medal.process_draw()

        if self.game.records.data[3] != 0:
            self.__two_text.process_draw()
            self.__silver_medal.process_draw()

        if self.game.records.data[2] != 0:
            self.__three_text.process_draw()
            self.__bronze_medal.process_draw()

        if self.game.records.data[1] != 0:
            self.__four_text.process_draw()
            self.__stone_medal.process_draw()

        if self.game.records.data[0] != 0:
            self.__five_text.process_draw()
            self.__wooden_medal.process_draw()

    def additional_event_check(self, event: pg.event.Event) -> None:
        if self.game.current_scene == self:
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.game.set_scene(self.game.scenes.SCENE_MENU)
