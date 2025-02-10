from collections.abc import Mapping
from functools import partial
from kernel import Expression, Int, Add, Subtract, Multiply, Let, Var

type Value = int
type Environment = Mapping[str, Value]


def eval_expr(
    expr: Expression,
    env: Environment,
) -> Value:
    recur = partial(eval_expr, env=env)
    match expr:
        case Int(i):
            return i

        case Add(e1, e2):
            return recur(e1) + recur(e2)

        case Subtract(e1, e2):
            return recur(e1) - recur(e2)

        case Multiply(e1, e2):
            return recur(e1) * recur(e2)

        case Let(x, e1, e2):
            # create a new varible x and assign it to e1
            # then copy envirnment vars and new var in scope and eval
            return recur(e2, env={**env, x: recur(e1)})

        case Var(x):  # pragma: no branch
            if x in env:  # varible has been declared and using
                return env[x]
            else:
                return Int(0)
