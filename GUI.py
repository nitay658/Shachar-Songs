import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

import Backend


class MusicPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")

        # Set the window size
        self.root.geometry("400x300")

        # Create a listbox to display album options
        self.album_listbox = tk.Listbox(root)
        self.album_listbox.bind("<<ListboxSelect>>", self.OnSelectAlbum)
        self.album_listbox.pack(fill=tk.BOTH, expand=True)

        self.song_listbox = None

        # Add scrollbars to the listbox
        self.album_listbox_scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=self.album_listbox.yview)
        self.album_listbox.config(yscrollcommand=self.album_listbox_scrollbar.set)
        self.album_listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a button to open the album selection dialog
        self.select_button = ttk.Button(root, text="Play an album", command=self.open_album_selection)
        self.select_button.pack()

        # Create a button to open the song selection dialog
        self.select_button = ttk.Button(root, text="Play a song", command=self.open_song_selection)
        self.select_button.pack()

        # Initialize albumsList with sample data
        self.bd = Backend.Backend()
        self.albumsList = self.bd.album_select()  # Replace with your album list
        # var = tk.Variable(value=self.albumsList)
        self.selected = None
        self.selected_song = None
        # Populate the listbox with album names
        for album in self.albumsList:
            self.album_listbox.insert(tk.END, f"{album}")

    def OnSelectAlbum(self, event):
        selected_index = self.album_listbox.curselection()
        self.selected = ",".join([self.album_listbox.get(i) for i in selected_index])
        # print(self.selected)

    def OnSelectSong(self, event):
        selected_index = self.song_listbox.curselection()
        self.selected_song = ",".join([self.song_listbox.get(i) for i in selected_index])
        print(self.selected_song)
        self.bd.Play_Song(self.selected, self.selected_song)
        # if self.song_listbox is not None:
        #    self.song_listbox.delete(0, tk.END)

    def open_album_selection(self):
        print(self.selected)
        if self.selected != "":
            msg = f'You selected: {self.selected}'
            showinfo(title='Information', message=msg)
            self.bd.Play_Album(self.selected)
            showinfo(title='Information', message="ended playing album")
        else:
            warning_msg_album_miss()

    def open_song_selection(self):
        # Create a listbox to display songs options
        # print(self.selected)
        if self.selected != "":
            self.song_listbox = tk.Listbox(self.root)
            self.bd = Backend.Backend()
            songList = self.bd.song_select(self.selected)  # Replace with your album list
            # var = tk.Variable(value=songList)
            # Populate the listbox with album names
            for song in songList:
                self.song_listbox.insert(tk.END, f"{song[:-4]}")
            self.song_listbox.bind("<<ListboxSelect>>", self.OnSelectSong)
            self.song_listbox.pack(fill=tk.BOTH, expand=True)
        else:
            warning_msg_album_miss()


def main():
    root = tk.Tk()
    app = MusicPlayerApp(root)
    root.mainloop()


def warning_msg_album_miss():
    msg = f'You do not selected an album....'
    showinfo(title='Information', message=msg)


if __name__ == '__main__':
    main()
