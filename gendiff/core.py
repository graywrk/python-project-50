import json
import yaml
from copy import deepcopy

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


# flake8: noqa: C901
def stylish(AST):

    def make_indent(level, space_count=4):
        return " " * (space_count * level - 2)

    def make_diff_string(key, value, prefix, level):
        if isinstance(value, dict):
            result = make_indent(level) + prefix + " " + str(key) + ": {\n"
            for item in value:
                result += make_diff_string(item, value[item], " ", level + 1) 
            result += "  " + make_indent(level) + "}\n"
            return result
        else:
            return make_indent(level) + prefix + " " + str(key) + ": " + str(value) + "\n"

    def stylish_inner(AST, level=1):
        result = ""
        for key in AST:
            if len(AST[key]['children']) > 0:
                result += "  " + make_indent(level) + key + ": {\n" + stylish_inner(AST[key]['children'], level + 1) + "  " + make_indent(level) + "}\n"
                continue
            if AST[key]['type'] == 'UNCHANGED':
                result += make_diff_string(key, AST[key]['value'], " ", level)
            elif AST[key]['type'] == 'CHANGED':
                result += make_diff_string(key, AST[key]['value'], "-", level)
                result += make_diff_string(key, AST[key]['new_value'], "+", level)
            elif AST[key]['type'] == 'DELETED':
                result += make_diff_string(key, AST[key]['value'], "-", level)
            elif AST[key]['type'] == 'ADDED':
                result += make_diff_string(key, AST[key]['value'], "+", level)
            else:
                raise Exception("Not supported key type")
        return result
    
    result = "{\n"
    result += stylish_inner(AST)
    result += "}"
    return result


def make_ast(dict1, dict2):
    AST = {}

    allkeys = {key for dictionary in [dict1, dict2] for key in dictionary}
    allkeys = sorted(allkeys)

    for key in allkeys:
        AST[key] = {'children': {}, 'type': 'UNCHANGED'}
        if key in dict1:
            if key in dict2:
                if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
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


def make_output(AST, formater):
    return formater(AST)


def generate_diff(file_path1, file_path2, formater=stylish):
    dict1 = load_from_file(file_path1)
    dict2 = load_from_file(file_path2)
    AST = make_ast(dict1, dict2)
    print(AST)
    return make_output(AST, formater)
