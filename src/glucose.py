from collections.abc import Sequence
from dataclasses import dataclass
from typing import Union

type Expression = Union[
    Int,
    Add[Expression],
    Subtract[Expression],
    Multiply[Expression],
    Var,
    Bool,
    If[Expression, Expression, Expression],
    LessThan[Expression],
    EqualTo[Expression],
    GreaterThanOrEqualTo[Expression],
    Unit,
    Tuple[Expression],
    Get[Expression],
    Set[Expression],
    Lambda[Expression],
    Apply[Expression],
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
class Unit:
    pass


@dataclass(frozen=True)
class Tuple[Operand]:
    components: Sequence[Operand]


@dataclass(frozen=True)
class Get[Operand]:
    tuple: Operand
    index: Operand


@dataclass(frozen=True)
class Set[Operand]:
    tuple: Operand
    index: Operand
    value: Operand


@dataclass(frozen=True)
class Lambda[Body]:
    parameters: Sequence[str]
    body: Body


@dataclass(frozen=True)
class Apply[Operand]:
    callee: Operand
    arguments: Sequence[Operand]


@dataclass(frozen=True)
class Program:
    parameters: Sequence[str]
    body: Expression
