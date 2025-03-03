from collections.abc import Sequence
from dataclasses import dataclass
from typing import Union
from sucrose import (
    Int,
    Var,
    Bool,
    If,
    Unit,
    Lambda,
    Apply,
    Assign,
)

type Expression = Union[
    Int,
    Add[Expression],
    Subtract[Expression],
    Multiply[Expression],
    Let[Expression, Expression],
    LetStar[Expression, Expression],
    LetRec[Expression, Expression],
    Var,
    Bool,
    Not[Expression],
    And[Expression],
    Or[Expression],
    If[Expression, Expression, Expression],
    Cond[Expression, Expression, Expression],
    LessThanOrEqualTo[Expression],
    LessThan[Expression],
    EqualTo[Expression],
    GreaterThan[Expression],
    GreaterThanOrEqualTo[Expression],
    Unit,
    Cell[Expression],
    Get[Expression],
    Set[Expression],
    Begin[Expression],
    While[Expression, Expression],
    Lambda[Expression],
    Apply[Expression],
    Assign[Expression],
]


@dataclass(frozen=True)
class Add[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Subtract[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Multiply[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Let[Value, Body]:
    bindings: Sequence[tuple[str, Value]]
    body: Body


@dataclass(frozen=True)
class LetStar[Value, Body]:
    bindings: Sequence[tuple[str, Value]]
    body: Body


@dataclass(frozen=True)
class LetRec[Value, Body]:
    bindings: Sequence[tuple[str, Value]]
    body: Body


@dataclass(frozen=True)
class Not[Operand]:
    operand: Operand


@dataclass(frozen=True)
class And[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Or[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Cond[Condition, Consequent, Default]:
    arms: Sequence[tuple[Condition, Consequent]]
    default: Default


@dataclass(frozen=True)
class LessThanOrEqualTo[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class LessThan[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class EqualTo[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class GreaterThan[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class GreaterThanOrEqualTo[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Cell[Operand]:
    value: Operand


@dataclass(frozen=True)
class Get[Operand]:
    cell: Operand


@dataclass(frozen=True)
class Set[Operand]:
    cell: Operand
    value: Operand


@dataclass(frozen=True)
class Begin[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class While[Condition, Body]:
    condition: Condition
    body: Body


@dataclass(frozen=True)
class Program:
    parameters: Sequence[str]
    definitions: Sequence[tuple[str, Expression]]
    body: Expression
