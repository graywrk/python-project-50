#!/usr/bin/env python3

import argparse
from gendiff import generate_diff


def main():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.')
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument('-f', '--format', help='set format of output (stylish, plain)', default='stylish', type=str)
    args = parser.parse_args()
    file_path1 = args.first_file
    file_path2 = args.second_file
    format = args.format
    diff = generate_diff(file_path1, file_path2, format)
    print(diff)


if __name__ == '__main__':
    main()
