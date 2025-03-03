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
from fructose import (
    Program,
    Expression,
    Int,
    Add,
    Subtract,
    Multiply,
    Let,
    LetStar,
    LetRec,
    Var,
    Bool,
    Not,
    And,
    Or,
    If,
    Cond,
    LessThanOrEqualTo,
    LessThan,
    EqualTo,
    GreaterThan,
    GreaterThanOrEqualTo,
    Unit,
    Cell,
    Get,
    Set,
    Begin,
    While,
    Lambda,
    Apply,
    Assign,
)


@v_args(inline=True)
class AstTransformer(Transformer[Token, Any]):
    def program(
        self,
        parameters: Sequence[str],
        definitions: Sequence[tuple[str, Expression]],
        body: Expression,
    ) -> Program:
        return Program(parameters, definitions, body)

    @v_args(inline=False)
    def parameters(
        self,
        parameters: Sequence[str],
    ) -> Sequence[str]:
        return parameters

    @v_args(inline=False)
    def definitions(
        self,
        definitions: Sequence[tuple[str, Expression]],
    ) -> Sequence[tuple[str, Expression]]:
        return definitions

    def value_def(
        self,
        name: str,
        value: Expression,
    ) -> tuple[str, Expression]:
        return name, value

    def function_def(
        self,
        name: str,
        parameters: Sequence[str],
        body: Expression,
    ) -> tuple[str, Expression]:
        return name, Lambda(parameters, body)

    def int_expr(
        self,
        value: int,
    ) -> Int:
        return Int(value)

    @v_args(inline=False)
    def add_expr(
        self,
        operands: Sequence[Expression],
    ) -> Add[Expression]:
        return Add(operands)

    @v_args(inline=False)
    def subtract_expr(
        self,
        operands: Sequence[Expression],
    ) -> Subtract[Expression]:
        return Subtract(operands)

    @v_args(inline=False)
    def multiply_expr(
        self,
        operands: Sequence[Expression],
    ) -> Multiply[Expression]:
        return Multiply(operands)

    def let_expr(
        self,
        bindings: Sequence[tuple[str, Expression]],
        body: Expression,
    ) -> Let[Expression, Expression]:
        return Let(bindings, body)

    def letstar_expr(
        self,
        bindings: Sequence[tuple[str, Expression]],
        body: Expression,
    ) -> LetStar[Expression, Expression]:
        return LetStar(bindings, body)

    def letrec_expr(
        self,
        bindings: Sequence[tuple[str, Expression]],
        body: Expression,
    ) -> LetRec[Expression, Expression]:
        return LetRec(bindings, body)

    @v_args(inline=False)
    def bindings(
        self,
        bindings: Sequence[tuple[str, Expression]],
    ) -> Sequence[tuple[str, Expression]]:
        return bindings

    def binding(
        self,
        name: str,
        value: Expression,
    ) -> tuple[str, Expression]:
        return name, value

    def var_expr(
        self,
        name: str,
    ) -> Var:
        return Var(name)

    def true_expr(
        self,
    ) -> Bool:
        return Bool(True)

    def false_expr(
        self,
    ) -> Bool:
        return Bool(False)

    def not_expr(
        self,
        operand: Expression,
    ) -> Not[Expression]:
        return Not(operand)

    @v_args(inline=False)
    def and_expr(
        self,
        operands: Sequence[Expression],
    ) -> And[Expression]:
        return And(operands)

    @v_args(inline=False)
    def or_expr(
        self,
        operands: Sequence[Expression],
    ) -> Or[Expression]:
        return Or(operands)

    def if_expr(
        self,
        condition: Expression,
        consequent: Expression,
        alternative: Expression,
    ) -> If[Expression, Expression, Expression]:
        return If(condition, consequent, alternative)

    def cond_expr(
        self,
        arms: Sequence[tuple[Expression, Expression]],
        default: Expression,
    ) -> Cond[Expression, Expression, Expression]:
        return Cond(arms, default)

    @v_args(inline=False)
    def arms(
        self,
        arms: Sequence[tuple[Expression, Expression]],
    ) -> Sequence[tuple[Expression, Expression]]:
        return arms

    def arm(
        self,
        condition: Expression,
        consequent: Expression,
    ) -> tuple[Expression, Expression]:
        return condition, consequent

    @v_args(inline=False)
    def less_than_or_equal_to_expr(
        self,
        operands: Sequence[Expression],
    ) -> LessThanOrEqualTo[Expression]:
        return LessThanOrEqualTo(operands)

    @v_args(inline=False)
    def less_than_expr(
        self,
        operands: Sequence[Expression],
    ) -> LessThan[Expression]:
        return LessThan(operands)

    @v_args(inline=False)
    def equal_to_expr(
        self,
        operands: Sequence[Expression],
    ) -> EqualTo[Expression]:
        return EqualTo(operands)

    @v_args(inline=False)
    def greater_than(
        self,
        operands: Sequence[Expression],
    ) -> GreaterThan[Expression]:
        return GreaterThan(operands)

    @v_args(inline=False)
    def greater_than_or_equal_to_expr(
        self,
        operands: Sequence[Expression],
    ) -> GreaterThanOrEqualTo[Expression]:
        return GreaterThanOrEqualTo(operands)

    def unit_expr(
        self,
    ) -> Unit:
        return Unit()

    def cell_expr(
        self,
        value: Expression,
    ) -> Cell[Expression]:
        return Cell(value)

    def get_expr(
        self,
        cell: Expression,
    ) -> Get[Expression]:
        return Get(cell)

    def set_expr(
        self,
        cell: Expression,
        value: Expression,
    ) -> Set[Expression]:
        return Set(cell, value)

    @v_args(inline=False)
    def begin_expr(
        self,
        operands: Sequence[Expression],
    ) -> Begin[Expression]:
        return Begin(operands)

    def while_expr(
        self,
        condition: Expression,
        body: Expression,
    ) -> While[Expression, Expression]:
        return While(condition, body)

    def lambda_expr(
        self,
        parameters: Sequence[str],
        body: Expression,
    ) -> Lambda[Expression]:
        return Lambda(parameters, body)

    @v_args(inline=False)
    def apply_expr(
        self,
        operands: Sequence[Expression],
    ) -> Apply[Expression]:
        callee, *arguments = operands
        return Apply(callee, arguments)

    def assign_expr(
        self,
        name: str,
        value: Expression,
    ) -> Assign[Expression]:
        return Assign(name, value)

    def int(
        self,
        value: Token,
    ) -> int:
        return int(value)

    def identifier(
        self,
        value: Token,
    ) -> str:
        return str(value)


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def parse(
    source: str,
) -> Program:
    with open(os.path.join(__location__, "./fructose.lark"), "r") as f:
        parser = Lark(f, start="program")
        tree: ParseTree = parser.parse(source)
        return AstTransformer().transform(tree)  # type: ignore


def parse_expression(
    source: str,
) -> Expression:
    with open(os.path.join(__location__, "./fructose.lark"), "r") as f:
        parser = Lark(f, start="expr")
        tree: ParseTree = parser.parse(source)
        return AstTransformer().transform(tree)  # type: ignore
