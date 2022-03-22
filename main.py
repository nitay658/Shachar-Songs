# This is a sample Python script.
import os
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
song = -1
album = -1


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    # print("Please choose a song to play")


def newPlayer(name, dir):
    name = "/music/" + dir + "/" + name
    # print(name)
    vlc_instance = vlc.Instance()
    player = vlc_instance.media_player_new()
    media = vlc_instance.media_new(name)
    player.set_media(media)
    player.play()
    time.sleep(1.5)
    duration = player.get_length() / 1000
    time.sleep(duration)
    player.stop()


def album_select():
    i = 1
    # print(cmd)
    for root, dirs, files in os.walk(cmd):
        for dir in dirs:
            print(i, ".  " + dir)
            albumsList.append(dir)
            i = i + 1
    album = input("Select Album number:\n")
    album = int(album)
    if album >= i:
        print("select valid number")
        return album_select()
    else:
        return album


def song_select(album):
    i = 1
    print(album)
    cmd2 = cmd + "/" + albumsList[album - 1]
    for root, dirs, files in os.walk(cmd2):
        for file in files:
            if file.endswith(".mp3"):
                songsList.append(file)
                file = file[:-4]
                print(file)
                i = i + 1
    song = input("select song number:\n")
    song = int(song)
    if value >= i:
        print("select valid number")
        song_select()
    else:
        return


def Pick_A_Song(number):
    print_hi(user_Name)
    album = album_select()
    if number == 1:
        song_select(album)
        newPlayer(songsList[song - 1], albumsList[album - 1])
    elif number == 3:
        Play_Album(album)


def Play_Album(album):
    if not songsList:
        print(album)
        cmd2 = cmd + "/" + albumsList[album - 1]
        for root, dirs, files in os.walk(cmd2):
            for file in files:
                if file.endswith(".mp3"):
                    songsList.append(file)
    for x in range(len(songsList)):
        newPlayer(songsList[x], albumsList[album - 1])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    user_Name = input("Insert user Name: \n")
    bool = True
    while bool:
        value = input("What would you like to do:\n1. Play a song.\n2. End program.\n3. play a album\n")
        value = int(value)
        if value == 1:
            Pick_A_Song(1)
        elif value == 2:
            bool = False
        elif value == 3:
            Pick_A_Song(3)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
