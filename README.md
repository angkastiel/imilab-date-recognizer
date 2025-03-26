# imilab-date-recognizer
Recognize timestamp on pictures and video records saved with Imilab Home application. Tested on camera Imilab C30.

# Usage

## Recognize date and time from camera photo or video
```
recognize.bat -s "<path-to-folder-with-records>" -d "<path-to-results-json-file>"
```
Example:
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
manual_check.bat -s "<path-to-recodnition-results-json-file>" -d "<path-to-folder-with-records>"
```
Example:
```
manual_check.bat -s "rec.json" -d "examples"
```

## Analyze date
```
analyze.bat -s "<path-to-recodnition-results-json-file>"
```
Example:
```
analyze.bat -s "rec.json"
```

## Recode date in timestamp field
Recode from format yyyy/mm/dd HH:MM:SS to yyyy-mm-dd HH:MM:SS
```
finish.bat -s "<path-to-recodnition-results-json-file>" -d "<path-to-results-json-file>"
```
Example:
```
finish.bat -s "rec.json" -d "timestamp.json"
```

# Setup

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

## 4) Install Python and PIL library
Or download and configure portable python.
1) Download Python 3.10.0 Windows embeddable package (x64) from https://www.python.org/downloads/
2) Put Python in `deps/python-3.10.0-embed-amd64`
3) Modify file `deps/python-3.10.0-embed-amd64/python310._pth`. Add paths:
```
Lib
Lib\site-packages
```
4) Download `get-pip.py` (https://bootstrap.pypa.io/get-pip.py) and put it to `deps/python-3.10.0-embed-amd64/get-pip.py`
5) Run `python get-pip.py` for `deps/python-3.10.0-embed-amd64`
6) Run `pip install pillow==11.1.0` for `deps/python-3.10.0-embed-amd64`

## 5) Modify python.bat
Or don't modify if you use python in `deps/python-3.10.0-embed-amd64`

Tested on ffmpeg 5.0.1, Tesseract 5.5.0, Python 3.10.0 and PIL 11.1.0