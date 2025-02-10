from collections.abc import Sequence
import pytest
from kernel import Program, Expression, Int, Add, Subtract, Multiply, Let, Var
from eval import Value, Environment, eval, eval_expr


@pytest.mark.parametrize(
    "program, arguments, expected",
    list[tuple[Program, Sequence[Value], Value]](
        [
            # Int
            (
                Program([], Int(0)),
                [],
                0,
            ),
            (
                Program(["x"], Var("x")),
                [0],
                0,
            ),
        ]
    ),
)
def test_eval(
    program: Program,
    arguments: Sequence[Value],
    expected: Value,
) -> None:
    assert eval(program, arguments) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Expression, Environment, Value]](
        [
            # Int
            (
                Int(0),
                {},
                0,
            ),
            # Add
            (
                Add(Int(1), Int(1)),
                {},
                2,
            ),
            # Subtract
            (
                Subtract(Int(1), Int(1)),
                {},
                0,
            ),
            # Multiply
            (
                Multiply(Int(1), Int(2)),
                {},
                2,
            ),
            # Let
            (
                Let("x", Int(1), Var("x")),
                {},
                1,
            ),
            # Var
            (
                Var("x"),
                {"x": 0},
                0,
            ),
        ]
    ),
)
def test_eval_expr(
    expr: Expression,
    env: Environment,
    expected: Value,
) -> None:
    assert eval_expr(expr, env) == expected
