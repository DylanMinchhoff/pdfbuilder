import pytest
from kernel import Expression, Int, Add, Subtract, Multiply, Let, Var
from parse_kernel import parse_expr


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "0",
                Int(0),
            ),
        ]
    ),
)
def test_parse_expr_int(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(+ 1 2)",
                Add(Int(1), Int(2)),
            ),
        ]
    ),
)
def test_parse_expr_add(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(- 2 1)",
                Subtract(Int(2), Int(1)),
            ),
        ]
    ),
)
def test_parse_expr_subtract(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(* 1 2)",
                Multiply(Int(1), Int(2)),
            ),
        ]
    ),
)
def test_parse_expr_multiply(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(let ([x 1]) x)",
                Let("x", Int(1), Var("x")),
            ),
        ]
    ),
)
def test_parse_expr_let(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "x",
                Var("x"),
            ),
        ]
    ),
)
def test_parse_expr_var(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected
