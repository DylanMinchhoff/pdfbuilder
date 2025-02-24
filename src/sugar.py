from collections.abc import Sequence
from dataclasses import dataclass
from typing import Annotated, Union
from kernel import Int, Let, Var, Bool, If, Unit, Cell, Get, Set, While


type Expression = Union[
    Int,
    Add[Expression],
    Subtract[Expression],
    Multiply[Expression],
    Let[Expression, Expression],
    Var,
    LetStar[Expression, Expression],
    Bool,
    Not[Expression],
    All[Expression],
    Any[Expression],
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
    Do[Expression],
    While[Expression, Expression],
]


@dataclass(frozen=True)
class Add[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Subtract[Operand]:
    operands: Annotated[Sequence[Operand], "non-empty"]


@dataclass(frozen=True)
class Multiply[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class LetStar[Value, Body]:
    bindings: Sequence[tuple[str, Value]]
    body: Body


@dataclass(frozen=True)
class Not[Operand]:
    x: Operand


@dataclass(frozen=True)
class All[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Any[Operand]:
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
class Do[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Program:
    parameters: Sequence[str]
    body: Expression
