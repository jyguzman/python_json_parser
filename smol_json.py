from tokenizer import Tokenizer
from parser import Parser
from typing import Union


def loads(json_string: str):
    lexer = Tokenizer(json_string)
    tokens = lexer.lex()
    lexer.print()
    parser = Parser(tokens)
    return parser.parse()


def dumps(obj: Union[None, bool, float, int, str, dict], level=0, indent=4) -> str:
    if obj is None:
        return "null"
    if isinstance(obj, str):
        return f'\"{obj}\"'
    if isinstance(obj, (bool, int, float)):
        return str(obj)
    if isinstance(obj, list):
        return '[\n' + ','.join([dumps(item, level, indent) for item in obj]) + ']'

    print(obj)

    json_str = ["{\n"]
    keys = 0

    for key in obj:
        kv_str = [' '*(level + 1)*indent, f'\"{key}\": ']
        val = obj[key]

        if isinstance(val, dict):
            kv_str.append(dumps(val, level + 1, indent))
        else:
            kv_str.append(dumps(val))

        keys += 1
        kv_str.append('\n' if keys == len(obj) else ',\n')

        json_str += kv_str
    json_str += [' '*(level*indent), "}"]
    return ''.join(json_str)
