from typing import Generator, Dict, Tuple

from Token import Token, TokenKind


def chr_to_int(char: chr, base: int) -> int:
    if '0' <= char <= '9':
        return int(char) - int('0')
    elif 'a' <= char <= 'z':
        return int(char) - int('a') + 10
    elif 'A' <= char <= 'Z':
        if base > 36:
            pass
        else:
            return int(char) - int('A') + 10

    raise NotImplementedError  # TODO: Char to int


class Lexer:
    Lexer: str = 'Lexer'  # TODO: Change type from str to TypeAlias in python 3.10
    _CharToTokenKind: Dict[chr, TokenKind] = {
        '.': TokenKind.Period,
        ',': TokenKind.Comma,
        '#': TokenKind.Hash,
        '^': TokenKind.Caret,
        ':': TokenKind.Colon,
        ';': TokenKind.Semicolon,

        '(': TokenKind.OpenParentheses,
        ')': TokenKind.CloseParentheses,
        '[': TokenKind.OpenSquareBracket,
        ']': TokenKind.CloseSquareBracket,
        '{': TokenKind.OpenBracket,
        '}': TokenKind.CloseBracket,

        '+': TokenKind.Plus,
        '-': TokenKind.Minus,
        '*': TokenKind.Asterisk,
        '/': TokenKind.Slash,
        '%': TokenKind.Percent,
        '=': TokenKind.Equals,
        '!': TokenKind.ExclamationMark,
        '<': TokenKind.LessThan,
        '>': TokenKind.GreaterThan,
    }

    _DoubleCharToTokenKind: Dict[Tuple[chr, chr], TokenKind] = {
        ('+', '='): TokenKind.PlusEquals,
        ('-', '='): TokenKind.MinusEquals,
        ('*', '='): TokenKind.AsteriskEquals,
        ('/', '='): TokenKind.SlashEquals,
        ('%', '='): TokenKind.PercentEquals,
        ('=', '='): TokenKind.EqualsEquals,
        ('!', '='): TokenKind.ExclamationMarkEquals,
        ('<', '='): TokenKind.LessThanEquals,
        ('>', '='): TokenKind.GreaterThanEquals,
        ('.', '.'): TokenKind.PeriodPeriod,
        ('-', '>'): TokenKind.RightArrow,
    }

    def __init__(self: Lexer, source: str) -> None:
        self._source: str = source
        self._position: int = 0
        self._line: int = 1
        self._column: int = 1

    def _peek(self: Lexer, offset: int) -> chr:
        index: int = self._position + offset
        if index >= len(self._source):
            return '\0'
        return self._source[index]

    @property
    def _current(self: Lexer) -> chr:
        return self._peek(0)

    def _next_chr(self: Lexer) -> chr:
        current: chr = self._current
        if self._current == '\n':
            self._line += 1
            self._column = 1
        else:
            self._column += 1
        self._position += 1
        return current

    def _skip_whitespace_and_comments(self: Lexer) -> int:
        raise NotImplementedError  # TODO: Skip whitespace and comments

    def get_tokens(self: Lexer) -> Generator[Token, None, None]:
        while self._current != '\0':
            start: int = self._position
            start_line: int = self._line
            start_column: int = self._column

            if self._current.isspace():
                yield from self._lex_whitespace(start, start_column, start_line)
            elif self._current == '/' and self._peek(1) == '/':
                raise NotImplementedError  # TODO: Single line comment
            elif self._current == '/' and self._peek(1) == '*':
                raise NotImplementedError  # TODO: Block comment
            elif self._current.isalpha() or self._current == '_':
                yield from self._lex_identifier(start, start_column, start_line)
            elif self._current.isdigit() or (self._current == '.' and self._peek(1).isdigit()):
                yield from self._lex_number(start, start_column, start_line)
            elif self._current == '\"':
                yield from self._lex_string(start, start_column, start_line)
            else:
                if (self._current, self._peek(1)) in self._DoubleCharToTokenKind:
                    char1: chr = self._current
                    self._next_chr()
                    char2: chr = self._current
                    self._next_chr()
                    yield Token(self._DoubleCharToTokenKind[(char1, char2)], self._source, start, start_line, start_column, 2)
                elif self._current in self._CharToTokenKind:
                    char: chr = self._current
                    self._next_chr()
                    yield Token(self._CharToTokenKind[char], self._source, start, start_line, start_column, 1)
                else:
                    self._next_chr()
                    yield Token(TokenKind.Invalid, self._source, start, start_line, start_column, 1, "Unknown character")

        while True:
            yield Token(TokenKind.EndOfFile, self._source, self._position, self._line, self._column, 0)

    def _lex_string(self: Lexer, start: int, start_column: int, start_line: int) -> Generator[Token, None, None]:
        length: int = 0

        self._next_chr()
        length += 1

        value: str = ""
        while self._current != '\"' and self._current != '\0':
            if self._current == '\\':
                self._next_chr()
                length += 1

                if self._current == '0':
                    value += '\0'
                    self._next_chr()
                    length += 1
                elif self._current == 'n' or self._current == 'N':
                    value += '\n'
                    self._next_chr()
                    length += 1
                elif self._current == 'r' or self._current == 'R':
                    value += '\r'
                    self._next_chr()
                    length += 1
                elif self._current == '\\':
                    value += '\\'
                    self._next_chr()
                    length += 1
                elif self._current == '\"':
                    value += '\"'
                    self._next_chr()
                    length += 1
                elif self._current == '\'':
                    value += '\''
                    self._next_chr()
                    length += 1
                else:
                    yield Token(TokenKind.Invalid, self._source, self._position, self._line, self._column, 1,
                                "Unknown escaped string literal")
                    value += self._current
                    self._next_chr()
                    length += 1
            else:
                value += self._current
                self._next_chr()
                length += 1
        if self._current == '\0':
            yield Token(TokenKind.Invalid, self._source, start, start_line, start_column, 1,
                        "String literal is unclosed at end of file")

        self._next_chr()
        length += 1

        yield Token(TokenKind.String, self._source, start, start_line, start_column, length, value)

    def _lex_whitespace(self: Lexer, start: int, start_column: int, start_line: int) -> Generator[Token, None, None]:
        length: int = 0

        while self._current.isspace():
            self._next_chr()
            length += 1

        yield Token(TokenKind.Whitespace, self._source, start, start_line, start_column, length)

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

        yield Token(TokenKind.Identifier, self._source, start, start_line, start_column, length, identifier)

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
                yield Token(TokenKind.Invalid, self._source, self._position, self._line, self._column, 1,
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
                    yield Token(TokenKind.Invalid, self._source, self._position, self._line, self._column, 1,
                                "Digit cannot be bigger than base")

                divisor *= base
                float_value += float(number) / float(divisor)

                self._next_chr()
                length += 1

            yield Token(TokenKind.Float, self._source, start, start_line, start_column, length, float_value)
        else:
            yield Token(TokenKind.Int, self._source, start, start_line, start_column, length, int_value)
