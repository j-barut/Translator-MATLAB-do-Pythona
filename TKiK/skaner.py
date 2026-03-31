from enum import Enum, auto
from typing import Any

class TokenType(Enum):
    INTEGER = auto()
    IDENTIFIER = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    LPAREN = auto()
    RPAREN = auto()
    EOF = auto()

class Token:
    def __init__(self, type_: TokenType, value: Any):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"({self.type.name}, '{self.value}')"

class ScannerError(Exception):
    pass

class Scanner:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if len(self.text) > 0 else None
        self.tokens = []

    def advance(self):
        """Przesuwa wskaźnik na kolejny znak w tekście."""
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None 
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        """Pomija spacje."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self) -> int:
        """Pobiera ciąg cyfr i zwraca jako liczbę całkowitą."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def identifier(self) -> str:
        """Pobiera ciąg liter i cyfr (zaczynający się od litery) jako identyfikator."""
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result

    def error(self):
        """Obsługa błędów."""
        char = self.current_char
        raise ScannerError(f"Błąd leksykalny: Nieoczekiwany znak '{char}'")

    def skaner(self) -> Token | None:
        """Funkcja skanująca, zwracająca następny token."""
        self.skip_whitespace()

        if self.current_char is None:
            return Token(TokenType.EOF, 'EOF')

        if self.current_char.isdigit():
            return Token(TokenType.INTEGER, self.integer())

        if self.current_char.isalpha():
            return Token(TokenType.IDENTIFIER, self.identifier())

        if self.current_char == '+':
            self.advance()
            return Token(TokenType.PLUS, '+')

        if self.current_char == '-':
            self.advance()
            return Token(TokenType.MINUS, '-')

        if self.current_char == '*':
            self.advance()
            return Token(TokenType.MULTIPLY, '*')

        if self.current_char == '/':
            self.advance()
            return Token(TokenType.DIVIDE, '/')

        if self.current_char == '(':
            self.advance()
            return Token(TokenType.LPAREN, '(')

        if self.current_char == ')':
            self.advance()
            return Token(TokenType.RPAREN, ')')

        self.error()
        return None

    def tokenize(self) -> list:
        """Główna pętla skanująca, która aktualizuje listę tokenów."""
        while True:
            token = self.skaner()
            self.tokens.append(token)
            
            if token.type == TokenType.EOF:
                break
                
        return self.tokens


