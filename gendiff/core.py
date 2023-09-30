import json


def generate_diff(file_path1, file_path2):
    with open(file_path1) as file1, open(file_path2) as file2:
        dict1 = json.load(file1)
        dict2 = json.load(file2)
    result = "{\n"
    allkeys = {key for dictionary in [dict1, dict2] for key in dictionary}
    allkeys = sorted(allkeys)
    for key in allkeys:
        if key in dict1 and key in dict2:
            if dict1[key] == dict2[key]:
                result += "    " + str(key) + ": " + str(dict1[key]) + "\n"
            else:
                result += "  - " + str(key) + ": " + str(dict1[key]) + "\n"
                result += "  + " + str(key) + ": " + str(dict2[key]) + "\n"
        elif key in dict1:
            result += "  - " + str(key) + ": " + str(dict1[key]) + "\n"
        elif key in dict2:
            result += "  + " + str(key) + ": " + str(dict2[key]) + "\n"
    result += "}"
    return result
