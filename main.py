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


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    # print("Please choose a song to play")


def newPlayer(name, dir):
    name1 = "/music/" + dir + "/" + name
    vlc_instance = vlc.Instance()
    player = vlc_instance.media_player_new()
    media = vlc_instance.media_new(name1)
    player.set_media(media)
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
    # print(cmd)
    for root, dirs, files in os.walk(cmd):
        for dir in dirs:
            print(i, ".  " + dir)
            albumsList.append(dir)
            i = i + 1
    album = input("Select Album number:  for break parse -1\n")
    album = int(album)
    if album >= i:
        print("select valid number")
        return album_select()
    else:
        return album


def song_select(album):
    i = 1
    # print(album)
    print("\n")
    cmd2 = cmd + "/" + albumsList[album - 1]
    for root, dirs, files in os.walk(cmd2):
        for file in files:
            if file.endswith(".mp3"):
                songsList.append(file)
                file = file[:-4]
                print(file)
                i = i + 1
    song = input("select song number:  for break parse -1 \n")
    song = int(song)
    if value >= i:
        print("select valid number")
        song_select()
    else:
        return song


def Pick_A_Song(number):
    # print_hi(user_Name)
    album = album_select()
    if album == -1:
        return
    if number == 1:
        song = song_select(album)
        if song == -1:
            return
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
        answer = input("Do you want to stop playing this album?  yes/no \n")
        if answer == "yes":
            break


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # user_Name = input("Insert user Name: \n")
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
