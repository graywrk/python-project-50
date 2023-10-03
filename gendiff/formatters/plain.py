def normalize_value(value):
    if isinstance(value, bool):
        if value:
            return "true"
        else:
            return "false"
    elif value is None:
        return "null"
    elif isinstance(value, dict):
        return "[complex value]"
    return "'%s'" % (str(value),)


def format_plain(AST, path=[]): # noqa: max-complexity=10
    result = ""
    for key in AST:
        if len(AST[key]['children']) > 0:
            result += format_plain(AST[key]['children'], path + [key])
            continue
        if AST[key]['type'] == 'UNCHANGED':
            pass
        elif AST[key]['type'] == 'CHANGED':
            result += "Property '%s' was updated. From %s to %s\n" % ('.'.join(path + [key]), normalize_value(AST[key]['value']), normalize_value(AST[key]['new_value']))
        elif AST[key]['type'] == 'DELETED':
            result += "Property '%s' was removed\n" % ('.'.join(path + [key]),)
        elif AST[key]['type'] == 'ADDED':
            result += "Property '%s' was added with value: %s\n" % ('.'.join(path + [key]), normalize_value(AST[key]['value']))
        else:
            raise Exception("Not supported key type")

    return result
