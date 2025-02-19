from collections.abc import Sequence
import os
from typing import Any
from lark import (
    Lark,
    ParseTree,
    Token,
    Transformer,
    v_args,  # type: ignore
)
from kernel import (
    Program,
    Expression,
    Int,
    Add,
    Subtract,
    Multiply,
    Let,
    Var,
    Bool,
    If,
    LessThan,
    EqualTo,
    GreaterThanOrEqualTo,
)


@v_args(inline=True)
class AstTransformer(Transformer[Token, Any]):
    def program(
        self,
        parameters: Sequence[str],
        body: Expression,
    ) -> Program:
        return Program(parameters, body)

    @v_args(inline=False)
    def parameters(
        self,
        parameters: Sequence[str],
    ) -> Sequence[str]:
        return parameters

    def int_expr(
        self,
        value: int,
    ) -> Int:
        return Int(value)

    def add_expr(
        self,
        x: Expression,
        y: Expression,
    ) -> Add[Expression]:
        return Add(x, y)

    def subtract_expr(
        self,
        x: Expression,
        y: Expression,
    ) -> Subtract[Expression]:
        return Subtract(x, y)

    def multiply_expr(
        self,
        x: Expression,
        y: Expression,
    ) -> Multiply[Expression]:
        return Multiply(x, y)

    def let_expr(
        self,
        name: str,
        value: Expression,
        body: Expression,
    ) -> Let[Expression, Expression]:
        return Let(name, value, body)

    def var_expr(
        self,
        name: str,
    ) -> Var:
        return Var(name)

    def bool_expr(
        self,
        value: bool,
    ) -> Bool:
        return Bool(value)

    def if_expr(
        self,
        condition: Expression,
        consequent: Expression,
        alternative: Expression,
    ) -> If[Expression, Expression, Expression]:
        return If(condition, consequent, alternative)

    def less_than_expr(
        self,
        x: Expression,
        y: Expression,
    ) -> LessThan[Expression]:
        return LessThan(x, y)

    def equal_to_expr(
        self,
        x: Expression,
        y: Expression,
    ) -> EqualTo[Expression]:
        return EqualTo(x, y)

    def greater_than_or_equal_to_expr(
        self,
        x: Expression,
        y: Expression,
    ) -> GreaterThanOrEqualTo[Expression]:
        return GreaterThanOrEqualTo(x, y)

    def int(
        self,
        value: Token,
    ) -> int:
        return int(value)

    def true(
        self,
        value: Token,
    ) -> bool:
        return True

    def false(
        self,
        value: Token,
    ) -> bool:
        return False

    def identifier(
        self,
        value: Token,
    ) -> str:
        return str(value)


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def parse(
    source: str,
) -> Program:
    with open(os.path.join(__location__, "./kernel.lark"), "r") as f:
        parser = Lark(f, start="program")
        tree: ParseTree = parser.parse(source)
        return AstTransformer().transform(tree)  # type: ignore


def parse_expr(
    source: str,
) -> Expression:
    with open(os.path.join(__location__, "./kernel.lark"), "r") as f:
        parser = Lark(f, start="expr")
        tree: ParseTree = parser.parse(source)
        return AstTransformer().transform(tree)  # type: ignore
