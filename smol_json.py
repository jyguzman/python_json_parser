from tokenizer import Tokenizer
from parser import Parser


def loads(json_string: str):
    lexer = Tokenizer(json_string)
    parser = Parser(lexer.lex())
    return parser.parse()


def dumps(obj: dict, level=0, indent=4) -> str:
    json_str = ["{\n"]
    keys = 0

    for key in obj:
        kv_str = [' '*(level + 1)*indent, f'\"{key}\": ']
        val = obj[key]

        if isinstance(val, str):
            kv_str.append(f'\"{val}\"')
        if isinstance(val, (bool, int, float)):
            kv_str.append(str(val))
        if isinstance(val, dict):
            kv_str.append(dumps(val, level + 1, indent))

        keys += 1
        kv_str.append('\n' if keys == len(obj) else ',\n')

        json_str += kv_str
    json_str += [' '*(level*indent), "}"]
    return ''.join(json_str)
