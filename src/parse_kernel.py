import os
from lark import (
    Lark,
    ParseTree,
    Token,
    Transformer,
    v_args,  # type: ignore
)
from kernel import (
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
class AstTransformer(Transformer[Token, Expression]):
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
        e1: Expression,
        e2: Expression,
    ) -> LessThan[Expression]:
        return LessThan(e1, e2)

    def equal_to_expr(
        self,
        e1: Expression,
        e2: Expression,
    ) -> EqualTo[Expression]:
        return EqualTo(e1, e2)

    def greater_than_or_equal_to_expr(
        self,
        e1: Expression,
        e2: Expression,
    ) -> GreaterThanOrEqualTo[Expression]:
        return GreaterThanOrEqualTo(e1, e2)

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


def parse_expr(
    source: str,
) -> Expression:
    with open(os.path.join(__location__, "./kernel.lark"), "r") as f:
        parser = Lark(f, start="expr")
        tree: ParseTree = parser.parse(source)
        return AstTransformer().transform(tree)  # type: ignore
