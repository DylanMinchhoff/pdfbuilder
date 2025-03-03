from functools import partial
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


def opt(
    program: Program,
) -> Program:
    return Program(
        parameters=program.parameters,
        body=opt_expression(program.body),
    )


def opt_expression(
    expr: Expression,
) -> Expression:
    recur = partial(opt_expression)

    # return as val, var for optimization
    match expr:
        case Int():
            return expr

        case Add(x, y):
            match recur(x), recur(y):
                case [Int(0), y]:
                    return y
                case [x, Int(0)]:
                    return x
                case [Int(i1), Int(i2)]:
                    return Int(i1 + i2)
                case [Int(i1), Add(Int(i2), y)]:
                    return Add(Int(i1 + i2), y)
                case [Add(Int(i1), x), Add(Int(i2), y)]:
                    return Add(Int(i1 + i2), Add(x, y))
                case [x, Int() as y]:
                    return Add(y, x)
                case [x, y]:  # pragma: no branch
                    return Add(x, y)

        case Subtract(x, y):
            match recur(x), recur(y):
                case [Int(i1), Int(i2)]:
                    return Int(i1 - i2)
                case [x, y]:  # pragma: no branch
                    return Subtract(x, y)

        case Multiply(x, y):
            match recur(x), recur(y):
                case [Int(0), y]:
                    return Int(0)
                case [x, Int(0)]:
                    return Int(0)
                case [Int(1), y]:
                    return y
                case [x, Int(1)]:
                    return x
                case [Int(i1), Int(i2)]:
                    return Int(i1 * i2)
                case [Int(i1), Multiply(Int(i2), y)]:
                    return Multiply(Int(i1 * i2), y)
                case [Multiply(Int(i1), x), Multiply(Int(i2), y)]:
                    return Multiply(Int(i1 * i2), Multiply(x, y))
                case [x, Int() as y]:
                    return Multiply(y, x)
                case [x, y]:  # pragma: no branch
                    return Multiply(x, y)

        case Var():
            return expr

        case Bool():
            return expr

        case If(condition, consequent, alternative):
            match recur(condition):
                case Bool(True):
                    return recur(consequent)
                case Bool(False):
                    return recur(alternative)
                case condition:  # pragma: no branch
                    return If(condition, recur(consequent), recur(alternative))

        case LessThan(x, y):
            match recur(x), recur(y):
                case [Int(i1), Int(i2)]:
                    return Bool(i1 < i2)
                case [x, y]:  # pragma: no branch
                    return LessThan(x, y)

        case EqualTo(x, y):
            match recur(x), recur(y):
                case [Int(i1), Int(i2)]:
                    return Bool(i1 == i2)
                case [Bool(b1), Bool(b2)]:
                    return Bool(b1 == b2)
                case [x, y]:  # pragma: no branch
                    return EqualTo(x, y)

        case GreaterThanOrEqualTo(x, y):
            match recur(x), recur(y):
                case [Int(i1), Int(i2)]:
                    return Bool(i1 >= i2)
                case [x, y]:  # pragma: no branch
                    return GreaterThanOrEqualTo(x, y)

        case Unit():
            return expr

        case Tuple(components):
            return Tuple([recur(e) for e in components])

        case Get(tuple, index):
            match recur(tuple), recur(index):
                case [Tuple(components), Int(i)] if i in range(len(components)):
                    return components[i]
                case [tuple, index]:  # pragma: no branch
                    return Get(tuple, index)

        case Set(tuple, index, value):
            return Set(recur(tuple), index, recur(value))

        case Lambda(parameters, body):
            return Lambda(parameters, recur(body))

        case Apply(callee, arguments):  # pragma no branch
            return Apply(recur(callee), [recur(e) for e in arguments])
