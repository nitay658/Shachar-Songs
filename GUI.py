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
        self.is_playing = False

        # Create a VLC instance
        self.Instance = vlc.Instance()

        # Create a media player
        self.player = self.Instance.media_player_new()

        # Create a frame to hold the controls
        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack()

        # Create play/pause button
        self.play_pause_button = tk.Button(self.controls_frame, text="Play", command=self.toggle_play_pause)
        self.play_pause_button.pack(side=tk.LEFT)

        # Create stop button
        self.stop_button = tk.Button(self.controls_frame, text="Stop", command=self.stop)
        self.stop_button.pack(side=tk.LEFT)

        # Create a label to display the current file
        self.current_file_label = tk.Label(root, text="")
        self.current_file_label.pack()

        # Store the original order of albums
        self.original_albums = []

        # Create a listbox for albums
        self.album_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
        self.album_listbox.pack()
        self.populate_album_listbox()

        # Create a listbox for songs
        self.song_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
        self.song_listbox.pack()
        self.album_listbox.bind('<<ListboxSelect>>', self.populate_song_listbox)
        self.song_listbox.bind('<<ListboxSelect>>', self.update_selected_song_path)

        self.play_full_album_button = tk.Button(self.controls_frame, text="Play Full Album",
                                                command=self.play_full_album)
        self.play_full_album_button.pack(side=tk.LEFT)

        # Create next button
        self.next_button = tk.Button(self.controls_frame, text="Next", command=self.play_next)
        self.next_button.pack(side=tk.LEFT)

        # Create previous button
        self.previous_button = tk.Button(self.controls_frame, text="Previous", command=self.play_previous)
        self.previous_button.pack(side=tk.LEFT)

        # Initialize the selected song path
        self.selected_song_path = None

    def toggle_play_pause(self):
        if self.is_playing:
            self.pause()
        else:
            self.play()

    def play(self):
        if self.player.get_state() == vlc.State.Ended:
            self.player.stop()
        elif self.selected_song_path:
            media = self.Instance.media_new(self.selected_song_path)
            self.player.set_media(media)
            self.current_file_label.config(text=f"Playing: {self.selected_song}")
            self.player.play()
            self.is_playing = True
            self.play_pause_button.config(text="Pause")

    def pause(self):
        if self.is_playing:
            self.is_playing = False
            self.play_pause_button.config(text="Play")
            self.player.pause()

    def stop(self):
        self.is_playing = False
        self.play_pause_button.config(text="Play")
        self.player.stop()

    def populate_album_listbox(self):
        music_dir = "music"
        if os.path.exists(music_dir) and os.path.isdir(music_dir):
            self.original_albums = [album for album in os.listdir(music_dir) if
                                    os.path.isdir(os.path.join(music_dir, album))]
            for album in self.original_albums:
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
        selected_index = self.song_listbox.curselection()
        self.selected_song = ",".join([self.song_listbox.get(i) for i in selected_index])
        if self.selected_album and self.selected_song:
            album_dir = os.path.join("music", self.selected_album)
            song_path = os.path.join(album_dir, self.selected_song)
            return song_path
        return None

    def update_selected_song_path(self, event):
        self.selected_song_path = self.get_selected_song_path()

    def play_full_album(self):
        selected_album_index = self.album_listbox.curselection()
        if selected_album_index:
            selected_album = self.album_listbox.get(selected_album_index[0])
            album_dir = os.path.join("music", selected_album)
            if os.path.exists(album_dir) and os.path.isdir(album_dir):
                songs = [song for song in os.listdir(album_dir) if song.endswith(".mp3")]
                songs.sort(
                    key=lambda song: int(song.split('.')[0].strip()) if song.split('.')[0].strip().isdigit() else song)
                if songs:
                    if self.is_playing:
                        self.stop()
                        self.song_listbox.selection_clear(0, tk.END)
                    self.current_file_label.config(text="")
                    for song in songs:
                        song_path = os.path.join(album_dir, song)
                        media = self.Instance.media_new(song_path)
                        self.player.set_media(media)
                        self.current_file_label.config(text=f"Playing: {song}")
                        self.player.play()
                        self.is_playing = True
                        self.play_pause_button.config(text="Pause")

    def play_next_song(self, event):
        selected_index = self.song_listbox.curselection()
        next_index = (selected_index[0] + 1) if selected_index else 0
        self.play_next_song_at_index(next_index)

    def play_next(self):
        selected_index = self.song_listbox.curselection()
        next_index = selected_index[0] + 1 if selected_index else 0
        self.play_next_song_at_index(next_index)

    def play_next_song_at_index(self, index):
        if index < self.song_listbox.size():
            self.song_listbox.selection_clear(0, tk.END)
            self.song_listbox.selection_set(index)
            self.song_listbox.see(index)
            self.update_selected_song_path(None)
            self.play()
        else:
            self.stop()

    def play_previous(self):
        selected_index = self.song_listbox.curselection()
        if selected_index:
            prev_index = selected_index[0] - 1
            if prev_index >= 0:
                self.song_listbox.selection_clear(0, tk.END)
                self.song_listbox.selection_set(prev_index)
                self.song_listbox.see(prev_index)
                self.update_selected_song_path(None)
                self.play()
            else:
                self.stop()


if __name__ == "__main__":
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")
    root = customtkinter.CTk()
    app = VLCPlayerApp(root)
    root.mainloop()
