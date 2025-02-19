from collections.abc import Callable
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
    "expr, fresh, expected",
    list[tuple[Program, Callable[[str], str], Program]](
        [
            (
                Program([], Int(0)),
                SequentialNameGenerator(),
                Program([], Int(0)),
            ),
            (
                Program(["x"], Var("x")),
                SequentialNameGenerator(),
                Program(["_x0"], Var("_x0")),
            ),
        ]
    ),
)
def test_uniqify(
    expr: Program,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, fresh, expected",
    list[tuple[Expression, Environment, Callable[[str], str], Expression]](
        [
            (
                Int(0),
                {},
                SequentialNameGenerator(),
                Int(0),
            ),
        ]
    ),
)
def test_uniqify_expr_int(
    expr: Int,
    env: Environment,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expr(expr, env, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, fresh, expected",
    list[tuple[Expression, Environment, Callable[[str], str], Expression]](
        [
            (
                Add(Int(1), Int(1)),
                {},
                SequentialNameGenerator(),
                Add(Int(1), Int(1)),
            ),
        ]
    ),
)
def test_uniqify_expr_add(
    expr: Expression,
    env: Environment,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expr(expr, env, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, fresh, expected",
    list[tuple[Expression, Environment, Callable[[str], str], Expression]](
        [
            (
                Subtract(Int(1), Int(1)),
                {},
                SequentialNameGenerator(),
                Subtract(Int(1), Int(1)),
            ),
        ]
    ),
)
def test_uniqify_expr_subtract(
    expr: Expression,
    env: Environment,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expr(expr, env, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, fresh, expected",
    list[tuple[Expression, Environment, Callable[[str], str], Expression]](
        [
            (
                Multiply(Int(1), Int(1)),
                {},
                SequentialNameGenerator(),
                Multiply(Int(1), Int(1)),
            ),
        ]
    ),
)
def test_uniqify_expr_multiply(
    expr: Expression,
    env: Environment,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expr(expr, env, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, fresh, expected",
    list[tuple[Expression, Environment, Callable[[str], str], Expression]](
        [
            (
                Let("x", Int(1), Var("x")),
                {},
                SequentialNameGenerator(),
                Let("_x0", Int(1), Var("_x0")),
            ),
            (
                Let("x", Int(1), Let("x", Int(2), Var("x"))),
                {},
                SequentialNameGenerator(),
                Let("_x0", Int(1), Let("_x1", Int(2), Var("_x1"))),
            ),
        ]
    ),
)
def test_uniqify_expr_let(
    expr: Expression,
    env: Environment,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expr(expr, env, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, fresh, expected",
    list[tuple[Expression, Environment, Callable[[str], str], Expression]](
        [
            (
                Var("x"),
                {"x": "y"},
                SequentialNameGenerator(),
                Var("y"),
            ),
        ]
    ),
)
def test_uniqify_expr_var(
    expr: Expression,
    env: Environment,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expr(expr, env, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, fresh, expected",
    list[tuple[Expression, Environment, Callable[[str], str], Expression]](
        [
            (
                Bool(True),
                {},
                SequentialNameGenerator(),
                Bool(True),
            ),
        ]
    ),
)
def test_uniqify_expr_bool(
    expr: Expression,
    env: Environment,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expr(expr, env, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, fresh, expected",
    list[tuple[Expression, Environment, Callable[[str], str], Expression]](
        [
            (
                If(Bool(True), Int(2), Int(2)),
                {},
                SequentialNameGenerator(),
                If(Bool(True), Int(2), Int(2)),
            ),
        ]
    ),
)
def test_uniqify_expr_if(
    expr: Expression,
    env: Environment,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expr(expr, env, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, fresh, expected",
    list[tuple[Expression, Environment, Callable[[str], str], Expression]](
        [
            (
                LessThan(Int(1), Int(1)),
                {},
                SequentialNameGenerator(),
                LessThan(Int(1), Int(1)),
            ),
        ]
    ),
)
def test_uniqify_expr_less_than(
    expr: Expression,
    env: Environment,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expr(expr, env, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, fresh, expected",
    list[tuple[Expression, Environment, Callable[[str], str], Expression]](
        [
            (
                EqualTo(Int(1), Int(1)),
                {},
                SequentialNameGenerator(),
                EqualTo(Int(1), Int(1)),
            ),
        ]
    ),
)
def test_uniqify_expr_equal_to(
    expr: Expression,
    env: Environment,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expr(expr, env, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, fresh, expected",
    list[tuple[Expression, Environment, Callable[[str], str], Expression]](
        [
            (
                GreaterThanOrEqualTo(Int(1), Int(1)),
                {},
                SequentialNameGenerator(),
                GreaterThanOrEqualTo(Int(1), Int(1)),
            ),
        ]
    ),
)
def test_uniqify_expr_greater_than_or_equal_to(
    expr: Expression,
    env: Environment,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expr(expr, env, fresh) == expected
