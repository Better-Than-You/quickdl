# downloader/download_task.py
import yt_dlp
import re
import os
import subprocess
from ffmpeg_progress_yield import FfmpegProgress


class DownloadTask:
    def __init__(self, url, resolution, include_audio, output_path, progress_callback, completion_callback):
        self.url = url
        self.resolution = resolution
        self.include_audio = include_audio
        self.output_path = output_path
        self.progress_callback = progress_callback
        self.completion_callback = completion_callback
    
    def get_video_title(url):
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
            cleaned_title = re.sub(r'[<>:"/\\|?*]', '', info.get('title', 'video'))
            return cleaned_title
    
    def start(self):
        self.output_path= self.output_path.split('.')[0] #removing the extension from output path
        
        # Extract resolution number (e.g., "1080p" -> 1080)
        resolution_number = int(self.resolution[:-1])  # Remove the "p" and convert to integer
        
        # Determine the format string based on the include_audio option
        if self.include_audio == 'audio_only':
            format_string = 'bestaudio/best'
            self.output_path = self.output_path + '.mp3'  # Set output path for audio-only
        elif self.include_audio == 'no_audio':
            self.output_path = self.output_path + '.mp4' 
            format_string = f'bestvideo[height<={resolution_number}][ext=mp4]' # Set format for video without audio
        else:
            temp_output_path = './temp/temp_vid.mp4'# Temporary output path for audio+video
            original_ouput_path = self.output_path
            self.output_path = temp_output_path
            format_string = f'bestvideo[height<={resolution_number}][ext=mp4]+bestaudio/best[height<={resolution_number}]'  # Set format for video with audio
            
        # Configure yt-dlp options
        ydl_opts = {
            'format': format_string,
            'outtmpl': self.output_path,  # Use the user-specified output path
            'progress_hooks': [self.update_progress],  # Add progress hook
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            
            self.progress_callback(100, "Download Complete!")
            
            # Perform FFmpeg conversion if necessary
            if self.include_audio != "audio_only" and self.include_audio != "no_audio":
                self.convert_to_mp4(input_path=self.output_path, output_path=original_ouput_path)

            self.completion_callback(True, "Download and conversion completed!")
        except Exception as e:
            self.completion_callback(False, f"An error occurred: {str(e)}")

    def update_progress(self, d):
        if d["status"] == "downloading":
            # Calculate progress percentage
            total_bytes = d.get("total_bytes") or d.get("total_bytes_estimate")
            if total_bytes:
                downloaded_bytes = d["downloaded_bytes"]
                progress_percent = (downloaded_bytes / total_bytes) * 100

                # Call the progress callback
                self.progress_callback(progress_percent) 
                
    def convert_to_mp4(self, input_path, output_path):
        input_path = f"{input_path}.webm"
        # Convert the downloaded file to MP4 using FFmpeg
        output_path = output_path + ".mp4"
        ffmpeg_command = [
            "ffmpeg",
            "-i", input_path,  # Input file
            "-c:v", "copy",  # Copy video stream without re-encoding
            "-c:a", "aac",  # Encode audio to AAC
            output_path  # Output file
        ]

        # Run FFmpeg with progress tracking
        self.run_ffmpeg_with_progress(ffmpeg_command)

        # Delete the original file
        os.remove(input_path)
        
    def run_ffmpeg_with_progress(self, ffmpeg_command):
            # Initialize FFmpeg progress tracker
            ff = FfmpegProgress(ffmpeg_command)

            # Run FFmpeg and update progress
            for progress in ff.run_command_with_progress():
                self.progress_callback(progress, 'Conversion')

            # Update progress to 100% when done
            self.progress_callback(100, 'Conversion complete!')