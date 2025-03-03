from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from functools import partial
from typing import Union
from glucose import (
    Program,
    Expression,
    Int,
    Add,
    Subtract,
    Multiply,
    Var,
    Bool,
    If,
    LessThan,
    EqualTo,
    GreaterThanOrEqualTo,
    Unit,
    Tuple,
    Get,
    Set,
    Lambda,
    Apply,
)
from store import Store


type Value = Union[
    Int,
    Bool,
    Unit,
    Location,
    Closure,
]

type Environment = Mapping[str, Value]


@dataclass(frozen=True)
class Location:
    value: int


@dataclass(frozen=True)
class Closure:
    abs: Lambda[Expression]
    env: Environment


def eval(
    program: Program,
    arguments: Sequence[Value],
) -> Value:
    return eval_expression(
        expr=program.body,
        env={p: a for p, a in zip(program.parameters, arguments, strict=True)},
        store=Store(),
    )


def eval_expression(
    expr: Expression,
    env: Environment,
    store: Store[Value],
) -> Value:
    recur = partial(eval_expression, env=env, store=store)
    match expr:
        case Int():
            return expr

        case Add(x, y):
            match recur(x), recur(y):
                case [Int(i1), Int(i2)]:
                    return Int(i1 + i2)
                case [x, y]:  # pragma: no cover
                    raise ValueError()

        case Subtract(x, y):
            match recur(x), recur(y):
                case [Int(i1), Int(i2)]:
                    return Int(i1 - i2)
                case [x, y]:  # pragma: no cover
                    raise ValueError()

        case Multiply(x, y):
            match recur(x), recur(y):
                case [Int(i1), Int(i2)]:
                    return Int(i1 * i2)
                case [x, y]:  # pragma: no cover
                    raise ValueError()

        case Var(x):
            return env[x]

        case Bool():
            return expr

        case If(condition, consequent, alternative):
            match recur(condition):
                case Bool(True):
                    return recur(consequent)
                case Bool(False):
                    return recur(alternative)
                case _:  # pragma: no cover
                    raise ValueError()

        case LessThan(x, y):
            match recur(x), recur(y):
                case [Int(i1), Int(i2)]:
                    return Bool(i1 < i2)
                case [x, y]:  # pragma: no cover
                    raise ValueError()

        case EqualTo(x, y):
            match recur(x), recur(y):
                case [Int(i1), Int(i2)]:
                    return Bool(i1 == i2)
                case [Bool(b1), Bool(b2)]:
                    return Bool(b1 == b2)
                case [x, y]:  # pragma: no cover
                    raise ValueError()

        case GreaterThanOrEqualTo(x, y):
            match recur(x), recur(y):
                case [Int(i1), Int(i2)]:
                    return Bool(i1 >= i2)
                case [x, y]:  # pragma: no cover
                    raise ValueError()

        case Unit():
            return expr

        case Tuple(es):
            base = store.malloc(1)
            for i, e in enumerate(es):
                store[base, i] = recur(e)
            return Location(base)

        case Get(tuple, index):
            match recur(tuple), recur(index):
                case [Location(base), Int(offset)]:
                    return store[base, offset]
                case _:  # pragma: no cover
                    raise ValueError()

        case Set(tuple, index, value):
            match recur(tuple), recur(index):
                case [Location(base), Int(offset)]:
                    store[base, offset] = recur(value)
                    return Unit()
                case tuple, index:  # pragma: no cover
                    raise ValueError()

        case Lambda():
            raise NotImplementedError()

        case Apply(callee, arguments):  # pragma: no branch
            raise NotImplementedError()
