from functools import partial
from kernel import Expression, Int, Add, Subtract, Multiply, Let, Var
from eval import eval_expr


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
                case [Int(i1), Int(i2)]:
                    return Int(i1 + i2)
                case [Int(a), Add(Int(b), ex)]:
                    return Add(Int(a + b), ex)
                case [Add(Int(a), e1), Add(Int(b), e2)]:
                    return Add(Int(a + b), Add(e1, e2))
                case [e1, Int(a)]:
                    return Add(Int(a), e1)
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
                case [Int(i1), Int(i2)]:
                    return Int(i1 * i2)
                case [Int(a), Multiply(Int(b), ex)]:
                    return Multiply(Int(a * b), ex)
                case [Multiply(Int(a), e1), Multiply(Int(b), e2)]:
                    return Multiply(Int(a * b), Multiply(e1, e2))
                case [e1, Int(a)]:
                    return Multiply(Int(a), e1)
                case [e1, e2]:  # pragma: no branch
                    # bring var to right and value to left [val, var]
                    return Multiply(e1, e2)

        case Let(x, e1, e2):
            # if var is const replace with const
            if e2 == Var(x):
                return e1
            return Let(x, e1, e2)

        case Var(x):  # pragma: no branch
            return Var(x)
