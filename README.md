# imilab-date-recognizer
Recognize timestamp on pics and video records of Imilab C30

# Usage

## Recognize date and time from camera photo or video
```
recognize.bat -s "examples" -d "rec.json"
```

## Manual check files
```
manual_check.bat -s "rec.json" -d "examples"
```

## Analyze date
```
analyze.bat -s "rec.json"
```

## Recode date from format yyyy/mm/dd HH:MM:SS to yyyy-mm-dd HH:MM:SS in field 'timestamp'
```
finish.bat -s "rec.json" -d "timestamp.json"
```

## Setup

## 1) Install Tesseract-OCR
See https://github.com/tesseract-ocr/tesseract

## 2) Install ffmpeg
Or use portable version

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
