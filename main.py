from typing import Union, Optional, Any, Generator, Dict, Tuple, List
from enum import Enum, auto

from Token import Token, TokenKind
from Lexer import Lexer
from Ast import *


def main() -> None:
    file = open("Test.lang", "r")
    if file:
        source: str = file.read()
        print(f"-------------- BEGIN_OF_SOURCE --------------\n{source}\n-------------- END_OF_SOURCE --------------")
    else:
        print("Unable to open 'Test.lang'")


if __name__ == "__main__":
    main()
