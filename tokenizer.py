from Token import Token, TokenType
from typing import Optional


class Tokenizer:
    def __init__(self, json_str: str = None):
        self.json_str = json_str
        if json_str is not None:
            self.size = len(self.json_str)
        self.pos = 0
        self.tokens = []
        self.keywords = {
            'false': (TokenType.FALSE, False),
            'true': (TokenType.TRUE, True),
            'null': (TokenType.NULL, None)
        }

    def curr(self):
        return self.json_str[self.pos]

    def peek(self, n: int = 0):
        if self.pos + n < self.size:
            return self.json_str[self.pos + n]
        return '\0'

    def previous(self, n: int = 1):
        if self.pos - n >= 0:
            return self.json_str[self.pos - n]
        return '\0'

    def is_eof(self):
        return self.pos >= self.size

    def advance(self) -> str:
        if self.peek() == '\0':
            return '\0'
        c = self.curr()
        self.pos += 1
        return c

    def lex_string(self) -> Token:
        start_pos = self.pos - 1
        string = [self.previous()]
        while self.peek(0) not in ('\"', '\0'):
            string.append(self.advance())

        if self.peek(0) == '\0':
            print("reached EOF without closing string")
            exit(1)

        string.append(self.advance())
        return Token(TokenType.STRING, start_pos, ''.join(string))

    def lex_number(self) -> Token:
        start_pos = self.pos - 1
        is_float = False

        num_str = [self.previous()]
        while self.peek().isdigit() or self.peek() == '.':
            if self.peek() == '.':
                is_float = True
            num_str.append(self.advance())

        num_str = ''.join(num_str)
        num = float(num_str) if is_float else int(num_str)
        num_type = TokenType.FLOAT if is_float else TokenType.INTEGER
        return Token(num_type, start_pos, num)

    def lex_keyword(self):
        start_pos = self.pos - 1
        keyword = [self.previous()]

        while self.peek().isalpha():
            keyword.append(self.advance())

        token_type, literal = self.keywords[''.join(keyword)]
        return Token(token_type, start_pos, literal)

    def match(self) -> Token:
        c = self.advance()
        while c in ('\n', '\r', ' '):
            c = self.advance()
        if c == '{':
            return Token(TokenType.LBRACE, self.pos, '{')
        if c == '}':
            return Token(TokenType.RBRACE, self.pos, '}')
        if c == '[':
            return Token(TokenType.LBRACKET, self.pos, '[')
        if c == ']':
            return Token(TokenType.RBRACKET, self.pos, ']')
        if c == ',':
            return Token(TokenType.COMMA, self.pos, ',')
        if c == ':':
            return Token(TokenType.COLON, self.pos, ':')
        if c == '\"':
            return self.lex_string()
        if c.isdigit():
            return self.lex_number()
        if c.isalpha():
            return self.lex_keyword()
        return Token(TokenType.EOF, self.pos, '')

    def add_token(self, token: Token):
        self.tokens.append(token)

    def reset(self, json_str: Optional[str]):
        self.json_str = json_str
        self.size = len(json_str)
        self.pos = -1
        self.tokens.clear()

    def lex(self, json_str=None):
        if json_str is not None:
            self.reset(json_str)

        if self.json_str.strip() in ('', None):
            print("JSON string must be provided.")
            exit(1)

        while not self.is_eof():
            token = self.match()
            self.add_token(token)
        self.add_token(Token(TokenType.EOF, self.pos, ''))

        return self.tokens

    def print(self):
        print('\n'.join(str(token) for token in self.tokens))
