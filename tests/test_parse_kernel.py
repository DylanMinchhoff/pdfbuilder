import pytest
from kernel import (
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
from parse_kernel import parse_expr


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Int]](
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
    expected: Int,
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


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "#t",
                Bool(True),
            ),
            (
                "#f",
                Bool(False),
            ),
        ]
    ),
)
def test_parse_expr_bool(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(if x 1 0)",
                If(Var("x"), Int(1), Int(0)),
            ),
        ]
    ),
)
def test_parse_expr_if(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(< 1 0)",
                LessThan(Int(1), Int(0)),
            ),
        ]
    ),
)
def test_parse_expr_less_than(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(== 1 0)",
                EqualTo(Int(1), Int(0)),
            ),
        ]
    ),
)
def test_parse_expr_equal_to(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(>= 1 0)",
                GreaterThanOrEqualTo(Int(1), Int(0)),
            ),
        ]
    ),
)
def test_parse_expr_greater_than_or_equal_to(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected
