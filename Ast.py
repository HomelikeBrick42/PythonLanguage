from typing import Optional, Dict, List
from enum import Enum, auto

from Token import Token


class AstKind(Enum):
    Program = auto()
    File = auto()
    Scope = auto()
    Declaration = auto()
    ConstDeclaration = auto()


class Ast:
    Ast: str = 'Ast'  # TODO: Change type from str to TypeAlias in python 3.10

    def __init__(self: Ast, kind: AstKind) -> None:
        self.kind = kind


class AstProgram(Ast):
    AstProgram: str = 'AstProgram'  # TODO: Change type from str to TypeAlias in python 3.10

    def __init__(self: AstProgram) -> None:
        super().__init__(AstKind.Program)
        self.files: Dict[str, AstFile] = {}


class AstFile(Ast):
    AstFile: str = 'AstFile'  # TODO: Change type from str to TypeAlias in python 3.10

    def __init__(self: AstFile, program: AstProgram) -> None:
        super().__init__(AstKind.File)
        self.statements: List[AstStatement] = []
        self.program: AstProgram = program


class AstStatement(Ast):
    AstStatement: str = 'AstStatement'  # TODO: Change type from str to TypeAlias in python 3.10

    def __init__(self: AstStatement, kind: AstKind, scope: Optional['AstScope'], file: AstFile) -> None:
        super().__init__(kind)
        self.scope: AstScope = scope
        self.file: AstFile = file


class AstScope(AstStatement):
    AstScope: str = 'AstScope'  # TODO: Change type from str to TypeAlias in python 3.10

    def __init__(self: AstScope, file: AstFile) -> None:
        super().__init__(AstKind.Scope, None, file)
        self.file: AstFile = file
        self.statements: List[AstStatement] = []


class AstDeclaration(AstStatement):
    AstDeclaration: str = 'AstDeclaration'  # TODO: Change type from str to TypeAlias in python 3.10

    def __init__(self: AstDeclaration, identifier: Token, type: 'AstType', value: Optional['AstExpression'],
                 scope: AstScope, file: AstFile) -> None:
        super().__init__(AstKind.Declaration, scope, file)
        self.identifier: Token = identifier
        self.type: 'AstType' = type
        self.value: Optional['AstExpression'] = value


class AstConstDeclaration(AstStatement):
    AstConstDeclaration: str = 'AstConstDeclaration'  # TODO: Change type from str to TypeAlias in python 3.10

    def __init__(self: AstConstDeclaration, identifier: Token, type: 'AstType', value: Optional['AstExpression'],
                 scope: AstScope, file: AstFile) -> None:
        super().__init__(AstKind.ConstDeclaration, scope, file)
        self.identifier: Token = identifier
        self.type: 'AstType' = type
        self.value: Optional['AstExpression'] = value


class AstExpression(AstStatement):
    AstExpression: str = 'AstExpression'  # TODO: Change type from str to TypeAlias in python 3.10

    def __init__(self: AstExpression, kind: AstKind, scope: AstScope, file: AstFile) -> None:
        super().__init__(kind, scope, file)


class AstBinaryOperator(AstExpression):
    AstBinaryOperator: str = 'AstBinaryOperator'  # TODO: Change type from str to TypeAlias in python 3.10

    def __init__(self: AstBinaryOperator, left: AstExpression, operator: Token, right: AstExpression, scope: AstScope,
                 file: AstFile) -> None:
        super().__init__(AstKind.BinaryOperator, scope, file)
        self.left: AstExpression = left
        self.operator: Token = operator
        self.right: AstExpression = right


class AstList(AstExpression):
    AstList: str = 'AstList'  # TODO: Change type from str to TypeAlias in python 3.10

    def __init__(self: AstList, scope: AstScope, file: AstFile) -> None:
        super().__init__(AstKind.List, scope, file)
        self.expressions: List[AstExpression] = []


class AstProcedure(AstExpression):
    AstProcedure: str = 'AstProcedure'  # TODO: Change type from str to TypeAlias in python 3.10

    def __init__(self: AstProcedure, parameters: AstList, , scope: AstScope, file: AstFile) -> None:
        super().__init__(AstKind.Procedure, scope, file)


class AstIntLiteral(AstExpression):
    AstIntLiteral: str = 'AstIntLiteral'  # TODO: Change type from str to TypeAlias in python 3.10

    def __init__(self: AstIntLiteral, int_token: Token, scope: AstScope, file: AstFile) -> None:
        super().__init__(AstKind.IntLiteral, scope, file)
        self.int_token: Token = int_token


class AstFloatLiteral(AstExpression):
    AstFloatLiteral: str = 'AstFloatLiteral'  # TODO: Change type from str to TypeAlias in python 3.10

    def __init__(self: AstFloatLiteral, float_token: Token, scope: AstScope, file: AstFile) -> None:
        super().__init__(AstKind.FloatLiteral, scope, file)
        self.float_token: Token = float_token


class AstStringLiteral(AstExpression):
    AstStringLiteral: str = 'AstStringLiteral'  # TODO: Change type from str to TypeAlias in python 3.10

    def __init__(self: AstStringLiteral, string_token: Token, scope: AstScope, file: AstFile) -> None:
        super().__init__(AstKind.StringLiteral, scope, file)
        self.string_token: Token = string_token
