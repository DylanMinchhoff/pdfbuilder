from collections.abc import Callable
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
from uniqify import Environment, uniqify, uniqify_expression
from util import SequentialNameGenerator


@pytest.mark.parametrize(
    "program, fresh, expected",
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
    program: Program,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify(program, fresh) == expected


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
def test_uniqify_expression_int(
    expr: Int,
    env: Environment,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, env, fresh) == expected


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
def test_uniqify_expression_add(
    expr: Expression,
    env: Environment,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, env, fresh) == expected


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
def test_uniqify_expression_subtract(
    expr: Expression,
    env: Environment,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, env, fresh) == expected


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
def test_uniqify_expression_multiply(
    expr: Expression,
    env: Environment,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, env, fresh) == expected


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
def test_uniqify_expression_var(
    expr: Expression,
    env: Environment,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, env, fresh) == expected


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
def test_uniqify_expression_bool(
    expr: Expression,
    env: Environment,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, env, fresh) == expected


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
def test_uniqify_expression_if(
    expr: Expression,
    env: Environment,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, env, fresh) == expected


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
def test_uniqify_expression_less_than(
    expr: Expression,
    env: Environment,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, env, fresh) == expected


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
def test_uniqify_expression_equal_to(
    expr: Expression,
    env: Environment,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, env, fresh) == expected


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
def test_uniqify_expression_greater_than_or_equal_to(
    expr: Expression,
    env: Environment,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, env, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, fresh, expected",
    list[tuple[Expression, Environment, Callable[[str], str], Expression]](
        [
            (
                Unit(),
                {},
                SequentialNameGenerator(),
                Unit(),
            ),
        ]
    ),
)
def test_uniqify_expression_unit(
    expr: Int,
    env: Environment,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, env, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, fresh, expected",
    list[tuple[Expression, Environment, Callable[[str], str], Expression]](
        [
            (
                Tuple([Unit()]),
                {},
                SequentialNameGenerator(),
                Tuple([Unit()]),
            ),
        ]
    ),
)
def test_uniqify_expression_cell(
    expr: Int,
    env: Environment,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, env, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, fresh, expected",
    list[tuple[Expression, Environment, Callable[[str], str], Expression]](
        [
            (
                Get(Var("x"), Int(0)),
                {"x": "x"},
                SequentialNameGenerator(),
                Get(Var("x"), Int(0)),
            ),
        ]
    ),
)
def test_uniqify_expression_get(
    expr: Int,
    env: Environment,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, env, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, fresh, expected",
    list[tuple[Expression, Environment, Callable[[str], str], Expression]](
        [
            (
                Set(Var("x"), Int(0), Unit()),
                {"x": "x"},
                SequentialNameGenerator(),
                Set(Var("x"), Int(0), Unit()),
            ),
        ]
    ),
)
def test_uniqify_expression_set(
    expr: Int,
    env: Environment,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, env, fresh) == expected


@pytest.mark.xfail
@pytest.mark.parametrize(
    "expr, env, fresh, expected",
    list[tuple[Expression, Environment, Callable[[str], str], Expression]](
        [
            (
                Lambda([], Unit()),
                {},
                SequentialNameGenerator(),
                Lambda([], Unit()),
            ),
        ]
    ),
)
def test_uniqify_expression_lambda(
    expr: Int,
    env: Environment,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, env, fresh) == expected


@pytest.mark.xfail
@pytest.mark.parametrize(
    "expr, env, fresh, expected",
    list[tuple[Expression, Environment, Callable[[str], str], Expression]](
        [
            (
                Apply(Int(0), []),
                {},
                SequentialNameGenerator(),
                Apply(Int(0), []),
            ),
        ]
    ),
)
def test_uniqify_expression_apply(
    expr: Int,
    env: Environment,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, env, fresh) == expected
