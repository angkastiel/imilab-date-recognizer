# imilab-date-recognizer
Recognize timestamp on pics and video records of Imilab C30

# Usage

## Recognize date and time from camera photo or video
```
recognize.bat -s "examples" -d "rec.json"
```
Example of results in rec.json file:
```
[
    {
        "file": "PIC_IMI_20250205_011728331.jpg",
        "timestamp": "2025/02/05 01:17:26"
    },
    {
        "file": "VIDEO_IMI_20240715_002427198.mp4",
        "timestamp": "2024/07/15 00:23:28",
        "duration": "00:00:59.65"
    }
]
```

## Manual check files
```
manual_check.bat -s "rec.json" -d "examples"
```

## Analyze date
```
analyze.bat -s "rec.json"
```

## Recode date in timestamp field
Recode from format yyyy/mm/dd HH:MM:SS to yyyy-mm-dd HH:MM:SS
```
finish.bat -s "rec.json" -d "timestamp.json"
```

## Setup

## 1) Install Tesseract-OCR
See https://github.com/tesseract-ocr/tesseract

## 2) Install ffmpeg
Or use portable version. See https://www.ffmpeg.org/

## 3) Change src/config.json
Put actual paths in config
```
{
    "ffmpeg": {
        "path": "..\\deps\\ffmpeg-5.0.1-full\\bin\\ffmpeg.exe"
    },
    "tesseract": {
        "path": "..\\deps\\Tesseract-OCR\\tesseract.exe"
    }
}
```

Tested on ffmpeg 5.0.1 and Tesseract 5.5.0