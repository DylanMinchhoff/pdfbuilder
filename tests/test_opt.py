import pytest
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
from opt import opt, opt_expression


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
    list[tuple[Expression, Expression]](
        [
            (
                Int(0),
                Int(0),
            ),
        ]
    ),
)
def test_opt_expression_int(
    expr: Expression,
    expected: Expression,
) -> None:
    assert opt_expression(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Expression, Expression]](
        [
            (
                Add(Int(0), Var("x")),
                Var("x"),
            ),
            (
                Add(Var("x"), Int(0)),
                Var("x"),
            ),
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
def test_opt_expression_add(
    expr: Expression,
    expected: Expression,
) -> None:
    assert opt_expression(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Expression, Expression]](
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
def test_opt_expression_subtract(
    expr: Expression,
    expected: Expression,
) -> None:
    assert opt_expression(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Expression, Expression]](
        [
            (
                Multiply(Int(0), Var("x")),
                Int(0),
            ),
            (
                Multiply(Var("x"), Int(0)),
                Int(0),
            ),
            (
                Multiply(Int(1), Var("x")),
                Var("x"),
            ),
            (
                Multiply(Var("x"), Int(1)),
                Var("x"),
            ),
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
                Multiply(Int(2), Var("x")),
                Multiply(Int(2), Var("x")),
            ),
            (
                Multiply(Var("x"), Int(2)),
                Multiply(Int(2), Var("x")),
            ),
            (
                Multiply(Var("x"), Var("y")),
                Multiply(Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_opt_expression_multiply(
    expr: Expression,
    expected: Expression,
) -> None:
    assert opt_expression(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Expression, Expression]](
        [
            (
                Var("x"),
                Var("x"),
            ),
        ]
    ),
)
def test_opt_expression_var(
    expr: Expression,
    expected: Expression,
) -> None:
    assert opt_expression(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Expression, Expression]](
        [
            (
                Bool(True),
                Bool(True),
            ),
            (
                Bool(False),
                Bool(False),
            ),
        ]
    ),
)
def test_opt_expression_bool(
    expr: Expression,
    expected: Expression,
) -> None:
    assert opt_expression(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Expression, Expression]](
        [
            (
                If(Bool(True), Int(0), Int(1)),
                Int(0),
            ),
            (
                If(Bool(False), Int(0), Int(1)),
                Int(1),
            ),
            (
                If(Var("x"), Int(0), Int(1)),
                If(Var("x"), Int(0), Int(1)),
            ),
        ]
    ),
)
def test_opt_expression_if(
    expr: Expression,
    expected: Expression,
) -> None:
    assert opt_expression(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Expression, Expression]](
        [
            (
                LessThan(Int(0), Int(1)),
                Bool(True),
            ),
            (
                LessThan(Int(0), Var("x")),
                LessThan(Int(0), Var("x")),
            ),
        ]
    ),
)
def test_opt_expression_less_than(
    expr: Expression,
    expected: Expression,
) -> None:
    assert opt_expression(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Expression, Expression]](
        [
            (
                EqualTo(Int(0), Int(1)),
                Bool(False),
            ),
            (
                EqualTo(Bool(True), Bool(True)),
                Bool(True),
            ),
            (
                EqualTo(Int(1), Var("x")),
                EqualTo(Int(1), Var("x")),
            ),
        ]
    ),
)
def test_opt_expression_equal_to(
    expr: Expression,
    expected: Expression,
) -> None:
    assert opt_expression(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Expression, Expression]](
        [
            (
                GreaterThanOrEqualTo(Int(0), Int(1)),
                Bool(False),
            ),
            (
                GreaterThanOrEqualTo(Int(1), Var("x")),
                GreaterThanOrEqualTo(Int(1), Var("x")),
            ),
        ]
    ),
)
def test_opt_expression_greeater_than_or_equal_to(
    expr: Expression,
    expected: Expression,
) -> None:
    assert opt_expression(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Expression, Expression]](
        [
            (
                Unit(),
                Unit(),
            ),
        ]
    ),
)
def test_opt_expression_unit(
    expr: Expression,
    expected: Expression,
) -> None:
    assert opt_expression(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Expression, Expression]](
        [
            (
                Tuple([]),
                Tuple([]),
            ),
        ]
    ),
)
def test_opt_expression_cell(
    expr: Expression,
    expected: Expression,
) -> None:
    assert opt_expression(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Expression, Expression]](
        [
            (
                Get(Tuple[Expression]([Unit()]), Int(0)),
                Unit(),
            ),
            (
                Get(Var("x"), Int(0)),
                Get(Var("x"), Int(0)),
            ),
        ]
    ),
)
def test_opt_expression_get(
    expr: Expression,
    expected: Expression,
) -> None:
    assert opt_expression(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Expression, Expression]](
        [
            (
                Set(Var("x"), Int(0), Var("y")),
                Set(Var("x"), Int(0), Var("y")),
            ),
        ]
    ),
)
def test_opt_expression_set(
    expr: Expression,
    expected: Expression,
) -> None:
    assert opt_expression(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Expression, Expression]](
        [
            (
                Lambda([], Var("x")),
                Lambda([], Var("x")),
            ),
        ]
    ),
)
def test_opt_expression_lambda(
    expr: Expression,
    expected: Expression,
) -> None:
    assert opt_expression(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Expression, Expression]](
        [
            (
                Apply(Var("x"), []),
                Apply(Var("x"), []),
            ),
        ]
    ),
)
def test_opt_expression_apply(
    expr: Expression,
    expected: Expression,
) -> None:
    assert opt_expression(expr) == expected
