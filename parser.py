from Token import Token, TokenType
from typing import List, Dict, Optional, Union
from JSONObject import JSONObject, JSONArray


class Parser:
    def __init__(self, tokens: List[Token] = None):
        if tokens is None:
            tokens = []
        self.tokens = tokens
        self.pos = 0

    def peek(self, n: int = 0) -> Token:
        if self.pos + n < len(self.tokens):
            return self.tokens[self.pos + n]
        return Token(TokenType.EOF, self.pos + n, '')

    def advance(self) -> Token:
        if self.pos + 1 < len(self.tokens):
            self.pos += 1
            return self.tokens[self.pos]
        return Token(TokenType.EOF, self.pos, '')

    def parse_array(self) -> JSONArray:
        array = JSONArray()
        self.expect(TokenType.LBRACKET)
        self.advance()

        while self.peek().type not in (TokenType.RBRACKET, TokenType.EOF):
            self.expect_value()
            array.add(self.parse_value())
            self.advance()
            if self.peek().type != TokenType.RBRACKET:
                self.expect(TokenType.COMMA)
                self.advance()
        self.expect(TokenType.RBRACKET)

        return array

    def parse_object(self) -> JSONObject:
        self.expect(TokenType.LBRACE)
        obj = JSONObject()

        while self.peek().type not in (TokenType.EOF, TokenType.RBRACE):
            key_token = self.advance()
            self.expect(TokenType.STRING)

            self.advance()
            self.expect(TokenType.COLON)

            self.advance()
            self.expect_value()

            key = key_token.literal
            value = self.parse_value()
            obj.add(key, value)

            self.advance()

        if self.peek().type == TokenType.RBRACE and self.peek(1).type == TokenType.EOF:
            self.advance()

        return obj

    def parse_value(self):
        token = self.tokens[self.pos]
        if token.type == TokenType.LBRACE:
            return self.parse_object()
        if token.type == TokenType.LBRACKET:
            return self.parse_array()
        if token.type == TokenType.STRING:
            return token.literal
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

    def parse(self) -> JSONObject | JSONArray | str | float | int | bool | None:
        result = self.parse_value()
        self.advance()
        self.expect(TokenType.EOF)
        return result
