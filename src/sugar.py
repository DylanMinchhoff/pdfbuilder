from collections.abc import Sequence
from dataclasses import dataclass
from typing import Annotated, Union


type Expression = Union[
    Int,
    Add,
    Subtract,
    Multiply,
    Let,
    Var,
]


@dataclass(frozen=True)
class Int:
    value: int


@dataclass(frozen=True)
class Add:
    operands: Sequence[Expression]


@dataclass(frozen=True)
class Subtract:
    operands: Annotated[Sequence[Expression], "non-empty"]


@dataclass(frozen=True)
class Multiply:
    operands: Sequence[Expression]


@dataclass(frozen=True)
class Let:
    name: str
    value: Expression
    body: Expression


@dataclass(frozen=True)
class Var:
    name: str


@dataclass(frozen=True)
class Program:
    parameters: Sequence[str]
    body: Expression
