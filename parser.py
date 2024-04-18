from Token import Token, TokenType
from typing import List, Dict, Optional


class Parser:
    def __init__(self, tokens: List[Token] = None):
        if tokens is None:
            tokens = []
        self.tokens = tokens
        self.pos = 0
        self.result: Dict = {}

    def peek(self, n: int = 0) -> Optional[Token]:
        if self.pos + n < len(self.tokens):
            return self.tokens[self.pos + n]
        return Token(TokenType.EOF, self.pos + n, '')

    def advance(self) -> Optional[Token]:
        if self.pos + 1 < len(self.tokens):
            self.pos += 1
            return self.tokens[self.pos]
        return Token(TokenType.EOF, self.pos, '')

    def parse_array(self):
        array = []
        while self.peek().type != TokenType.RBRACKET:
            t = self.advance()
            self.expect_value()
            array.append(self.parse_value(t))
            self.advance()
            if self.peek().type != TokenType.RBRACKET:
                self.expect(TokenType.COMMA)
        self.expect(TokenType.RBRACKET)
        return array

    def parse_object(self) -> Dict:
        self.expect(TokenType.LBRACE)
        obj = {}
        while self.peek().type not in (TokenType.EOF, TokenType.RBRACE):
            key_token = self.advance()
            self.expect(TokenType.STRING)

            self.advance()
            self.expect(TokenType.COLON)

            value_token = self.advance()
            self.expect_value()

            value = self.parse_value(value_token)
            obj[key_token.literal.strip('\"')] = value

            self.advance()

        if self.peek().type == TokenType.RBRACE and self.peek(1).type == TokenType.EOF:
            self.advance()

        return obj

    def parse_value(self, token: Token):
        if token.type == TokenType.LBRACE:
            return self.parse_object()
        if token.type == TokenType.LBRACKET:
            return self.parse_array()
        if token.type == TokenType.STRING:
            return token.literal.strip('\"')
        if token.type == TokenType.FLOAT:
            return float(token.literal)
        if token.type == TokenType.INTEGER:
            return int(token.literal)
        if token.type in (TokenType.TRUE, TokenType.FALSE):
            return token.literal
        return None

    def expect(self, *token_types: TokenType):
        token = self.peek()

        if len(token_types) == 1 and token.type != token_types[0]:
            print(f"Expected a {token_types[0]} at pos {self.peek().pos} {token}")
            exit(1)

        if token.type not in token_types:
            print(f"Expected one of {token_types} at pos {token.pos} {token}")
            exit(1)

    def expect_value(self):
        self.expect(TokenType.LBRACE, TokenType.LBRACKET, TokenType.STRING,
                    TokenType.INTEGER, TokenType.FLOAT, TokenType.TRUE, TokenType.FALSE,
                    TokenType.NULL)

    def is_eof(self):
        return self.tokens[self.pos].type == TokenType.EOF

    def parse(self) -> Dict:
        self.result = self.parse_object()
        self.expect(TokenType.EOF)
        self.advance()
        return self.result
