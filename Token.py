from enum import Enum, auto
from typing import Union, Any


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
    Hash = auto()
    Caret = auto()
    Colon = auto()
    Semicolon = auto()
    RightArrow = auto()
    PeriodPeriod = auto()

    OpenParentheses = auto()
    CloseParentheses = auto()
    OpenSquareBracket = auto()
    CloseSquareBracket = auto()
    OpenBracket = auto()
    CloseBracket = auto()

    Plus = auto()
    Minus = auto()
    Asterisk = auto()
    Slash = auto()
    Percent = auto()
    Equals = auto()
    ExclamationMark = auto()
    LessThan = auto()
    GreaterThan = auto()

    PlusEquals = auto()
    MinusEquals = auto()
    AsteriskEquals = auto()
    SlashEquals = auto()
    PercentEquals = auto()
    EqualsEquals = auto()
    ExclamationMarkEquals = auto()
    LessThanEquals = auto()
    GreaterThanEquals = auto()


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
