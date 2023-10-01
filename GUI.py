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
        self.album_listbox.pack(fill=tk.BOTH, expand=True)

        # Add scrollbars to the listbox
        self.album_listbox_scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=self.album_listbox.yview)
        self.album_listbox.config(yscrollcommand=self.album_listbox_scrollbar.set)
        self.album_listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a button to open the album selection dialog
        self.select_button = ttk.Button(root, text="Play an album", command=self.open_album_selection)
        self.select_button.pack()

        # Initialize albumsList with sample data
        self.bd = Backend.Backend()
        self.albumsList = self.bd.album_select()  # Replace with your album list
        var = tk.Variable(value=self.albumsList)
        # Populate the listbox with album names
        for album in self.albumsList:
            self.album_listbox.insert(tk.END, f"{album}")

    def open_album_selection(self):
        selected_index = self.album_listbox.curselection()
        selected = ",".join([self.album_listbox.get(i) for i in selected_index])
        print(selected)
        msg = f'You selected: {selected}'
        showinfo(title='Information', message=msg)
        self.bd.Play_Album(selected)


def main():
    root = tk.Tk()
    app = MusicPlayerApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
