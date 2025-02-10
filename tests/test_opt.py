import pytest
from kernel import Program, Expression, Int, Add, Subtract, Multiply, Let, Var
from opt import opt, opt_expr


@pytest.mark.parametrize(
    "program, expected",
    list[tuple[Program, Program]](
        [
            (
                Program([], Int(0)),
                Program([], Int(0)),
            ),
        ]
    ),
)
def test_opt(
    program: Program,
    expected: Program,
) -> None:
    assert opt(program) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Int, Expression]](
        [
            (
                Int(0),
                Int(0),
            ),
        ]
    ),
)
def test_opt_expr_int(
    expr: Int,
    expected: Expression,
) -> None:
    assert opt_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Add, Expression]](
        [
            (
                Add(Int(1), Int(1)),
                Int(2),
            ),
            (
                Add(Int(1), Add(Int(1), Int(1))),
                Int(3),
            ),
            (
                Add(Int(1), Add(Var("x"), Int(1))),
                Add(Int(2), Var("x")),
            ),
            (
                Add(Add(Int(1), Var("x")), Add(Int(1), Var("y"))),
                Add(Int(2), Add(Var("x"), Var("y"))),
            ),
            (
                Add(Int(1), Add(Int(1), Var("x"))),
                Add(Int(2), Var("x")),
            ),
            (
                Add(Int(1), Var("x")),
                Add(Int(1), Var("x")),
            ),
            (
                Add(Var("x"), Int(1)),
                Add(Int(1), Var("x")),
            ),
            (
                Add(Var("x"), Var("y")),
                Add(Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_opt_expr_add(
    expr: Add,
    expected: Expression,
) -> None:
    assert opt_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Subtract, Expression]](
        [
            (
                Subtract(Int(2), Int(1)),
                Int(1),
            ),
            (
                Subtract(Var("x"), Var("y")),
                Subtract(Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_opt_expr_subtract(
    expr: Add,
    expected: Expression,
) -> None:
    assert opt_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Multiply, Expression]](
        [
            (
                Multiply(Int(1), Int(2)),
                Int(2),
            ),
            (
                Multiply(Int(1), Multiply(Int(2), Int(3))),
                Int(6),
            ),
            (
                Multiply(Int(2), Multiply(Var("x"), Int(3))),
                Multiply(Int(6), Var("x")),
            ),
            (
                Multiply(Multiply(Int(2), Var("x")), Multiply(Int(3), Var("y"))),
                Multiply(Int(6), Multiply(Var("x"), Var("y"))),
            ),
            (
                Multiply(Int(2), Multiply(Int(3), Var("x"))),
                Multiply(Int(6), Var("x")),
            ),
            (
                Multiply(Int(1), Var("x")),
                Multiply(Int(1), Var("x")),
            ),
            (
                Multiply(Var("x"), Int(1)),
                Multiply(Int(1), Var("x")),
            ),
            (
                Multiply(Var("x"), Var("y")),
                Multiply(Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_opt_expr_multiply(
    expr: Multiply,
    expected: Expression,
) -> None:
    assert opt_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Let, Expression]](
        [
            (
                Let("x", Int(1), Var("x")),
                Int(1),
            ),
            (
                Let("x", Int(1), Var("y")),
                Let("x", Int(1), Var("y")),
            ),
        ]
    ),
)
def test_opt_expr_let(
    expr: Let,
    expected: Expression,
) -> None:
    assert opt_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Var, Expression]](
        [
            (
                Var("x"),
                Var("x"),
            ),
        ]
    ),
)
def test_opt_expr_var(
    expr: Var,
    expected: Expression,
) -> None:
    assert opt_expr(expr) == expected
