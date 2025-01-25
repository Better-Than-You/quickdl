import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(True)

def main():
    from gui.main_window import YouTubeDownloaderApp
    import tkinter as tk
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()