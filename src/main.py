# -*- coding: utf-8 -*-
import os
import subprocess

import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent.resolve()))

import ffmpeg
import tempfile

from PIL import Image, ImageOps


def get_file_path(path: str) -> str:
    script_dir = Path(__file__).parent.resolve()
    return (script_dir / path).resolve()


def check_file_path(path: str):
    if not os.path.exists(path):
        raise Exception(f"Path not found: {path}")


with open(get_file_path('config.json'), 'r', encoding='utf-8') as f:
    config = json.load(f)

FFMPEG_PATH = get_file_path(config.get("ffmpeg", {}).get("path"))
TESSERACT_PATH = get_file_path(config.get("tesseract", {}).get("path"))

check_file_path(FFMPEG_PATH)
check_file_path(TESSERACT_PATH)


import re
from datetime import datetime

def check_date_time_format(input_string):
    if input_string is None:
        return False
    pattern = r'^\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}$'
    if not re.match(pattern, input_string):
        return False
    try:
        datetime.strptime(input_string, '%Y/%m/%d %H:%M:%S')
    except ValueError:
        return False
    return True    
    
    
def check_duration_format(input_string):
    if input_string is None:
        return False
    pattern = r'^\d{2}:\d{2}:\d{2}.\d{2}$'
    if re.match(pattern, input_string):
        return True
    else:
        return False

def crop_imilab_frame(image: Image) -> Image:
    image = image.resize((2560, 1440), Image.LANCZOS);
    x = 300
    y = 0
    width = 570
    height = 65
    return image.crop((x, y, x + width, y + height))
    

def prepare_image_for_recognition(input_image_path: str, output_image_path: str, invert: bool, scale: float) -> bool:    
    try:
        image = Image.open(input_image_path)
        relult_image = crop_imilab_frame(image)
        image.close()
        
        if scale is not None:
            scale_image = relult_image.resize((round(relult_image.width * scale), round(relult_image.height * scale)), Image.LANCZOS);
            relult_image = scale_image
        
        if invert:
            inverted_image = ImageOps.invert(relult_image)
            relult_image = inverted_image

        relult_image = relult_image.convert('L')
        relult_image = relult_image.point(lambda x: 0 if x < 128 else 255, '1')

        relult_image.save(output_image_path)
        relult_image.close()
        return True
    except Exception as e:
        print(f"Crop error: {e}")
        return False


def run_tesseract(image_path: str) -> str:
    try:
        result = subprocess.run(
            [TESSERACT_PATH, '--oem', '3', '--psm', '6', '-c', 'tessedit_char_whitelist=0123456789 :/', image_path, 'stdout'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Cannot OCR {image_path}: {e}")
        return None
            
    
def get_temp_jpg_file() -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f:
        return f.name
        
    
def do_recognize_timestamp(image_path: str, invert_image: bool, scale_image: float) -> str:
    temp_fn: str = get_temp_jpg_file()
    try:
        if not prepare_image_for_recognition(image_path, temp_fn, invert_image, scale_image):
            print(f'Cannot crop image {image_path}')
            return None
        return str(run_tesseract(temp_fn)).strip('(').strip(')').strip('.').strip(',').strip()
    finally:
        os.remove(temp_fn)
        
        
def get_only_digits(s: str) -> str:
    r: str = ""
    for c in s:
        if c.isdigit():
            r = r + c
    return r
        
    
def recognize_timestamp(image_path: str) -> str:
    s1: str = do_recognize_timestamp(image_path, invert_image=False, scale_image=None)
    s2: str = do_recognize_timestamp(image_path, invert_image=True, scale_image=None)
    s3: str = do_recognize_timestamp(image_path, invert_image=True, scale_image=0.5)
    if s1 == s2 == s3:
        return s3, False
    print(s1)
    print(s2)
    print(s3)
        
    s = s3
    if not check_date_time_format(s):
        if check_date_time_format(s2):
            s = s2
        else:
            if check_date_time_format(s1):
                s = s1
    if check_date_time_format(s) and (get_only_digits(s1) == get_only_digits(s2) == get_only_digits(s3)):
        return s, False
    return s, True


ffmpeg = ffmpeg.FFmpegRunner(FFMPEG_PATH)

def detect_timestamp(file_path: str) -> str:
    if file_path.lower().endswith(('.jpg', '.jpeg')):
        return recognize_timestamp(file_path)
    if file_path.lower().endswith(('.mp4')):    
        temp_fn = get_temp_jpg_file()
        try:
            if not ffmpeg.extract_first_frame(file_path, temp_fn):
                print(f'Cannot extract frames for {file_path}')
                return None
            return recognize_timestamp(temp_fn)
        finally:
           os.remove(temp_fn) 
    return None
    
    
import argparse
parser = argparse.ArgumentParser(description='Recognize timestamp on video and photo')
parser.add_argument('--source', '-s', required=True, help='Source directory path')
parser.add_argument('--destination', '-d', required=True, help='Destination file path')

args = parser.parse_args()

results = list()

for filename in os.listdir(args.source):
    file_path = os.path.join(args.source, filename)
    
    o = dict()
    o["file"] = filename
    r = detect_timestamp(file_path)
    if r is None:
        str_timestamp, has_difs = None, None
    else:
        str_timestamp, has_difs = r
    if not check_date_time_format(str_timestamp):
        str_timestamp = f"??????????? {str_timestamp}"
    o["timestamp"] = str_timestamp
    if has_difs is not None and has_difs:
        o["need_manual_check"] = True
    
    dur_text = None
    if filename.lower().endswith(('.mp4')):         
        dur_text = ffmpeg.extract_duration(file_path)
        if not check_duration_format(dur_text):
            dur_text = f"??????????? {dur_text}"
        o["duration"] = dur_text
            
        
    results.append(o)
    print(f"{filename}")
    print(str_timestamp)
    print(dur_text)
    print("-" * 40)  # Разделитель для удобства чтения
    
import json
with open(args.destination, 'w', encoding='utf-8') as json_file:
    json.dump(results, json_file, indent=4)
            
