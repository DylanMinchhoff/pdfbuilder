import pytest
from kernel import (
    Program,
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
from uniqify import Environment, uniqify, uniqify_expr
from util import SequentialNameGenerator


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Program, Program]](
        [
            (
                Program([], Int(0)),
                Program([], Int(0)),
            ),
            (
                Program(["x"], Var("x")),
                Program(["_x0"], Var("_x0")),
            ),
        ]
    ),
)
def test_uniqify(
    expr: Program,
    expected: Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert uniqify(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Expression, Environment, Expression]](
        [
            (
                Int(0),
                {},
                Int(0),
            ),
        ]
    ),
)
def test_uniqify_expr_int(
    expr: Int,
    env: Environment,
    expected: Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert uniqify_expr(expr, env, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Expression, Environment, Expression]](
        [
            (
                Add(Int(1), Int(1)),
                {},
                Add(Int(1), Int(1)),
            ),
        ]
    ),
)
def test_uniqify_expr_add(
    expr: Expression,
    env: Environment,
    expected: Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert uniqify_expr(expr, env, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Expression, Environment, Expression]](
        [
            (
                Subtract(Int(1), Int(1)),
                {},
                Subtract(Int(1), Int(1)),
            ),
        ]
    ),
)
def test_uniqify_expr_subtract(
    expr: Expression,
    env: Environment,
    expected: Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert uniqify_expr(expr, env, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Expression, Environment, Expression]](
        [
            (
                Multiply(Int(1), Int(1)),
                {},
                Multiply(Int(1), Int(1)),
            ),
        ]
    ),
)
def test_uniqify_expr_multiply(
    expr: Expression,
    env: Environment,
    expected: Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert uniqify_expr(expr, env, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Expression, Environment, Expression]](
        [
            (
                Let("x", Int(1), Var("x")),
                {},
                Let("_x0", Int(1), Var("_x0")),
            ),
            (
                Let("x", Int(1), Let("x", Int(2), Var("x"))),
                {},
                Let("_x0", Int(1), Let("_x1", Int(2), Var("_x1"))),
            ),
        ]
    ),
)
def test_uniqify_expr_let(
    expr: Expression,
    env: Environment,
    expected: Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert uniqify_expr(expr, env, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Expression, Environment, Expression]](
        [
            (
                Var("x"),
                {"x": "y"},
                Var("y"),
            ),
        ]
    ),
)
def test_uniqify_expr_var(
    expr: Expression,
    env: Environment,
    expected: Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert uniqify_expr(expr, env, fresh) == expected


@pytest.mark.xfail
@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Expression, Environment, Expression]](
        [
            (
                Bool(True),
                {},
                Bool(True),
            ),
        ]
    ),
)
def test_uniqify_expr_bool(
    expr: Expression,
    env: Environment,
    expected: Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert uniqify_expr(expr, env, fresh) == expected


@pytest.mark.xfail
@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Expression, Environment, Expression]](
        [
            (
                If(Bool(True), Int(2), Int(2)),
                {},
                If(Bool(True), Int(2), Int(2)),
            ),
        ]
    ),
)
def test_uniqify_expr_if(
    expr: Expression,
    env: Environment,
    expected: Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert uniqify_expr(expr, env, fresh) == expected


@pytest.mark.xfail
@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Expression, Environment, Expression]](
        [
            (
                LessThan(Int(1), Int(1)),
                {},
                LessThan(Int(1), Int(1)),
            ),
        ]
    ),
)
def test_uniqify_expr_less_than(
    expr: Expression,
    env: Environment,
    expected: Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert uniqify_expr(expr, env, fresh) == expected


@pytest.mark.xfail
@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Expression, Environment, Expression]](
        [
            (
                EqualTo(Int(1), Int(1)),
                {},
                EqualTo(Int(1), Int(1)),
            ),
        ]
    ),
)
def test_uniqify_expr_equal_to(
    expr: Expression,
    env: Environment,
    expected: Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert uniqify_expr(expr, env, fresh) == expected


@pytest.mark.xfail
@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Expression, Environment, Expression]](
        [
            (
                GreaterThanOrEqualTo(Int(1), Int(1)),
                {},
                GreaterThanOrEqualTo(Int(1), Int(1)),
            ),
        ]
    ),
)
def test_uniqify_expr_greater_than_or_equal_to(
    expr: Expression,
    env: Environment,
    expected: Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert uniqify_expr(expr, env, fresh) == expected
