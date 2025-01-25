# YouTube Downloader

A simple and efficient YouTube video downloader with a graphical user interface (GUI) built using Tkinter. This application allows you to download YouTube videos in various resolutions and formats, including audio-only options. Future updates will include Instagram video downloading.

## Features

- Download YouTube videos in different resolutions (144p, 240p, 360p, 480p, 720p, 1080p, 1440p, 2160p).
- Option to download videos with or without audio.
- Option to download audio-only files in MP3 format.
- Progress bar to show download and conversion progress.
- User-friendly GUI built with Tkinter.
- Future support for Instagram video downloading.

## Requirements

- Python 3.x
- `yt-dlp`
- `ffmpeg`
- `tkinter`
- `ffmpeg-progress-yield`

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/youtube-downloader.git
    cd youtube-downloader
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Ensure `ffmpeg` is installed and available in your system's PATH. You can download it from [FFmpeg's official website](https://ffmpeg.org/download.html).

## Usage

1. Run the application:

    ```bash
    python main.py
    ```

2. Enter the YouTube URL, select the desired resolution, and choose whether to include audio or download audio-only.

3. Click the "Download" button and select the location to save the file.

4. The progress bar will show the download and conversion progress. Once complete, a success message will be displayed.

## Project Structure

```plaintext
youtube-downloader/
├── downloader/
│   ├── __init__.py
│   ├── download_manager.py
│   └── download_task.py
├── gui/
│   ├── __init__.py
│   ├── download_item.py
│   ├── main_window.py
│   └── styles.py
├── __pycache__/
├── .gitignore
├── main.py
├── README.md
└── requirements.txt