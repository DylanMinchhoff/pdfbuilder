from functools import partial
import sugar
from sugar import (
    Int,
    Let,
    Var,
    LetStar,
    Bool,
    Not,
    All,
    Any,
    If,
    Cond,
    Unit,
    Cell,
    Get,
    Set,
    While,
)
import kernel


def desugar(
    program: sugar.Program,
) -> kernel.Program:
    return kernel.Program(
        parameters=program.parameters,
        body=desugar_expr(program.body),
    )


def desugar_expr(
    expr: sugar.Expression,
) -> kernel.Expression:
    recur = partial(desugar_expr)

    match expr:
        case Int():
            return expr

        case sugar.Add(es):
            match es:
                case []:
                    return Int(0)
                case [first, *rest]:
                    return kernel.Add(recur(first), recur(sugar.Add(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.Subtract(es):
            match es:
                case [first]:
                    return kernel.Subtract(Int(0), recur(first))
                case [first, second]:
                    return kernel.Subtract(recur(first), recur(second))
                case [first, *rest]:
                    return kernel.Subtract(recur(first), recur(sugar.Subtract(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.Multiply(es):
            match es:
                case []:
                    return Int(1)
                case [first, *rest]:
                    return kernel.Multiply(recur(first), recur(sugar.Multiply(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case Let(x, e1, e2):
            return Let(x, recur(e1), recur(e2))

        case Var():
            return expr

        case LetStar(bindings, body):
            match bindings:
                case []:
                    return recur(body)
                case [[x, e1], *rest]:
                    return Let(x, recur(e1), recur(LetStar(rest, body)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case Bool():
            return expr

        case Not(e1):
            return If(kernel.EqualTo(recur(e1), Bool(True)), Bool(False), Bool(True))

        case All(es):
            match es:
                case []:
                    return Bool(True)
                case [first, *rest]:
                    return If(recur(first), recur(All(rest)), Bool(False))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case Any(es):
            match es:
                case []:
                    return Bool(False)
                case [first, *rest]:
                    return If(recur(first), Bool(True), recur(Any(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case If(e1, e2, e3):
            return If(recur(e1), recur(e2), recur(e3))

        case Cond(arms, default):
            match arms:
                case []:
                    return recur(default)
                case [[e1, e2], *rest]:
                    return If(recur(e1), recur(e2), recur(Cond(rest, default)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.LessThanOrEqualTo(es):
            match es:
                case [] | [_]:
                    return Bool(True)
                case [first, second]:
                    return kernel.GreaterThanOrEqualTo(recur(second), recur(first))
                case [first, second, *rest]:
                    return If(
                        kernel.GreaterThanOrEqualTo(recur(second), recur(first)),
                        recur(sugar.LessThanOrEqualTo([second, *rest])),
                        Bool(False),
                    )
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.LessThan(es):
            match es:
                case [] | [_]:
                    return Bool(True)
                case [first, second]:
                    return kernel.LessThan(recur(first), recur(second))
                case [first, second, *rest]:
                    return If(
                        kernel.LessThan(recur(first), recur(second)),
                        recur(sugar.LessThan([second, *rest])),
                        Bool(False),
                    )
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.EqualTo(es):
            match es:
                case [] | [_]:
                    return Bool(True)
                case [first, second]:
                    return kernel.EqualTo(recur(first), recur(second))
                case [first, second, *rest]:
                    return If(
                        kernel.EqualTo(recur(first), recur(second)),
                        recur(sugar.EqualTo([second, *rest])),
                        Bool(False),
                    )
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.GreaterThan(es):
            match es:
                case [] | [_]:
                    return Bool(True)
                case [first, second]:
                    return kernel.LessThan(recur(second), recur(first))
                case [first, second, *rest]:
                    return If(
                        kernel.LessThan(recur(second), recur(first)),
                        recur(sugar.GreaterThan([second, *rest])),
                        Bool(False),
                    )
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.GreaterThanOrEqualTo(es):  # pragma: no branch
            match es:
                case [] | [_]:
                    return Bool(True)
                case [first, second]:
                    return kernel.GreaterThanOrEqualTo(recur(first), recur(second))
                case [first, second, *rest]:
                    return If(
                        kernel.GreaterThanOrEqualTo(recur(first), recur(second)),
                        recur(sugar.GreaterThanOrEqualTo([second, *rest])),
                        Bool(False),
                    )

                case _:  # pragma: no cover
                    raise NotImplementedError()

        case _:  # pragma: no branch
            raise NotImplementedError()
