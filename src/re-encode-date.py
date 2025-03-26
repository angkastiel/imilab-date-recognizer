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

def recode_date(s: str):
    #print(s)
    d = datetime.strptime(s, '%Y/%m/%d %H:%M:%S')
    return d.strftime('%Y-%m-%d %H:%M:%S')


def convert_json(input_file: str, output_file: str):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for o in data:
        o['timestamp'] = recode_date(o['timestamp'])
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Recode timestamp')
    parser.add_argument('--source', '-s', required=True, help='Source file path')
    parser.add_argument('--destination', '-d', required=True, help='Destination file path')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.source):
        print(f"Error: Source file '{args.source}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    convert_json(args.source, args.destination)