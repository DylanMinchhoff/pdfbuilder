from collections.abc import Sequence, Mapping
from dataclasses import dataclass
from functools import partial
from typing import Union
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
    Unit,
    Cell,
    Get,
    Set,
    Do,
    While,
)
from store import Store


@dataclass(frozen=True)
class Location:
    value: int


type Value = Union[Int, Bool, Unit, Location]

type Environment = Mapping[str, Value]


def eval(
    program: Program,
    arguments: Sequence[Int],
) -> Value:
    return eval_expr(
        expr=program.body,
        env={p: a for p, a in zip(program.parameters, arguments, strict=True)},
        store=Store(),
    )


def eval_expr(
    expr: Expression,
    env: Environment,
    store: Store[Value],
) -> Value:
    recur = partial(eval_expr, env=env, store=store)
    match expr:
        case Int():
            return expr

        case Add(e1, e2):
            match recur(e1), recur(e2):
                case [Int(i1), Int(i2)]:
                    return Int(i1 + i2)
                case _:  # pragma: no cover
                    raise ValueError()

        case Subtract(e1, e2):
            match recur(e1), recur(e2):
                case [Int(i1), Int(i2)]:
                    return Int(i1 - i2)
                case _:  # pragma: no cover
                    raise ValueError()

        case Multiply(e1, e2):
            match recur(e1), recur(e2):
                case [Int(i1), Int(i2)]:
                    return Int(i1 * i2)
                case _:  # pragma: no cover
                    raise ValueError()

        case Let(x, e1, e2):
            return recur(e2, env={**env, x: recur(e1)})

        case Var(x):
            return env[x]

        case Bool():
            return expr

        case If(e1, e2, e3):
            match recur(e1):
                case Bool(True):
                    return recur(e2)
                case Bool(False):
                    return recur(e3)
                case _:  # pragma: no cover
                    raise ValueError()

        case LessThan(e1, e2):
            match recur(e1), recur(e2):
                case [Int(i1), Int(i2)]:
                    return Bool(i1 < i2)
                case _:  # pragma: no cover
                    raise ValueError()

        case EqualTo(e1, e2):
            match recur(e1), recur(e2):
                case [Int(i1), Int(i2)]:
                    return Bool(i1 == i2)
                case [Bool(b1), Bool(b2)]:
                    return Bool(b1 == b2)
                case _:  # pragma: no cover
                    raise ValueError()

        case GreaterThanOrEqualTo(e1, e2):
            match recur(e1), recur(e2):
                case [Int(i1), Int(i2)]:
                    return Bool(i1 >= i2)
                case _:  # pragma: no cover
                    raise ValueError()

        case Cell(value):
            return Location(store.next_free)

        case Get(cell):
            return cell.value

        case Set(cell, value):
            Store[Cell(value)]
            return Unit()

        case Do(first, second):
            recur(first)
            return recur(second)

        case While(condition, body):
            while condition == Bool(True):
                recur(body)
            return Unit()

        case Unit():
            return Unit()

        case _:  # pragma: no branch
            raise NotImplementedError()
