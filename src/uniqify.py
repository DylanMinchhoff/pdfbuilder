from collections.abc import Callable, Mapping
from functools import partial
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


type Environment = Mapping[str, str]


def uniqify(
    program: Program,
    fresh: Callable[[str], str],
) -> Program:
    local = {x: fresh(x) for x in program.parameters}
    return Program(
        parameters=list(local.values()),
        body=uniqify_expr(program.body, local, fresh),
    )


def uniqify_expr(
    expr: Expression,
    env: Environment,
    fresh: Callable[[str], str],
) -> Expression:
    recur = partial(uniqify_expr, env=env, fresh=fresh)

    match expr:
        case Int():
            return expr

        case Add(e1, e2):
            return Add(recur(e1), recur(e2))

        case Subtract(e1, e2):
            return Subtract(recur(e1), recur(e2))

        case Multiply(e1, e2):
            return Multiply(recur(e1), recur(e2))

        case Let(x, e1, e2):
            y = fresh(x)
            return Let(y, recur(e1), recur(e2, env={**env, x: y}))

        case Var(x):
            return Var(env[x])

        case Bool():
            return expr

        case If(e1, e2, e3):
            return If(recur(e1), recur(e2), recur(e3))

        case LessThan(e1, e2):
            return LessThan(recur(e1), recur(e2))

        case EqualTo(e1, e2):
            return EqualTo(recur(e1), recur(e2))

        case GreaterThanOrEqualTo(e1, e2):
            return GreaterThanOrEqualTo(recur(e1), recur(e2))

        case Unit():
            return Unit()

        case Get(value):
            return Get(value)

        case Set(cell, value):
            return Set(cell, value)

        case Cell(value):
            return Cell(value)

        case Do(a, b):
            return Do(a, b)

        case While(cond, body):
            return While(cond, body)

        case _:  # pragma: no branch
            raise NotADirectoryError()
