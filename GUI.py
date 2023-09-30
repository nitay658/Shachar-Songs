import tkinter as tk
from tkinter import ttk
import Backend as Backend
import os
import time
import vlc
from tkinter import filedialog
import main as player


class MusicPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")

        # Create and configure a label
        self.root.geometry("200x200")
        self.label = ttk.Label(root, text="Have Fun:")
        self.label.pack(pady=10)

        # Create a button to open a file dialog for selecting the music directory
        self.Play_a_song_button = ttk.Button(root, text="Play a song", command=self.Play_a_song)
        self.Play_a_song_button.pack()

        # Create a button to start the music player
        self.Play_a_album_button = ttk.Button(root, text="Play an album", command=self.Play_a_album)
        self.Play_a_album_button.pack()

    def Play_a_song(self):
        bd = Backend.Backend()
        album = bd.album_select()

    def Play_a_album(self):
        bd = Backend.Backend()
        albumList = bd.album_select()
        # Get the selected index from the listbox
        selected_index = albumList.curselection()

        if selected_index:
            # Extract the selected album's index
            album_index = selected_index[0]
            album = albumList[int(album_index)]
            self.show_selected_album(album)
        else:
            # No album selected, show an error message
            self.show_error("Please select an album.")





def main():
    root = tk.Tk()
    app = MusicPlayerApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
