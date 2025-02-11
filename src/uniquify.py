# from collections.abc import Sequence, Mapping
# from functools import partial
# from kernel import Program, Expression, Int, Add, Subtract, Multiply, Let, Var

# type Value = int
# type Environment = Mapping[str, Value]


# def eval(
#     program: Program,
#     arguments: Sequence[Value],
# ) -> Value:
#     local = {x: fresh(x) for x in program.parameters}
#     return Program(
#         program=program.parameters,
#         body=uniquify_expr(
#             program.body, local, fresh
#         )
#     )


# def uniquify_expr(
#     expr: Expression,
#     env: Environment,
#     fresh: Callable[[str], str]
# ) -> Value:
#     recur = partial(uniquify_expr, env=env)
#     match expr:
#         case Int(i):
#             return i

#         case Add(e1, e2):
#             return recur(e1) + recur(e2)

#         case Subtract(e1, e2):
#             return recur(e1) - recur(e2)

#         case Multiply(e1, e2):
#             return recur(e1) * recur(e2)

#         case Let(x, e1, e2):
#             y = fresh(x)
#             return Let(y, recur(e1), recur(e2, env={**env, x: y}))

#         case Var(x):  # pragma: no branch
#             # varible has been declared and using
#             return Var(env[x])
