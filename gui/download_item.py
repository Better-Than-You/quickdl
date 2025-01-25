# gui/download_item.py
import tkinter as tk
from tkinter import ttk

class DownloadItem(ttk.Frame):
    def __init__(self, parent, on_download):
        super().__init__(parent)
        self.on_download = on_download
        self.create_widgets()

    def create_widgets(self):
        # URL Entry
        self.url_label = ttk.Label(self, text="YouTube URL:")
        self.url_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.url_entry = ttk.Entry(self, width=40)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)

        # Resolution Selection
        self.resolution_label = ttk.Label(self, text="Resolution:")
        self.resolution_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.resolution_var = tk.StringVar(value="1080p")
        self.resolution_combobox = ttk.Combobox(
            self, textvariable=self.resolution_var, values=["144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"], state="readonly"
        )
        self.resolution_combobox.grid(row=1, column=1, padx=5, pady=5)

        # Audio Options
        self.audio_var = tk.BooleanVar(value=True)
        self.audio_with = ttk.Radiobutton(self, text="With Audio", variable=self.audio_var, value=True)
        self.audio_with.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.audio_without = ttk.Radiobutton(self, text="No Audio", variable=self.audio_var, value=False)
        self.audio_without.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Progress Bar
        self.progress_label = ttk.Label(self, text="Download progress: 0%")
        self.progress_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Download Button
        self.download_button = ttk.Button(self, text="Download", command=self.start_download)
        self.download_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

    def start_download(self):
        url = self.url_entry.get()
        resolution = self.resolution_var.get()
        include_audio = self.audio_var.get()
        self.on_download(url, resolution, include_audio, self.update_progress)

    def update_progress(self, progress):
        self.progress_bar["value"] = progress
        self.progress_label.config(text=f"Download progress: {int(progress)}%")