import pytest
import os
from gendiff import core


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def test_gendiff():
    file1_path = CURRENT_DIR + "/fixtures/file1.json"
    file2_path = CURRENT_DIR + "/fixtures/file2.json"
    result_file_path = CURRENT_DIR + "/fixtures/result.txt"
    with open(result_file_path) as result_file:
        result = result_file.read()
    assert core.generate_diff(file1_path, file2_path) == result