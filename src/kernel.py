from collections.abc import Sequence
from dataclasses import dataclass
from typing import Union


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
    x: Expression
    y: Expression


@dataclass(frozen=True)
class Subtract:
    x: Expression
    y: Expression


@dataclass(frozen=True)
class Multiply:
    x: Expression
    y: Expression


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
