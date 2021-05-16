from typing import Union, Any, Generator, Dict

from enum import Enum, auto


def chr_to_int(char: chr, base: int) -> int:
    if '0' <= char <= '9':
        return int(char) - int('0')
    elif 'a' <= char <= 'z':
        return int(char) - int('a') + 10
    elif 'a' <= char <= 'z':
        if base > 36:
            pass
        else:
            return int(char) - int('a') + 10

    raise NotImplementedError  # TODO: Char to int


class TokenKind(Enum):
    EndOfFile = auto()
    Invalid = auto()
    Whitespace = auto()
    Identifier = auto()
    Int = auto()
    Float = auto()
    String = auto()

    Period = auto()
    Comma = auto()


class Token:
    Token: str = 'Token'  # TODO: Change type from str to TypeAlias in python 3.10
    ValueType: Any = Union[int, float, str, None]

    def __init__(self: Token, kind: TokenKind, source: str, position: int, line: int, column: int, length: int,
                 value: ValueType = None) -> None:
        self.kind: TokenKind = kind
        self.source: str = source
        self.position: int = position
        self.line: int = line
        self.column: int = column
        self.length: int = length
        self.value: Token.ValueType = value

    def __repr__(self: Token) -> str:
        return f"Token(kind = {self.kind}, position = {self.position}, line = {self.line}, column = {self.column}" \
               f", length = {self.length}, value = {self.value})"

    def __str__(self: Token) -> str:
        return self.source[self.position:self.position + self.length]


class Lexer:
    Lexer: str = 'Lexer'  # TODO: Change type from str to TypeAlias in python 3.10
    CharToTokenKind: Dict[chr, TokenKind] = {
        '.': TokenKind.Period,
        ',': TokenKind.Comma,
    }

    def __init__(self: Lexer, source: str) -> None:
        self.source: str = source
        self.position: int = 0
        self.line: int = 1
        self.column: int = 1

    def _peek(self: Lexer, offset: int) -> chr:
        index: int = self.position + offset
        if index >= len(self.source):
            return '\0'
        return self.source[index]

    @property
    def _current(self: Lexer) -> chr:
        return self._peek(0)

    def _next_chr(self: Lexer) -> chr:
        current: chr = self._current
        if self._current == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.position += 1
        return current

    def _skip_whitespace_and_comments(self: Lexer) -> int:
        raise NotImplementedError  # TODO: Skip whitespace and comments

    def get_tokens(self: Lexer) -> Generator[Token, None, None]:
        while self._current != '\0':
            start: int = self.position
            start_line: int = self.line
            start_column: int = self.column

            if self._current.isspace():
                yield from self._lex_whitespace(start, start_column, start_line)
            elif self._current == '/':
                self._next_chr()
                if self._current == '/':
                    self._next_chr()
                    raise NotImplementedError  # TODO: Single line comment
                if self._current == '*':
                    self._next_chr()
                    raise NotImplementedError  # TODO: Multi line comment
                else:
                    raise NotImplementedError  # TODO: Slash character
            elif self._current.isalpha() or self._current == '_':
                yield from self._lex_identifier(start, start_column, start_line)
            elif self._current.isdigit() or (self._current == '.' and self._peek(1).isdigit()):
                yield from self._lex_number(start, start_column, start_line)
            elif self._current == '\"':
                raise NotImplementedError  # TODO: String literal
            else:
                if self._current in self.CharToTokenKind:
                    char: chr = self._current
                    self._next_chr()
                    yield Token(self.CharToTokenKind[char], self.source, start, start_line, start_column, 1)
                else:
                    self._next_chr()
                    yield Token(TokenKind.Invalid, self.source, start, start_line, start_column, 1, "Unknown character")

        while True:
            yield Token(TokenKind.EndOfFile, self.source, self.position, self.line, self.column, 0)

    def _lex_whitespace(self: Lexer, start: int, start_column: int, start_line: int) -> Generator[Token, None, None]:
        length: int = 0

        while self._current.isspace():
            self._next_chr()
            length += 1

        yield Token(TokenKind.Whitespace, self.source, start, start_line, start_column, length)

    def _lex_identifier(self: Lexer, start: int, start_column: int, start_line: int) -> Generator[Token, None, None]:
        length: int = 0

        identifier: str = ""
        while self._current.isalpha() or self._current.isdigit() \
                or self._current == '_' or self._current == '\\':
            if self._current == '\\':
                self._next_chr()
                length += 1

                length += self._skip_whitespace_and_comments()
            else:
                identifier += self._next_chr()
                length += 1

        yield Token(TokenKind.Identifier, self.source, start, start_line, start_column, length, identifier)

    def _lex_number(self: Lexer, start: int, start_column: int, start_line: int) -> Generator[Token, None, None]:
        length: int = 0
        base: int = 10
        int_value: int = 0

        if self._current == '0':
            self._next_chr()
            length += 1
            if self._current == 'x' or self._current == 'X':
                self._next_chr()
                length += 1
                base = 16
            elif self._current == 'b' or self._current == 'B':
                self._next_chr()
                length += 1
                base = 2
            else:
                base = 10

        while self._current.isdigit() or self._current.isalpha():
            number: int = chr_to_int(self._current, base)
            if number >= base:
                yield Token(TokenKind.Invalid, self.source, self.position, self.line, self.column, 1,
                            "Digit cannot be bigger than base")

            int_value *= base
            int_value += number

            self._next_chr()
            length += 1

        if self._current == '.':  # Float literal
            self._next_chr()
            length += 1

            float_value: float = float(int_value)
            divisor: int = 1

            while self._current.isdigit() or self._current.isalpha():
                number: int = chr_to_int(self._current, base)
                if number >= base:
                    yield Token(TokenKind.Invalid, self.source, self.position, self.line, self.column, 1,
                                "Digit cannot be bigger than base")

                divisor *= base
                float_value += float(number) / float(divisor)

                self._next_chr()
                length += 1

            yield Token(TokenKind.Float, self.source, start, start_line, start_column, length, float_value)
        else:
            yield Token(TokenKind.Int, self.source, start, start_line, start_column, length, int_value)


def main() -> None:
    file = open("Test.lang", "r")
    if file:
        source: str = file.read()
        print(f"-------------- BEGIN_OF_SOURCE --------------\n{source}\n-------------- END_OF_SOURCE --------------")
        lexer = Lexer(source)
        tokens = lexer.get_tokens()
        while True:
            token: Token = next(tokens)
            if token.kind != TokenKind.Whitespace:
                print(f"{repr(token)}, text = {str(token)}")

            if token.kind == TokenKind.EndOfFile:
                break
    else:
        print("Unable to open 'Test.lang'")


if __name__ == "__main__":
    main()
