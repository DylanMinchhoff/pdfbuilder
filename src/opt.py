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
)


def opt(
    program: Program,
) -> Program:
    return Program(
        parameters=program.parameters,
        body=opt_expr(program.body),
    )


def opt_expr(
    expr: Expression,
) -> Expression:
    recur = partial(opt_expr)

    # return as val, var for optimization
    match expr:
        case Int():
            return expr

        case Add(e1, e2):
            match recur(e1), recur(e2):
                case [Int(0), e2]:
                    return e2
                case [e1, Int(0)]:
                    return e1
                case [Int(i1), Int(i2)]:
                    return Int(i1 + i2)
                case [Int(i1), Add(Int(i2), e2)]:
                    return Add(Int(i1 + i2), e2)
                case [Add(Int(i1), e1), Add(Int(i2), e2)]:
                    return Add(Int(i1 + i2), Add(e1, e2))
                case [e1, Int() as e2]:
                    return Add(e2, e1)
                case [e1, e2]:  # pragma: no branch
                    return Add(e1, e2)

        case Subtract(e1, e2):
            match recur(e1), recur(e2):
                case [Int(i1), Int(i2)]:
                    return Int(i1 - i2)
                case [e1, e2]:  # pragma: no branch
                    return Subtract(e1, e2)

        case Multiply(e1, e2):
            match recur(e1), recur(e2):
                case [Int(0), e2]:
                    return Int(0)
                case [e1, Int(0)]:
                    return Int(0)
                case [Int(1), e2]:
                    return e2
                case [e1, Int(1)]:
                    return e1
                case [Int(i1), Int(i2)]:
                    return Int(i1 * i2)
                case [Int(i1), Multiply(Int(i2), e2)]:
                    return Multiply(Int(i1 * i2), e2)
                case [Multiply(Int(i1), e1), Multiply(Int(i2), e2)]:
                    return Multiply(Int(i1 * i2), Multiply(e1, e2))
                case [e1, Int() as e2]:
                    return Multiply(e2, e1)
                case [e1, e2]:  # pragma: no branch
                    # bring var to right and value to left [val, var]
                    return Multiply(e1, e2)

        case Let(x, e1, e2):
            match recur(e2):
                case Var(y) if x == y:
                    return recur(e1)
                case e2:  # pragma: no branch
                    return Let(x, recur(e1), e2)

        case Var():
            return expr

        case _:
            raise NotImplementedError()
