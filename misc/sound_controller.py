import pygame as pg


def update(object):
    object.update_volume()


class SoundController:
    def __init__(self, game, sound, channel: int = 0, volume: int = 1):
        self.sound = sound
        self.game = game
        self.volume = volume
        self.channel = pg.mixer.Channel(channel)
        self.update()

    def update(self):
        self.volume = 0 if not self.game.settings.MUTE else self.game.settings.VOLUME / 100
        self.sound.set_volume(self.volume)

    def play(self):
        self.sound.set_volume(self.volume)
        self.channel.play(self.sound)

    def pause(self):
        self.channel.pause()

    def unpause(self):
        self.channel.unpause()

    def stop(self):
        self.channel.stop()

    def get_busy(self):
        return self.channel.get_busy()
