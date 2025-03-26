# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 22:03:39 2025

@author: kastiel
"""

import os
import sys
import argparse
import json


def find_first_check(input_file: str, directory: str):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for o in data:
        file_name = str(o['file'])
        if (('need_manual_check' in o) and  o['need_manual_check']):
            os.startfile(os.path.join(directory, file_name))
            sys.exit(-1)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Manual check')
    parser.add_argument('--source', '-s', required=True, help='Source file path')
    parser.add_argument('--directory', '-d', required=True, help='Directory path')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.source):
        print(f"Error: Source file '{args.source}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    find_first_check(args.source, args.directory)