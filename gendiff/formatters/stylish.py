# flake8: noqa: C901
def format_stylish(AST):
    def normalize_value(value):
        if isinstance(value, bool):
            if value:
                return 'true'
            else:
                return 'false'
        elif value is None:
            return 'null'
        elif isinstance(value, dict):
            return value
        else:
            return str(value)

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
                result += make_diff_string(key, normalize_value(AST[key]['value']), " ", level)
            elif AST[key]['type'] == 'CHANGED':
                result += make_diff_string(key, normalize_value(AST[key]['value']), "-", level)
                result += make_diff_string(key, normalize_value(AST[key]['new_value']), "+", level)
            elif AST[key]['type'] == 'DELETED':
                result += make_diff_string(key, normalize_value(AST[key]['value']), "-", level)
            elif AST[key]['type'] == 'ADDED':
                result += make_diff_string(key, normalize_value(AST[key]['value']), "+", level)
            else:
                raise Exception("Not supported key type")
        return result
    
    result = "{\n"
    result += stylish_inner(AST)
    result += "}"
    return result
