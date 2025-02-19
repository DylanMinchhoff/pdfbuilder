import pytest
import sugar
from sugar import (
    Sum,
    Difference,
    Product,
    LetStar,
    Not,
    All,
    Any,
    Cond,
    Ascending,
    NonDescending,
    Same,
    NonAscending,
    Descending,
)
import kernel
from kernel import (
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
from desugar import desugar, desugar_expr


@pytest.mark.parametrize(
    "program, expected",
    list[tuple[sugar.Program, kernel.Program]](
        [
            (
                sugar.Program([], Int(0)),
                kernel.Program([], Int(0)),
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
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                Int(0),
                Int(0),
            ),
        ]
    ),
)
def test_desugar_expr_int(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                Add(Int(0), Int(0)),
                Add(Int(0), Int(0)),
            ),
        ]
    ),
)
def test_desugar_expr_add(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                Subtract(Int(0), Int(0)),
                Subtract(Int(0), Int(0)),
            ),
        ]
    ),
)
def test_desugar_expr_subtract(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                Multiply(Int(0), Int(0)),
                Multiply(Int(0), Int(0)),
            ),
        ]
    ),
)
def test_desugar_expr_multiply(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                Let("x", Int(0), Var("x")),
                Let("x", Int(0), Var("x")),
            ),
        ]
    ),
)
def test_desugar_expr_let(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                Var("x"),
                Var("x"),
            ),
        ]
    ),
)
def test_desugar_expr_var(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                Bool(True),
                Bool(True),
            ),
        ]
    ),
)
def test_desugar_expr_bool(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                If(Bool(True), Var("x"), Var("y")),
                If(Bool(True), Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_desugar_expr_if(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                LessThan(Int(1), Int(2)),
                LessThan(Int(1), Int(2)),
            ),
        ]
    ),
)
def test_desugar_expr_less_than(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                EqualTo(Int(1), Int(2)),
                EqualTo(Int(1), Int(2)),
            ),
        ]
    ),
)
def test_desugar_expr_equal_to(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                GreaterThanOrEqualTo(Int(1), Int(2)),
                GreaterThanOrEqualTo(Int(1), Int(2)),
            ),
        ]
    ),
)
def test_desugar_expr_greater_than_or_equal_to(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                Sum([]),
                Int(0),
            ),
            (
                Sum([Int(1)]),
                Add(Int(1), Int(0)),
            ),
            (
                Sum([Int(1), Int(1)]),
                Add(Int(1), Add(Int(1), Int(0))),
            ),
        ]
    ),
)
def test_desugar_expr_sum(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                Difference([Int(1)]),
                Subtract(Int(0), Int(1)),
            ),
            (
                Difference([Int(2), Int(1)]),
                Subtract(Int(2), Int(1)),
            ),
            (
                Difference([Int(3), Int(2), Int(1)]),
                Subtract(Int(3), Subtract(Int(2), Int(1))),
            ),
        ]
    ),
)
def test_desugar_expr_difference(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                Product([]),
                Int(1),
            ),
            (
                Product([Int(1)]),
                Multiply(Int(1), Int(1)),
            ),
            (
                Product([Int(2), Int(2)]),
                Multiply(Int(2), Multiply(Int(2), Int(1))),
            ),
        ]
    ),
)
def test_desugar_expr_product(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                LetStar([], Var("x")),
                Var("x"),
            ),
            (
                LetStar([("x", Int(0))], Var("x")),
                Let("x", Int(0), Var("x")),
            ),
            (
                LetStar([("x", Int(0)), ("y", Int(1))], Var("x")),
                Let(
                    "x",
                    Int(0),
                    Let("y", Int(1), Var("x")),
                ),
            ),
        ]
    ),
)
def test_desugar_expr_letstar(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                Not(Var("x")),
                If(EqualTo(Var("x"), Bool(True)), Bool(False), Bool(True)),
            ),
        ]
    ),
)
def test_desugar_expr_not(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                All([]),
                Bool(True),
            ),
            (
                All([Bool(True)]),
                If(Bool(True), Bool(True), Bool(False)),
            ),
            (
                All([Bool(True), Bool(False)]),
                If(Bool(True), If(Bool(False), Bool(True), Bool(False)), Bool(False)),
            ),
        ]
    ),
)
def test_desugar_expr_all(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    print(desugar_expr(expr))
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                Any([]),
                Bool(False),
            ),
            (
                Any([Bool(True)]),
                If(Bool(True), Bool(True), Bool(False)),
            ),
            (
                Any([Bool(True), Bool(False)]),
                If(Bool(True), Bool(True), If(Bool(False), Bool(True), Bool(False))),
            ),
        ]
    ),
)
def test_desugar_expr_any(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                Cond([], Int(0)),
                Int(0),
            ),
            (
                Cond([(Bool(True), Int(1))], Int(0)),
                If(Bool(True), Int(1), Int(0)),
            ),
        ]
    ),
)
def test_desugar_expr_cond(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                NonDescending([]),
                Bool(True),
            ),
            (
                NonDescending([Int(0)]),
                Bool(True),
            ),
            (
                NonDescending([Int(1), Int(2)]),
                GreaterThanOrEqualTo(Int(2), Int(1)),
            ),
            (
                NonDescending([Int(1), Int(2), Int(3)]),
                If(GreaterThanOrEqualTo(Int(2), Int(1)), GreaterThanOrEqualTo(Int(3), Int(2)), Bool(False)),
            ),
        ]
    ),
)
def test_desugar_expr_non_descending(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                Ascending([]),
                Bool(True),
            ),
            (
                Ascending([Int(0)]),
                Bool(True),
            ),
            (
                Ascending([Int(1), Int(2)]),
                LessThan(Int(1), Int(2)),
            ),
            (
                Ascending([Int(1), Int(2), Int(3)]),
                If(LessThan(Int(1), Int(2)), LessThan(Int(2), Int(3)), Bool(False)),
            ),
        ]
    ),
)
def test_desugar_expr_ascending(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                Same([]),
                Bool(True),
            ),
            (
                Same([Int(0)]),
                Bool(True),
            ),
            (
                Same([Int(1), Int(2)]),
                EqualTo(Int(1), Int(2)),
            ),
            (
                Same([Int(1), Int(2), Int(3)]),
                If(EqualTo(Int(1), Int(2)), EqualTo(Int(2), Int(3)), Bool(False)),
            ),
        ]
    ),
)
def test_desugar_expr_same(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                Descending([]),
                Bool(True),
            ),
            (
                Descending([Int(0)]),
                Bool(True),
            ),
            (
                Descending([Int(1), Int(2)]),
                LessThan(Int(2), Int(1)),
            ),
            (
                Descending([Int(1), Int(2), Int(3)]),
                If(LessThan(Int(2), Int(1)), LessThan(Int(3), Int(2)), Bool(False)),
            ),
        ]
    ),
)
def test_desugar_expr_descending(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                NonAscending([]),
                Bool(True),
            ),
            (
                NonAscending([Int(0)]),
                Bool(True),
            ),
            (
                NonAscending([Int(1), Int(2)]),
                GreaterThanOrEqualTo(Int(1), Int(2)),
            ),
            (
                NonAscending([Int(1), Int(2), Int(3)]),
                If(GreaterThanOrEqualTo(Int(1), Int(2)), GreaterThanOrEqualTo(Int(2), Int(3)), Bool(False)),
            ),
        ]
    ),
)
def test_desugar_expr_non_ascending(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected
