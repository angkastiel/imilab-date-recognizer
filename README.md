# imilab_date_recognizer
Recognize timestamp on pics and video records of Imilab C30

## Recognize date and time from camera photo or video
```
recognize -s "examples" -d "rec.json"
```

## Manual check files
```
manual_check -s "rec.json" -d "examples"
```

## Analyze date
```
analyze -s "rec.json"
```

## Recode date from format yyyy/mm/dd HH:MM:SS to yyyy-mm-dd HH:MM:SS in field 'timestamp'
```
finish -s "rec.json" -d "timestamp.json"
```
