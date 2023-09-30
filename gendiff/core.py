import json
import yaml


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


def make_diff_string(key, value, prefix="    "):
    return prefix + str(key) + ": " + str(value) + "\n"


def generate_diff(file_path1, file_path2):
    dict1 = load_from_file(file_path1)
    dict2 = load_from_file(file_path2)

    result = "{\n"

    allkeys = {key for dictionary in [dict1, dict2] for key in dictionary}
    allkeys = sorted(allkeys)

    for key in allkeys:
        if key in dict1 and key in dict2:
            if dict1[key] == dict2[key]:
                result += make_diff_string(key, dict1[key])
            else:
                result += make_diff_string(key, dict1[key], "  - ")
                result += make_diff_string(key, dict2[key], "  + ")
        elif key in dict1:
            result += make_diff_string(key, dict1[key], "  - ")
        elif key in dict2:
            result += make_diff_string(key, dict2[key], "  + ")
    result += "}"
    return result
