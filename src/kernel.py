from collections.abc import Sequence
from dataclasses import dataclass
from typing import Union


type Expression = Union[
    Int,
    Add[Expression],
    Subtract[Expression],
    Multiply[Expression],
    Let[Expression, Expression],
    Var,
    Bool,
    If[Expression, Expression, Expression],
    LessThan[Expression],
    EqualTo[Expression],
    GreaterThanOrEqualTo[Expression],
]


@dataclass(frozen=True)
class Int:
    value: int


@dataclass(frozen=True)
class Add[Operand]:
    x: Operand
    y: Operand


@dataclass(frozen=True)
class Subtract[Operand]:
    x: Operand
    y: Operand


@dataclass(frozen=True)
class Multiply[Operand]:
    x: Operand
    y: Operand


@dataclass(frozen=True)
class Let[Value, Name]:
    name: str
    value: Value
    body: Name


@dataclass(frozen=True)
class Var:
    name: str


@dataclass(frozen=True)
class Bool:
    value: bool


@dataclass(frozen=True)
class If[Condition, Consequent, Alternative]:
    condition: Condition
    consequent: Consequent
    alternative: Alternative


@dataclass(frozen=True)
class LessThan[Operand]:
    x: Operand
    y: Operand


@dataclass(frozen=True)
class EqualTo[Operand]:
    x: Operand
    y: Operand


@dataclass(frozen=True)
class GreaterThanOrEqualTo[Operand]:
    x: Operand
    y: Operand


@dataclass(frozen=True)
class Program:
    parameters: Sequence[str]
    body: Expression
