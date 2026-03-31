
from enum import Enum, auto
from typing import Any
from stream import Stream


class TokenType(Enum):
    INTEGER = auto()
    IDENTIFIER = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    LPAREN = auto()
    RPAREN = auto()
    WHITESPACE = auto()
    EOL = auto()
    EOF = auto()


class Token:
    def __init__(self, type_: TokenType, value: Any):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"({self.type.name}, '{self.value}')"


class ScannerError(Exception):
    pass


class Scanner2:

    def __init__(self, stream: Stream):
        self.stream = stream
        self.tokens = []

    # def skip_whitespace(self):
    #     """Pomija spacje."""
    #     while self.stream.current_char is not None and self.stream.current_char.isspace():
    #         self.stream.advance()

    def integer(self) -> int:
        """Pobiera ciąg cyfr i zwraca jako liczbę całkowitą."""
        result = ''
        while self.stream.current_char is not None and self.stream.current_char.isdigit():
            result += self.stream.current_char
            self.stream.advance()
        return int(result)

    def identifier(self) -> str:
        """Pobiera ciąg liter i cyfr (zaczynający się od litery) jako identyfikator."""
        result = ''
        while self.stream.current_char is not None and (self.stream.current_char.isalnum() or self.stream.current_char == '_'):
            result += self.stream.current_char
            self.stream.advance()
        return result

    def error(self):
        """Obsługa błędów."""
        char = self.stream.current_char
        raise ScannerError(f"Błąd leksykalny: Nieoczekiwany znak '{char}'")

    def skaner(self) -> Token | None:
        """Funkcja skanująca, zwracająca następny token."""
        # self.skip_whitespace()

        if self.stream.current_char is None:
            return Token(TokenType.EOF, 'EOF')

        if self.stream.current_char.isdigit():
            return Token(TokenType.INTEGER, self.integer())

        if self.stream.current_char.isalpha():
            return Token(TokenType.IDENTIFIER, self.identifier())

        if self.stream.current_char == '+':
            self.stream.advance()
            return Token(TokenType.PLUS, '+')

        if self.stream.current_char == '-':
            self.stream.advance()
            return Token(TokenType.MINUS, '-')

        if self.stream.current_char == '*':
            self.stream.advance()
            return Token(TokenType.MULTIPLY, '*')

        if self.stream.current_char == '/':
            self.stream.advance()
            return Token(TokenType.DIVIDE, '/')

        if self.stream.current_char == '(':
            self.stream.advance()
            return Token(TokenType.LPAREN, '(')

        if self.stream.current_char == ')':
            self.stream.advance()
            return Token(TokenType.RPAREN, ')')

        if self.stream.current_char == '=':
            self.stream.advance()
            return Token(TokenType.EQUAL, '=')

        if self.stream.current_char == '!=':
            self.stream.advance()
            return Token(TokenType.NOT_EQUAL, '!=')

        if self.stream.current_char == ' ':
            self.stream.advance()
            return Token(TokenType.WHITESPACE, ' ')

        if self.stream.current_char == '\n':
            self.stream.advance()
            return Token(TokenType.EOL, '\n')

        self.error()
        return None

    def tokenize(self) -> list:
        """Główna pętla skanująca, która aktualizuje listę tokenów."""
        while True:
            token = self.skaner()
            self.tokens.append(token)

            if token.type == TokenType.EOF:
                self.stream.close()
                break

        return self.tokens


