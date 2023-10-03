import json
import yaml
from copy import deepcopy
from gendiff.formatters.plain import format_plain
from gendiff.formatters.stylish import format_stylish
from gendiff.formatters.json import format_json


def load_from_json(file_path):
    with open(file_path) as file:
        result_dict = json.load(file)
    return result_dict


def load_from_yaml(file_path):
    with open(file_path) as file:
        result_dict = yaml.safe_load(file)
    return result_dict


def load_from_file(file_path):
    if file_path.endswith('.yaml') or file_path.endswith('.yml'):
        return load_from_yaml(file_path)
    elif file_path.endswith('.json'):
        return load_from_json(file_path)
    else:
        raise Exception('Unknown file format')


def make_ast(dict1, dict2):
    AST = {}

    allkeys = {key for dictionary in [dict1, dict2] for key in dictionary}
    allkeys = sorted(allkeys)

    for key in allkeys:
        AST[key] = {'children': {}, 'type': 'UNCHANGED'}
        if key in dict1:
            if key in dict2:
                if isinstance(dict1[key], dict) and \
                   isinstance(dict2[key], dict):
                    AST[key]['children'] = make_ast(dict1[key], dict2[key])
                if dict1[key] == dict2[key]:
                    AST[key]['type'] = 'UNCHANGED'
                    AST[key]['value'] = deepcopy(dict1[key])
                else:
                    AST[key]['type'] = 'CHANGED'
                    AST[key]['value'] = deepcopy(dict1[key])
                    AST[key]['new_value'] = deepcopy(dict2[key])
            else:
                AST[key]['type'] = 'DELETED'
                AST[key]['value'] = deepcopy(dict1[key])
        else:
            AST[key]['type'] = 'ADDED'
            AST[key]['value'] = deepcopy(dict2[key])

    return AST


def make_output(AST, formatter):
    return formatter(AST)


def generate_diff(file_path1, file_path2, formatter='stylish'):
    dict1 = load_from_file(file_path1)
    dict2 = load_from_file(file_path2)
    AST = make_ast(dict1, dict2)
    if formatter == 'plain':
        return make_output(AST, format_plain)
    elif formatter == 'stylish':
        return make_output(AST, format_stylish)
    elif formatter == 'json':
        return make_output(AST, format_json)
    else:
        raise Exception('Unknown formatter')
