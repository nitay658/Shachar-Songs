import tkinter as tk
import vlc
import os
import customtkinter


class VLCPlayerApp:
    def __init__(self, root_):
        self.root = root_
        self.root.title("VLC Music Player")
        self.selected_album = ""
        self.selected_song = ""
        self.is_pause = False

        # Create a VLC instance
        self.Instance = vlc.Instance()

        # Create a media player
        self.player = self.Instance.media_player_new()

        # Create a frame to hold the controls
        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack()

        # Create play button
        self.play_button = tk.Button(self.controls_frame, text="Play", command=self.play)

        self.play_button.pack(side=tk.LEFT)

        # Create pause button
        self.pause_button = tk.Button(self.controls_frame, text="Pause", command=self.pause)
        self.pause_button.pack(side=tk.LEFT)

        # Create stop button
        self.stop_button = tk.Button(self.controls_frame, text="Stop", command=self.stop)
        self.stop_button.pack(side=tk.LEFT)

        # Create a label to display the current file
        self.current_file_label = tk.Label(root, text="")
        self.current_file_label.pack()

        # Create a listbox for albums
        self.album_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
        self.album_listbox.pack()
        self.populate_album_listbox()

        # Create a listbox for songs
        self.song_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
        self.song_listbox.pack()
        self.album_listbox.bind('<<ListboxSelect>>', self.populate_song_listbox)
        self.song_listbox.bind('<<ListboxSelect>>', self.update_selected_song_path)

        # Initialize the selected song path
        self.selected_song_path = None

    def play(self):
        if self.is_pause:
            self.player.play()
            self.is_pause = False
        elif self.player.get_state() == vlc.State.Ended:
            self.player.stop()
        elif self.selected_song_path:
            media = self.Instance.media_new(self.selected_song_path)
            self.player.set_media(media)
            self.current_file_label.config(text=f"Playing: {self.selected_song}")
            self.player.play()

    def pause(self):
        self.is_pause = True
        self.player.pause()

    def stop(self):
        # print("stop")
        self.player.stop()

    def populate_album_listbox(self):
        music_dir = "music"
        if os.path.exists(music_dir) and os.path.isdir(music_dir):
            albums = [album for album in os.listdir(music_dir) if os.path.isdir(os.path.join(music_dir, album))]
            for album in albums:
                self.album_listbox.insert(tk.END, album)

    def populate_song_listbox(self, event):
        selected_album_indices = self.album_listbox.curselection()
        if selected_album_indices:
            selected_album_index = selected_album_indices[0]
            self.selected_album = self.album_listbox.get(selected_album_index)
            if self.selected_album:
                album_dir = os.path.join("music", self.selected_album)
                if os.path.exists(album_dir) and os.path.isdir(album_dir):
                    songs = [song for song in os.listdir(album_dir) if song.endswith(".mp3")]
                    self.song_listbox.delete(0, tk.END)
                    for song in songs:
                        self.song_listbox.insert(tk.END, song)

    def get_selected_song_path(self):
        # selected_album = self.album_listbox.get(self.album_listbox.curselection())
        selected_index = self.song_listbox.curselection()
        self.selected_song = ",".join([self.song_listbox.get(i) for i in selected_index])

        # print("102")
        # print("selected_album: " + self.selected_album)
        # print("selected_song: " + self.selected_song)
        if self.selected_album and self.selected_song:
            # print("104")
            album_dir = os.path.join("music", self.selected_album)
            song_path = os.path.join(album_dir, self.selected_song)
            return song_path
        return None

    def update_selected_song_path(self, event):
        self.selected_song_path = self.get_selected_song_path()


if __name__ == "__main__":
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")
    root = customtkinter.CTk()
    app = VLCPlayerApp(root)
    root.mainloop()
