# main.py
import tkinter as tk
from gui.main_window import YouTubeDownloaderApp
import ctypes

if __name__ == "__main__":
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()