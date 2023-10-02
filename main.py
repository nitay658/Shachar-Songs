# This is a sample Python script.
import os
import select
import signal
import sys
import threading
import time

import vlc

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Global Variables
albumsList = []
songsList = []
user_Name = ''
cmd = os.getcwd() + "/music"
cmd2 = ''
album = -1
TIMEOUT = 5

playAlbum = 2
playSong = 1
exIt = 3
goback = -1


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    # print("Please choose a song to play")


def Player_Reset(name_):
    vlc_instance_ = vlc.Instance()
    player_ = vlc_instance_.media_player_new()
    media_ = vlc_instance_.media_new(name_)
    player_.set_media(media_)
    return player_


def newPlayer(name, dir):
    name1 = "/music/" + dir + "/" + name
    print("name1:  "+name1)
    player = Player_Reset(name1)
    player.play()
    time.sleep(1.5)
    answer = ""
    while player.is_playing():
        if answer != "pa":
            answer = input(name + " is playing...\ns - stop\npa - pause\nInput something : ")
            if answer == "pa":
                player.pause()
                print(player.is_playing())
            if answer == "s":
                player.stop()
        else:
            answer = input(name + " is pausing...\ns - stop\npl - play\nInput something : ")
            if answer == "s":
                player.stop()
            if answer == "pl":
                player.play()
                time.sleep(1.5)
    player.stop()


def album_select():
    i = 1
    for root, dirs, files in os.walk(cmd):
        for dir in dirs:
            print(i, ".  " + dir)
            albumsList.append(dir)
            i = i + 1
    album = input("Select Album number:  for break parse -1\n")
    album = int(album)
    if album >= len(albumsList):
        print("select valid number")
        return album_select()
    else:
        return album


def song_select(album):
    print("\n")
    cmd2 = cmd + "/" + albumsList[album - 1]
    for root, dirs, files in os.walk(cmd2):
        for file in files:
            if file.endswith(".mp3"):
                songsList.append(file)
                file = file[:-4]
                print(file)
    song = input("select song number:  for break parse -1 \n")
    song = int(song)
    if value >= len(songsList):
        print("select valid number")
        song_select()
    else:
        return song


def Pick_A_Song(number):
    album = album_select()
    if album == goback:
        return
    if number == playSong:
        song = song_select(album)
        if song == goback:
            return
        newPlayer(songsList[song - 1], albumsList[album - 1])
    elif number == playAlbum:
        Play_Album(album)


def Play_Album(album):
    if not songsList:
        cmd_ = cmd + "/" + albumsList[album - 1]
        for root, dirs, files in os.walk(cmd_):
            for file in files:
                if file.endswith(".mp3"):
                    songsList.append(file)

    current_song = 0  # Initialize the current song index

    while current_song < len(songsList):
        # newPlayer_album(songsList[current_song], albumsList[album - 1])
        album_name = "/music/" + albumsList[album - 1] + "/" + songsList[current_song]
        album_player = Player_Reset(album_name)
        # Ask the user if they want to change the song or stop playing the album
        album_player.play()
        time.sleep(1.5)
        album_answer = ""

        while album_player.is_playing():
            if album_answer != "pa":
                album_answer = input("Options:\n"
                                     "1. Next song\n"
                                     "2. Stop playing this album\n"
                                     "pa - pause\n"
                                     "Enter your choice: ")
                if album_answer == "pa":
                    album_player.pause()
            else:
                album_answer = input("Options:\n"
                                     "1. Next song\n"
                                     "2. Stop playing this album\n"
                                     "pl - play\n"
                                     "Enter your choice: ")
                if album_answer == "pl":
                    album_player.play()
                    time.sleep(1.5)

            if album_answer == "1":
                current_song += 1  # Move to the next song
                album_player.stop()
            elif album_answer == "2":
                current_song = len(songsList)
                album_player.stop()
                # Stop playing the album if the user chooses to do so


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # user_Name = input("Insert user Name: \n")
    bool = True
    while bool:
        value = input("What would you like to do:\n1. Play a song.\n2. Play an album.\n3. End program.\n")
        value = int(value)
        if value == playSong or value == playAlbum:
            Pick_A_Song(value)
        elif value == exIt:
            bool = False
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
