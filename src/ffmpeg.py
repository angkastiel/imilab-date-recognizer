# -*- coding: utf-8 -*-
"""
Created on Sun Mar 23 01:36:39 2025

@author: kastiel
"""

import subprocess

class FFmpegRunner:
    def __init__(self, ffmpeg_path='ffmpeg'):
        self.ffmpeg_path = ffmpeg_path


    def extract_first_frame(self, video_path, output_frame_path):
        try:        
            command = [
                self.ffmpeg_path, '-y', '-i', video_path, 
                '-ss', '00:00:00', 
                '-vframes', '1',
                '-q:v', '2', 
                output_frame_path
            ]
            subprocess.run(command, stderr=subprocess.PIPE, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"ffmpeg error {video_path}: {e}")
            return False


    def extract_duration(self, video_path):
        try:
            command = [
                self.ffmpeg_path, '-i', video_path, '-hide_banner'
            ]
            result = subprocess.run(command, stderr=subprocess.PIPE, text=True)
            duration_line = [line for line in result.stderr.splitlines() if 'Duration' in line]
            duration = duration_line[0].split()[1]
        
            return duration.strip(',').strip()
        except subprocess.CalledProcessError as e:
            print(f"ffmpeg error {video_path}: {e}")
