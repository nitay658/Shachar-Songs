import os
import time

import vlc


class Backend:
    def __init__(self):
        self.albumsList = []
        self.songsList = []
        self.user_Name = ''
        self.cmd = os.getcwd() + "/music"

    def album_select(self):
        for root, dirs, files in os.walk(self.cmd):
            for dir in dirs:
                self.albumsList.append(dir)

        return self.albumsList

    def Play_Album(self, album):
        if not self.songsList:
            cmd_ = self.cmd + "/" + self.albumsList[album - 1]
            for root, dirs, files in os.walk(cmd_):
                for file in files:
                    if file.endswith(".mp3"):
                        self.songsList.append(file)

        current_song = 0  # Initialize the current song index

        while current_song < len(self.songsList):
            # newPlayer_album(songsList[current_song], albumsList[album - 1])
            album_name = "/music/" + self.albumsList[album - 1] + "/" + self.songsList[current_song]
            album_player = Player_Reset(album_name)
            # Ask the user if they want to change the song or stop playing the album
            album_player.play()
            time.sleep(1.5)


def Player_Reset(self, name_):
    vlc_instance_ = vlc.Instance()
    player_ = vlc_instance_.media_player_new()
    media_ = vlc_instance_.media_new(name_)
    player_.set_media(media_)
    return player_
