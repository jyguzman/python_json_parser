from dataclasses import dataclass
from typing import Union
from enum import Enum, auto


class TokenType(Enum):
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    COLON = auto()
    STRING = auto()
    TRUE = auto()
    FALSE = auto()
    INTEGER = auto()
    FLOAT = auto()
    NULL = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    pos: int
    literal: Union[str, int, float, bool, None]

    def __repr__(self):
        return f'Token({self.type}, {self.pos}, {self.literal})'
