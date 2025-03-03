from collections.abc import Sequence
from functools import partial
import sucrose
from sucrose import (
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
    Assign,
    Lambda,
    Apply,
)
import glucose


def convert_assignments(
    program: sucrose.Program,
) -> glucose.Program:
    vars = mutable_free_variables(program.body)
    return glucose.Program(
        program.parameters,
        _wrap_vars(list(vars), convert_assignments_expresssion(program.body, vars)),
    )


def convert_assignments_expresssion(
    expr: sucrose.Expression,
    vars: set[str],
) -> glucose.Expression:
    recur = partial(convert_assignments_expresssion, vars=vars)

    match expr:
        case Int():
            return expr

        case Add(x, y):
            return Add(recur(x), recur(y))

        case Subtract(x, y):
            return Subtract(recur(x), recur(y))

        case Multiply(x, y):
            return Multiply(recur(x), recur(y))

        case Var(name):
            return Get(expr, Int(0)) if name in vars else expr

        case Bool():
            return expr

        case If(condition, consequent, alternative):
            return If(recur(condition), recur(consequent), recur(alternative))

        case LessThan(x, y):
            return LessThan(recur(x), recur(y))

        case EqualTo(x, y):
            return EqualTo(recur(x), recur(y))

        case GreaterThanOrEqualTo(x, y):
            return GreaterThanOrEqualTo(recur(x), recur(y))

        case Unit():
            return expr

        case Tuple(components):
            return Tuple([recur(e) for e in components])

        case Get(tuple, index):
            return Get(recur(tuple), recur(index))

        case Set(tuple, index, value):
            return Set(recur(tuple), recur(index), recur(value))

        case Lambda(parameters, body):
            (vars_m, vars_u) = _partition(set(parameters), body)
            local_m = (vars | vars_m) - vars_u
            return Lambda(parameters, _wrap_vars(list(vars_m), recur(body, vars=local_m)))

        case Apply(callee, arguments):
            return Apply(recur(callee), [recur(e) for e in arguments])

        case Assign(name, value):  # pragma: no branch
            return Set(Var(name), Int(0), recur(value))


def _wrap_vars(
    vars: Sequence[str],
    expr: glucose.Expression,
) -> glucose.Expression:
    match vars:
        case []:
            return expr
        case vars:  # pragma: no branch
            return Apply(Lambda(list(vars), expr), [Tuple([Var(v)]) for v in vars])


def _partition(
    vars: set[str],
    *exprs: sucrose.Expression,
) -> tuple[set[str], set[str]]:
    mv = {mv for e in exprs for mv in mutable_free_variables(e)}
    return (vars & mv, vars - mv)


def mutable_free_variables(
    expr: sucrose.Expression,
) -> set[str]:
    recur = partial(mutable_free_variables)

    match expr:
        case Int():
            return set()

        case Add(x, y) | Subtract(x, y) | Multiply(x, y):
            return recur(x) | recur(y)

        case Var():
            return set()

        case Bool():
            return set()

        case If(condition, consequent, alternative):
            return recur(condition) | recur(consequent) | recur(alternative)

        case LessThan(x, y) | EqualTo(x, y) | GreaterThanOrEqualTo(x, y):
            return recur(x) | recur(y)

        case Unit():
            return set()

        case Tuple(components):
            return {mv for e in components for mv in recur(e)}

        case Get(tuple, index):
            return recur(tuple) | recur(index)

        case Set(tuple, index, value):
            return recur(tuple) | recur(index) | recur(value)

        case Lambda(parameters, body):
            return recur(body) - set(parameters)

        case Apply(callee, arguments):
            return recur(callee) | {mv for e in arguments for mv in recur(e)}

        case Assign(name, value):  # pragma: no branch
            return {name} | recur(value)
