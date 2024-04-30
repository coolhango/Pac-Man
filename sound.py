import pygame as pg
from pygame import mixer
import time


class Sound:
    def __init__(self, game):
        self.game = game
        mixer.init()
        # self.ship_laser = mixer.Sound("sounds/ship_laser.wav")
        self.waka_waka = mixer.Sound("sounds/waka_waka.wav")
        self.waka_channel = pg.mixer.Channel(1)
        self.eating_ghost = mixer.Sound("sounds/eating_ghost.wav")
        self.current_song = 0
        self.songs = ["sounds/Melody.wav", "sounds/koala.wav", "sounds/This_Groove.wav"]
        self.volume = 0.25
        self.set_volume(self.volume)
        # self.set_effects_volume(ship=0.15)

    def reset(self):
        self.current_song = 0
        self.set_volume(self.volume)

    def select_song(self):
        if self.current_song == (len(self.songs) - 1):
            self.current_song = 0
        else:
            self.current_song += 1
        return self.songs[self.current_song]

    # def set_effects_volume(self, ship=0.25):
    # self.ship_laser.set_volume(ship)

    def set_volume(self, volume=0.3):
        mixer.music.set_volume(volume)

    def play_music(self, filename):
        self.stop_music()
        mixer.music.load(filename)
        mixer.music.play(-1)

    def play_once(self, filename):
        self.stop_music()
        mixer.music.load(filename)
        mixer.music.play(0)

    def pause_music(self):
        mixer.music.pause()

    def unpause_music(self):
        mixer.music.unpause()

    def stop_music(self):
        mixer.music.stop()

    def play_start_up(self):
        self.stop_music()
        self.play_once("sounds/start_up.wav")
        time.sleep(5)

    def play_waka_waka(self):
        if not self.waka_channel.get_busy():
            self.waka_channel.play(self.waka_waka)

    def play_eating_ghost(self):
        self.pause_music()
        mixer.Sound.play(self.eating_ghost)
        time.sleep(0.1)
        self.unpause_music()

    def play_ship_laser(self):
        mixer.Sound.play(self.ship_laser)

    def play_game_over(self):
        self.stop_music()
        self.ship_laser.stop()
        self.alien_laser.stop()
        self.set_volume(1)
        self.play_once("sounds/gameover.wav")
        # have to sleep for however long the last sound is...
        time.sleep(3)
        self.set_volume(self.volume)
        self.stop_music()


if __name__ == "__main__":
    print("\nERROR: sound.py is the wrong file! Run play from game.py\n")
