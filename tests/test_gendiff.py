import pytest
import os
from gendiff import generate_diff


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def test_gendiff_json():
    file1_path = CURRENT_DIR + "/fixtures/file1.json"
    file2_path = CURRENT_DIR + "/fixtures/file2.json"
    result_file_path = CURRENT_DIR + "/fixtures/result1.txt"
    with open(result_file_path) as result_file:
        result = result_file.read()
    assert generate_diff(file1_path, file2_path) == result


def test_gendiff_yaml():
    file1_path = CURRENT_DIR + "/fixtures/file1.yaml"
    file2_path = CURRENT_DIR + "/fixtures/file2.yaml"
    result_file_path = CURRENT_DIR + "/fixtures/result1.txt"
    with open(result_file_path) as result_file:
        result = result_file.read()
    assert generate_diff(file1_path, file2_path) == result


def test_gendiff_with_nested_data():
    file1_path = CURRENT_DIR + "/fixtures/file3.json"
    file2_path = CURRENT_DIR + "/fixtures/file4.json"
    result_file_path = CURRENT_DIR + "/fixtures/result2.txt"
    with open(result_file_path) as result_file:
        result = result_file.read()
    assert generate_diff(file1_path, file2_path) == result