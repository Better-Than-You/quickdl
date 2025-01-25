# downloader/download_manager.py
from .download_task import DownloadTask
import re

class DownloadManager:
    def __init__(self):
        self.task = None

    def get_video_title(url):
        return DownloadTask.get_video_title(url)
    
    def is_yt_url(url):
        yt_url_regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$"
        return re.match(yt_url_regex, url) is not None
    
    def start_download(self, url, resolution, include_audio, output_path, progress_callback, completion_callback):
        self.task = DownloadTask(url, resolution, include_audio, output_path, progress_callback, completion_callback)
        self.task.start()