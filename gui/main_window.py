# gui/main_window.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from downloader.download_manager import DownloadManager

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("450x400")
        self.root.configure(bg="#f5f5f5")  # Light gray background

        # Initialize styles
        self.configure_styles()

        # Create GUI components
        self.create_widgets()

    def configure_styles(self):
        from .styles import configure_styles
        configure_styles()

    def create_widgets(self):
        # URL Entry
        url_label = ttk.Label(self.root, text="YouTube URL:")
        url_label.pack(pady=(20, 5))
        self.url_entry = ttk.Entry(self.root, width=50, font=("Segoe UI", 10))
        self.url_entry.pack(pady=5, ipady=5)  # Add internal padding for better appearance

        # Placeholder frame for resolution label and combobox
        self.resolution_frame = ttk.Frame(self.root)
        self.resolution_frame.pack(pady=(10, 5))

        # Resolution Label
        self.resolution_label = ttk.Label(self.resolution_frame, text="Resolution:")
        self.resolution_label.pack(side=tk.LEFT, padx=5)

        # Resolution Dropdown
        resolutions = ["144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"]
        self.resolution_var = tk.StringVar(value="1080p")  # Default to 1080p
        self.resolution_combobox = ttk.Combobox(self.resolution_frame, textvariable=self.resolution_var, values=resolutions, state="readonly")
        self.resolution_combobox.pack(side=tk.LEFT, padx=5)

        # Audio Options
        self.audio_var = tk.StringVar(value="with_audio")  # Default to "With Audio"
        self.audio_var.trace_add("write", self.toggle_resolution_visibility)  # Add trace to handle visibility
        audio_frame = ttk.Frame(self.root)
        audio_frame.pack(pady=(10, 5))

        audio_with = ttk.Radiobutton(
            audio_frame, text="With Audio", variable=self.audio_var, value="with_audio", style="TRadiobutton"
        )
        audio_with.pack(side=tk.LEFT, padx=10)

        audio_without = ttk.Radiobutton(
            audio_frame, text="No Audio", variable=self.audio_var, value="no_audio", style="TRadiobutton"
        )
        audio_without.pack(side=tk.LEFT, padx=10)

        audio_only = ttk.Radiobutton(
            audio_frame, text="Audio Only", variable=self.audio_var, value="audio_only", style="TRadiobutton"
        )
        audio_only.pack(side=tk.LEFT, padx=10)

        # Progress Bar
        self.progress_label = ttk.Label(self.root, text="", font=("Segoe UI", 10))
        self.progress_label.pack(pady=(10, 5))

        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=5)

        # Download Button
        download_button = ttk.Button(
            self.root,
            text="Download",
            style="TButton",
            command=self.handle_download_click  # Call the download function
        )
        download_button.pack(pady=20)

        # Add a subtle border around the main content
        main_frame = ttk.Frame(self.root, padding="20", style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)

    def handle_download_click(self):
        self.progress_label.config(text="Starting download...")
        self.start_download()
    
    def toggle_resolution_visibility(self, *args):
        if self.audio_var.get() == "audio_only":
            # Hide the resolution label and combobox
            self.resolution_label.pack_forget()
            self.resolution_combobox.pack_forget()
        else:
            # Show the resolution label and combobox
            self.resolution_label.pack(side=tk.LEFT, padx=5)
            self.resolution_combobox.pack(side=tk.LEFT, padx=5)
    def start_download(self):
        # Get all parameters from the GUI
        url = self.url_entry.get()
        resolution = self.resolution_var.get()
        include_audio = self.audio_var.get()
        
        # Validate the URL
        if not DownloadManager.is_yt_url(url=url):
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return

        # Ask the user where to save the file
        # Suggest a default filename based on the video title
        video_title = DownloadManager.get_video_title(url)
        if include_audio == "audio_only":
            default_filename = f"{video_title}.mp3" if video_title else "audio.mp3"
            defaultextension = ".mp3"
            filetypes = [("MP3 files", "*.mp3"), ("All files", "*.*")]
        else:
            default_filename = f"{video_title}.mp4" if video_title else "video.mp4"
            defaultextension = ".mp4"
            filetypes = [("MP4 files", "*.mp4"), ("All files", "*.*")]

        output_path = filedialog.asksaveasfilename(
            defaultextension=defaultextension,
            filetypes=filetypes,
            initialfile=default_filename,
            title="Save Video As"
        )

        # If the user cancels the file dialog, return
        if not output_path:
            return

        # Reset progress bar
        self.progress_bar["value"] = 0

        # Initialize the download manager
        self.download_manager = DownloadManager()

        # Start the download in a separate thread
        download_thread = threading.Thread(
            target=self.download_manager.start_download,
            args=(url, resolution, include_audio, output_path, self.update_progress, self.on_download_complete),
            daemon=True
        )
        download_thread.start()

    
    #this function 
    def update_progress(self, progress, status='Download'):
        # Update progress bar and label
        self.progress_bar["value"] = progress
        self.progress_label.config(text=f"{status} progress: {int(progress)}%")
        self.root.update_idletasks()  # Refresh the GUI

    def on_download_complete(self, success, message):
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

        # Reset progress bar after download
        self.progress_bar["value"] = 0
        self.progress_label.config(text="Download progress")