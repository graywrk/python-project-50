#!/usr/bin/env python3

import argparse
from gendiff import gendiff


def main():
    parser = argparse.ArgumentParser(description='Compares two configuration files and shows a difference.')
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()
    
    #gendiff()


if __name__ == '__main__':
    main()
