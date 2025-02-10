import pytest
import sugar
import kernel
from desugar import desugar, desugar_expr


@pytest.mark.parametrize(
    "program, expected",
    list[tuple[sugar.Program, kernel.Program]](
        [
            (
                sugar.Program([], sugar.Int(0)),
                kernel.Program([], kernel.Int(0)),
            ),
        ]
    ),
)
def test_desugar(
    program: sugar.Program,
    expected: kernel.Expression,
) -> None:
    assert desugar(program) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Int, kernel.Expression]](
        [
            (
                sugar.Int(0),
                kernel.Int(0),
            ),
        ]
    ),
)
def test_desugar_expr_int(
    expr: sugar.Int,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Add, kernel.Expression]](
        [
            (
                sugar.Add([]),
                kernel.Int(0),
            ),
            (
                sugar.Add([sugar.Int(1)]),
                kernel.Add(kernel.Int(1), kernel.Int(0)),
            ),
            (
                sugar.Add([sugar.Int(1), sugar.Int(1)]),
                kernel.Add(kernel.Int(1), kernel.Add(kernel.Int(1), kernel.Int(0))),
            ),
        ]
    ),
)
def test_desugar_expr_add(
    expr: sugar.Add,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Subtract, kernel.Expression]](
        [
            (
                sugar.Subtract([sugar.Int(1)]),
                kernel.Subtract(kernel.Int(0), kernel.Int(1)),
            ),
            (
                sugar.Subtract([sugar.Int(2), sugar.Int(1)]),
                kernel.Subtract(kernel.Int(2), kernel.Int(1)),
            ),
            (
                sugar.Subtract([sugar.Int(3), sugar.Int(2), sugar.Int(1)]),
                kernel.Subtract(kernel.Int(3), kernel.Subtract(kernel.Int(2), kernel.Int(1))),
            ),
        ]
    ),
)
def test_desugar_expr_subtract(
    expr: sugar.Subtract,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Multiply, kernel.Expression]](
        [
            (
                sugar.Multiply([]),
                kernel.Int(1),
            ),
            (
                sugar.Multiply([sugar.Int(1)]),
                kernel.Multiply(kernel.Int(1), kernel.Int(1)),
            ),
            (
                sugar.Multiply([sugar.Int(2), sugar.Int(2)]),
                kernel.Multiply(kernel.Int(2), kernel.Multiply(kernel.Int(2), kernel.Int(1))),
            ),
        ]
    ),
)
def test_desugar_expr_multiply(
    expr: sugar.Multiply,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Let, kernel.Expression]](
        [
            (
                sugar.Let("x", sugar.Int(0), sugar.Var("x")),
                kernel.Let("x", kernel.Int(0), kernel.Var("x")),
            ),
        ]
    ),
)
def test_desugar_expr_let(
    expr: sugar.Let,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Var, kernel.Expression]](
        [
            (
                sugar.Var("x"),
                kernel.Var("x"),
            ),
        ]
    ),
)
def test_desugar_expr_var(
    expr: sugar.Var,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected
