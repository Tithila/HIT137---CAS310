import tkinter as tk
from tkinter import messagebox


class Video:   # Defining attribute class

    def __init__(self, title, duration):
        self.__title = title   # Attribute that captures title
        self.__duration = duration   # Attribute that captures period/time
        self.is_paused = False   # Boolean expression to track if the video is paused or not

    def PVideo(self):
        self.is_paused = False
        return f"Playing {self.__title}"

    def PauseVideo(self):
        if not self.is_paused:
            self.is_paused = True
            return f"Paused {self.__title}"
        else:
            return f"{self.__title} is already paused"

    def get_details(self):
        return f"Title: {self.__title}, Duration: {self.__duration} min"


class Playlist(tk.Frame, Video):
    def __init__(self, parent, videos):
        tk.Frame.__init__(self, parent)
        self.videos = videos   # Encapsulated playlist videos
        self.active_position = 0   # Encapsulated current video index

    def PauseVideo(self):
        return self.videos[self.active_position].PauseVideo()

    def NlineVideo(self):
        self.active_position += 1
        if self.active_position >= len(self.videos):
            self.active_position = 0
        return self.videos[self.active_position].PVideo()

    def RetVideo(self):
        self.active_position -= 1
        if self.active_position < 0:
            self.active_position = len(self.videos) - 1
        return self.videos[self.active_position].PVideo()


# Polymorphism: Adding functionality for the video app
def status(func):
    def wrapper(*args, **kwargs):
        response = messagebox.askokcancel("Verify", "Can you verify it?")
        if response:
            return func(*args, **kwargs)
        else:
            return "Operations Denied"
    return wrapper


class Grp9VidApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CAS310 Video Channel")
        self.geometry("800x600")
        self.playlist = None
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self, text="Video Channel Application", font=("Aptos", 22))
        self.title_label.pack(pady=25)

        self.load_button = tk.Button(self, text="Add video", command=self.add_video)
        self.load_button.pack(pady=25)

        self.play_button = tk.Button(self, text="Play Video", command=self.PVideo)
        self.play_button.pack(pady=25)

        self.pause_button = tk.Button(self, text="Pause Video", command=self.PauseVideo)
        self.pause_button.pack(pady=25)

        self.next_button = tk.Button(self, text="Next in Line", command=self.NlineVideo)
        self.next_button.pack(pady=25)

        self.previous_button = tk.Button(self, text="Return Video", command=self.RetVideo)
        self.previous_button.pack(pady=25)

    # Polymorphism: This PVideo method behaves differently in Playlist and Video
    @status
    def PVideo(self):
        if self.playlist:
            video = self.playlist.videos[self.playlist.active_position].PVideo()
            messagebox.showinfo("Playing", video)
        else:
            messagebox.showwarning("Error", "No playlist loaded!")

    @status
    def add_video(self):
        video1 = Video("Video 1", 10)
        video2 = Video("Video 2", 15)
        video3 = Video("Video 3", 20)
        self.playlist = Playlist(self, [video1, video2, video3])
        messagebox.showinfo("Playlist", "Playlist Loaded Successfully!")

    @status
    def PauseVideo(self):
        if self.playlist:
            video = self.playlist.PauseVideo()
            messagebox.showinfo("Pause", video)
        else:
            messagebox.showwarning("Error", "No playlist loaded!")

    @status
    def NlineVideo(self):
        if self.playlist:
            video = self.playlist.NlineVideo()
            messagebox.showinfo("Playing Next", video)
        else:
            messagebox.showwarning("Error", "No playlist loaded!")

    @status
    def RetVideo(self):
        if self.playlist:
            video = self.playlist.RetVideo()
            messagebox.showinfo("Playing Previous", video)
        else:
            messagebox.showwarning("Error", "No playlist loaded!")


# Instantiate the app and run it
if __name__ == "__main__":
    app = Grp9VidApp()
    app.mainloop()

