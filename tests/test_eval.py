from collections.abc import Sequence
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
from eval import Closure, Location, Store, Value, Environment, eval, eval_expression


@pytest.mark.parametrize(
    "program, arguments, expected",
    list[tuple[Program, Sequence[Value], Value]](
        [
            (
                Program([], Int(0)),
                [],
                Int(0),
            ),
            (
                Program(["x"], Var("x")),
                [Int(0)],
                Int(0),
            ),
        ]
    ),
)
def test_eval(
    program: Program,
    arguments: Sequence[Value],
    expected: int,
) -> None:
    assert eval(program, arguments) == expected


@pytest.mark.parametrize(
    "expr, env, store, expected",
    list[tuple[Int, Environment, Store[Value], Value]](
        [
            (
                Int(0),
                {},
                Store(),
                Int(0),
            ),
        ]
    ),
)
def test_eval_expression_int(
    expr: Int,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store) == expected


@pytest.mark.parametrize(
    "expr, env, store, expected",
    list[tuple[Expression, Environment, Store[Value], Value]](
        [
            (
                Add(Int(1), Int(1)),
                {},
                Store(),
                Int(2),
            ),
        ]
    ),
)
def test_eval_expression_add(
    expr: Expression,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store) == expected


@pytest.mark.parametrize(
    "expr, env, store, expected",
    list[tuple[Expression, Environment, Store[Value], Value]](
        [
            (
                Subtract(Int(1), Int(1)),
                {},
                Store(),
                Int(0),
            ),
        ]
    ),
)
def test_eval_expression_subtract(
    expr: Expression,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store) == expected


@pytest.mark.parametrize(
    "expr, env, store, expected",
    list[tuple[Expression, Environment, Store[Value], Value]](
        [
            (
                Multiply(Int(1), Int(2)),
                {},
                Store(),
                Int(2),
            ),
        ]
    ),
)
def test_eval_multiply(
    expr: Expression,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store) == expected


@pytest.mark.parametrize(
    "expr, env, store, expected",
    list[tuple[Var, Environment, Store[Value], Value]](
        [
            (
                Var("x"),
                {"x": Int(0)},
                Store(),
                Int(0),
            ),
        ]
    ),
)
def test_eval_expression_var(
    expr: Var,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store) == expected


@pytest.mark.parametrize(
    "expr, env, store, expected",
    list[tuple[Bool, Environment, Store[Value], Value]](
        [
            (
                Bool(True),
                {},
                Store(),
                Bool(True),
            ),
            (
                Bool(False),
                {},
                Store(),
                Bool(False),
            ),
        ]
    ),
)
def test_eval_expression_bool(
    expr: Bool,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store) == expected


@pytest.mark.parametrize(
    "expr, env, store, expected",
    list[tuple[Expression, Environment, Store[Value], Value]](
        [
            (
                If(Bool(True), Int(10), Int(20)),
                {},
                Store(),
                Int(10),
            ),
            (
                If(Bool(False), Int(10), Int(20)),
                {},
                Store(),
                Int(20),
            ),
        ]
    ),
)
def test_eval_expression_if(
    expr: Expression,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store) == expected


@pytest.mark.parametrize(
    "expr, env, store, expected",
    list[tuple[Expression, Environment, Store[Value], Value]](
        [
            (
                LessThan(Int(1), Int(2)),
                {},
                Store(),
                Bool(True),
            ),
        ]
    ),
)
def test_eval_expression_less_than(
    expr: Expression,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store) == expected


@pytest.mark.parametrize(
    "expr, env, store, expected",
    list[tuple[Expression, Environment, Store[Value], Value]](
        [
            (
                EqualTo(Int(1), Int(2)),
                {},
                Store(),
                Bool(False),
            ),
            (
                EqualTo(Bool(True), Bool(True)),
                {},
                Store(),
                Bool(True),
            ),
        ]
    ),
)
def test_eval_expression_equal_to(
    expr: Expression,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store) == expected


@pytest.mark.parametrize(
    "expr, env, store, expected",
    list[tuple[Expression, Environment, Store[Value], Value]](
        [
            (
                GreaterThanOrEqualTo(Int(2), Int(1)),
                {},
                Store(),
                Bool(True),
            ),
        ]
    ),
)
def test_eval_expression_greater_than_or_equal_to(
    expr: Expression,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store) == expected


@pytest.mark.parametrize(
    "expr, env, store, expected",
    list[tuple[Expression, Environment, Store[Value], Value]](
        [
            (
                Unit(),
                {},
                Store(),
                Unit(),
            ),
        ]
    ),
)
def test_eval_expression_unit(
    expr: Unit,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store) == expected


@pytest.mark.parametrize(
    "expr, env, store, expected",
    list[tuple[Expression, Environment, Store[Value], Value]](
        [
            (
                Tuple([]),
                {},
                Store(),
                Location(0),
            ),
        ]
    ),
)
def test_eval_expression_cell(
    expr: Expression,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store) == expected


@pytest.mark.parametrize(
    "expr, env, store, expected",
    list[tuple[Expression, Environment, Store[Value], Value]](
        [
            (
                Get(Tuple[Expression]([Int(0)]), Int(0)),
                {},
                Store(),
                Int(0),
            ),
        ]
    ),
)
def test_eval_expression_get(
    expr: Expression,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store) == expected


@pytest.mark.parametrize(
    "expr, env, store, expected",
    list[tuple[Expression, Environment, Store[Value], Value]](
        [
            (
                Set(Tuple[Expression]([Int(0)]), Int(0), Int(0)),
                {},
                Store(),
                Unit(),
            ),
        ]
    ),
)
def test_eval_expression_set(
    expr: Expression,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store) == expected


@pytest.mark.xfail
@pytest.mark.parametrize(
    "expr, env, store, expected",
    list[tuple[Expression, Environment, Store[Value], Value]](
        [
            (
                Lambda([], Var("x")),
                {},
                Store(),
                Closure(Lambda([], Var("x")), {}),
            ),
        ]
    ),
)
def test_eval_expression_lambda(
    expr: Expression,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store) == expected


@pytest.mark.xfail
@pytest.mark.parametrize(
    "expr, env, store, expected",
    list[tuple[Expression, Environment, Store[Value], Value]](
        [
            (
                Apply(Lambda(["x"], Var("x")), [Int(0)]),
                {},
                Store(),
                Int(0),
            ),
        ]
    ),
)
def test_eval_expression_apply(
    expr: Expression,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store) == expected
