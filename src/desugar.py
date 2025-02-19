from functools import partial
import sugar
from sugar import (
    Sum,
    Difference,
    Product,
    LetStar,
    Cond,
    Not,
    All,
    Any,
    NonAscending,
    Descending,
    Same,
    Ascending,
    NonDescending,
)
import kernel
from kernel import (
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
)


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

        case Sum([*vals]):
            match [*vals]:
                case []:
                    return Int(0)
                case [Int(a), *rest]:
                    return Add(Int(a), recur(Sum([*rest])))

        case Difference([*vals]):
            match [*vals]:
                case []:
                    return Int(0)
                case [Int(a)]:
                    return Subtract(Int(0), Int(a))
                case [Int(a), Int(b)]:
                    return Subtract(Int(a), Int(b))
                case [Int(a), *rest]:
                    return Subtract(Int(a), recur(Difference([*rest])))

        case Product([*vals]):
            match [*vals]:
                case []:
                    return Int(1)
                case [Int(a), *rest]:
                    return Multiply(Int(a), recur(Product([*rest])))

        case LetStar([*lets], body):
            match [*lets]:
                case []:
                    return body
                case [[n, e]]:
                    return Let(n, e, body)
                case [[n, e], *rest]:
                    return Let(n, e, recur(LetStar([*rest], body)))

        case Not(a):
            return If(EqualTo(a, Bool(True)), Bool(False), Bool(True))

        case All([*op]):
            match [*op]:
                case []:
                    return Bool(True)
                # case [a]:
                #     return If(a, Bool(True), Bool(False))
                case [a, *rest]:
                    return If(a, recur(All([*rest])), Bool(False))

        case Any([*op]):
            match [*op]:
                case []:
                    return Bool(False)
                case [a, *rest]:
                    return If(a, Bool(True), recur(Any([*rest])))

        case Cond([*seq], default):
            match [*seq]:
                case []:
                    return default
                case [[a, b], *rest]:
                    return If(a, b, recur(Cond([*rest], default)))

        case NonDescending([*statements]):
            match [*statements]:
                case []:
                    return Bool(True)
                case [Int(a)]:
                    return Bool(True)
                case [Int(a), Int(b)]:
                    return GreaterThanOrEqualTo(Int(b), Int(a))
                case [Int(a), Int(b), *rest]:
                    return If(GreaterThanOrEqualTo(Int(b), Int(a)), recur(NonDescending([Int(b), *rest])), Bool(False))

        case Ascending([*statements]):
            match [*statements]:
                case []:
                    return Bool(True)
                case [Int(a)]:
                    return Bool(True)
                case [Int(a), Int(b)]:
                    return LessThan(Int(a), Int(b))
                case [Int(a), Int(b), *rest]:
                    return If(LessThan(Int(a), Int(b)), recur(Ascending([Int(b), *rest])), Bool(False))

        case Same([*statements]):
            match [*statements]:
                case []:
                    return Bool(True)
                case [Int(a)]:
                    return Bool(True)
                case [Int(a), Int(b)]:
                    return EqualTo(Int(a), Int(b))
                case [Int(a), Int(b), *rest]:
                    return If(EqualTo(Int(a), Int(b)), recur(Same([Int(b), *rest])), Bool(False))

        case Descending([*statements]):
            match [*statements]:
                case []:
                    return Bool(True)
                case [Int(a)]:
                    return Bool(True)
                case [Int(a), Int(b)]:
                    return LessThan(Int(b), Int(a))
                case [Int(a), Int(b), *rest]:
                    return If(LessThan(Int(b), Int(a)), recur(Descending([Int(b), *rest])), Bool(False))

        case NonAscending([*statements]):
            match [*statements]:
                case []:
                    return Bool(True)
                case [Int(a)]:
                    return Bool(True)
                case [Int(a), Int(b)]:
                    return GreaterThanOrEqualTo(Int(a), Int(b))
                case [Int(a), Int(b), *rest]:
                    return If(GreaterThanOrEqualTo(Int(a), Int(b)), recur(NonAscending([Int(b), *rest])), Bool(False))

        case Add(e1, e2):
            return Add(recur(e1), recur(e2))

        case Subtract(e1, e2):
            return Subtract(recur(e1), recur(e2))

        case Multiply(e1, e2):
            return Multiply(recur(e1), recur(e2))

        case Let(x, e1, e2):
            return Let(x, recur(e1), recur(e2))

        case Var():
            return expr

        case Bool():
            return expr

        case If(cond, con, alt):
            return If(cond, con, alt)

        case LessThan(a, b):
            return LessThan(a, b)

        case GreaterThanOrEqualTo(a, b):
            return GreaterThanOrEqualTo(a, b)

        case EqualTo(a, b):
            return EqualTo(a, b)

        case _:
            raise NotImplementedError()
