# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 22:03:39 2025

@author: kastiel
"""

import os
import sys
import argparse
import json
from datetime import datetime

def parse_imilab_date(s: str):
    try:
        return datetime.strptime(s, '%Y/%m/%d %H:%M:%S')
    except:
        return None


def parse_datetime(input_str: str):
    """
    Парсит дату и время из строки формата 'YYYYMMDD_HHMMSSsss'
    
    Args:
        input_str (str): Строка с датой (напр. '20240711_094748456')
    
    Returns:
        datetime: Объект datetime
    """

    
    # Разделяем дату и время
    date_part, time_part = input_str.split('_')
    
    # Парсим компоненты
    year = int(date_part[:4])
    month = int(date_part[4:6])
    day = int(date_part[6:8])
    
    hour = int(time_part[:2])
    minute = int(time_part[2:4])
    second = int(time_part[4:6])
    
    # Создаем объект datetime (миллисекунды сохраняем отдельно)
    dt = datetime(year, month, day, hour, minute, second)
    
    return dt


def parse_imilab_filename_date(fn: str):
    if not fn.startswith('PIC_IMI_') and not fn.startswith('VIDEO_IMI_'):
        return None
    try:
        fn = fn.removeprefix('PIC_IMI_').removeprefix('VIDEO_IMI_').removesuffix('.jpg').removesuffix('.mp4')
        return parse_datetime(fn)
    except:
        return None
    

def analyze_json(input_file: str):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for o in data:
        file_name = str(o['file'])
        ts = parse_imilab_date(o['timestamp'])
        fts = parse_imilab_filename_date(file_name)
        if ts is None:
            print('Cannot parse timestamp:', file_name, o['timestamp'])
            continue
        if fts is None:
            print('Cannot parse timestamp from filename:', file_name)
            continue
        if ts.date() != fts.date():
            print('Dates are not equal for:', file_name)
            print('    ', o['timestamp'])
            print('    ', fts)
            continue
        if (file_name.endswith('.jpg')):
            if (ts.time().hour != fts.time().hour) or (ts.time().minute != fts.time().minute):
                print('Times are not equal for:', file_name)
                print('    ', o['timestamp'])
                print('    ', fts)
                continue
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze timestamp')
    parser.add_argument('--source', '-s', required=True, help='Source file path')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.source):
        print(f"Error: Source file '{args.source}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    analyze_json(args.source)