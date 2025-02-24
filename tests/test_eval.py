from collections.abc import Sequence
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
    Unit,
    Cell,
    Get,
    Set,
    Do,
    While,
)
from eval import Location, Store, Value, Environment, eval, eval_expr


@pytest.mark.parametrize(
    "program, arguments, expected",
    list[tuple[Program, Sequence[Int], Value]](
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
    arguments: Sequence[Int],
    expected: Value,
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
def test_eval_expr_int(
    expr: Int,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expr(expr, env, store) == expected


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
def test_eval_expr_add(
    expr: Expression,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expr(expr, env, store) == expected


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
def test_eval_expr_subtract(
    expr: Expression,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expr(expr, env, store) == expected


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
    assert eval_expr(expr, env, store) == expected


@pytest.mark.parametrize(
    "expr, env, store, expected",
    list[tuple[Expression, Environment, Store[Value], Value]](
        [
            (
                Let("x", Int(1), Var("x")),
                {},
                Store(),
                Int(1),
            ),
        ]
    ),
)
def test_eval_expr_let(
    expr: Expression,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expr(expr, env, store) == expected


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
def test_eval_expr_var(
    expr: Var,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expr(expr, env, store) == expected


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
def test_eval_expr_bool(
    expr: Bool,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expr(expr, env, store) == expected


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
def test_eval_expr_if(
    expr: Expression,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expr(expr, env, store) == expected


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
def test_eval_expr_less_than(
    expr: Expression,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expr(expr, env, store) == expected


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
def test_eval_expr_equal_to(
    expr: Expression,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expr(expr, env, store) == expected


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
def test_eval_expr_greater_than_or_equal_to(
    expr: Expression,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expr(expr, env, store) == expected


@pytest.mark.xfail()
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
def test_eval_expr_unit(
    expr: Unit,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expr(expr, env, store) == expected


@pytest.mark.xfail()
@pytest.mark.parametrize(
    "expr, env, store, expected",
    list[tuple[Expression, Environment, Store[Value], Value]](
        [
            (
                Cell(Unit()),
                {},
                Store(),
                Location(0),
            ),
        ]
    ),
)
def test_eval_expr_cell(
    expr: Expression,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expr(expr, env, store) == expected


@pytest.mark.xfail()
@pytest.mark.parametrize(
    "expr, env, store, expected",
    list[tuple[Expression, Environment, Store[Value], Value]](
        [
            (
                Get(Cell[Expression](Int(0))),
                {},
                Store(),
                Int(0),
            ),
        ]
    ),
)
def test_eval_expr_get(
    expr: Expression,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expr(expr, env, store) == expected


@pytest.mark.xfail()
@pytest.mark.parametrize(
    "expr, env, store, expected",
    list[tuple[Expression, Environment, Store[Value], Value]](
        [
            (
                Set(Cell[Expression](Int(0)), Int(0)),
                {},
                Store(),
                Unit(),
            ),
        ]
    ),
)
def test_eval_expr_set(
    expr: Expression,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expr(expr, env, store) == expected


@pytest.mark.xfail()
@pytest.mark.parametrize(
    "expr, env, store, expected",
    list[tuple[Expression, Environment, Store[Value], Value]](
        [
            (
                Do(Unit(), Int(1)),
                {},
                Store(),
                Int(1),
            ),
        ]
    ),
)
def test_eval_expr_do(
    expr: Expression,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expr(expr, env, store) == expected


@pytest.mark.xfail()
@pytest.mark.parametrize(
    "expr, env, store, expected",
    list[tuple[Expression, Environment, Store[Value], Value]](
        [
            (
                While(Bool(False), Var("x")),
                {},
                Store(),
                Unit(),
            ),
            (
                Let(
                    "x",
                    Cell(Bool(True)),
                    While(
                        Get(Var("x")),
                        Set(Var("x"), Bool(False)),
                    ),
                ),
                {},
                Store(),
                Unit(),
            ),
        ]
    ),
)
def test_eval_expr_while(
    expr: Expression,
    env: Environment,
    store: Store[Value],
    expected: Value,
) -> None:
    assert eval_expr(expr, env, store) == expected
