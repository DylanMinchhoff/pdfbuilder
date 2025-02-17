from collections.abc import Sequence
from dataclasses import dataclass
from typing import Annotated, Union
import kernel

type Expression = Union[
    kernel.Int,
    kernel.Add[Expression],
    kernel.Subtract[Expression],
    kernel.Multiply[Expression],
    kernel.Let[Expression, Expression],
    kernel.Var,
    kernel.Bool,
    kernel.If[Expression, Expression, Expression],
    kernel.LessThan[Expression],
    kernel.EqualTo[Expression],
    kernel.GreaterThanOrEqualTo[Expression],
    #
    Sum[Expression],
    Difference[Expression],
    Product[Expression],
    LetStar[Expression, Expression],
    Not[Expression],
    All[Expression],
    Any[Expression],
    Cond[Expression, Expression, Expression],
    NonDescending[Expression],
    Ascending[Expression],
    Same[Expression],
    Descending[Expression],
    NonAscending[Expression],
]


@dataclass(frozen=True)
class Sum[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Difference[Operand]:
    operands: Annotated[Sequence[Operand], "non-empty"]


@dataclass(frozen=True)
class Product[Operand]:
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
class NonDescending[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Ascending[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Same[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Descending[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class NonAscending[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Program:
    parameters: Sequence[str]
    body: Expression
