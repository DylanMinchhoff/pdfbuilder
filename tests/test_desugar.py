import pytest
import sugar
from sugar import Int, Let, Var, LetStar, Bool, Not, All, Any, If, Cond, Unit, Cell, Get, Set, While
import kernel
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
                sugar.Add([]),
                Int(0),
            ),
            (
                sugar.Add([Int(1)]),
                kernel.Add(Int(1), Int(0)),
            ),
            (
                sugar.Add([Int(1), Int(1)]),
                kernel.Add(Int(1), kernel.Add(Int(1), Int(0))),
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
                sugar.Subtract([Int(1)]),
                kernel.Subtract(Int(0), Int(1)),
            ),
            (
                sugar.Subtract([Int(2), Int(1)]),
                kernel.Subtract(Int(2), Int(1)),
            ),
            (
                sugar.Subtract([Int(3), Int(2), Int(1)]),
                kernel.Subtract(Int(3), kernel.Subtract(Int(2), Int(1))),
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
                sugar.Multiply([]),
                Int(1),
            ),
            (
                sugar.Multiply([Int(1)]),
                kernel.Multiply(Int(1), Int(1)),
            ),
            (
                sugar.Multiply([Int(2), Int(2)]),
                kernel.Multiply(Int(2), kernel.Multiply(Int(2), Int(1))),
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
                Not(Var("x")),
                If(kernel.EqualTo(Var("x"), Bool(True)), Bool(False), Bool(True)),
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
                sugar.LessThanOrEqualTo([]),
                Bool(True),
            ),
            (
                sugar.LessThanOrEqualTo([Int(0)]),
                Bool(True),
            ),
            (
                sugar.LessThanOrEqualTo([Int(1), Int(2)]),
                kernel.GreaterThanOrEqualTo(Int(2), Int(1)),
            ),
            (
                sugar.LessThanOrEqualTo([Int(1), Int(2), Int(3)]),
                If(
                    kernel.GreaterThanOrEqualTo(Int(2), Int(1)),
                    kernel.GreaterThanOrEqualTo(Int(3), Int(2)),
                    Bool(False),
                ),
            ),
        ]
    ),
)
def test_desugar_expr_less_than_or_equal_to(
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
                sugar.LessThan([]),
                Bool(True),
            ),
            (
                sugar.LessThan([Int(0)]),
                Bool(True),
            ),
            (
                sugar.LessThan([Int(1), Int(2)]),
                kernel.LessThan(Int(1), Int(2)),
            ),
            (
                sugar.LessThan([Int(1), Int(2), Int(3)]),
                If(
                    kernel.LessThan(Int(1), Int(2)),
                    kernel.LessThan(Int(2), Int(3)),
                    Bool(False),
                ),
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
                sugar.EqualTo([]),
                Bool(True),
            ),
            (
                sugar.EqualTo([Int(0)]),
                Bool(True),
            ),
            (
                sugar.EqualTo([Int(1), Int(2)]),
                kernel.EqualTo(Int(1), Int(2)),
            ),
            (
                sugar.EqualTo([Int(1), Int(2), Int(3)]),
                If(
                    kernel.EqualTo(Int(1), Int(2)),
                    kernel.EqualTo(Int(2), Int(3)),
                    Bool(False),
                ),
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
                sugar.GreaterThan([]),
                Bool(True),
            ),
            (
                sugar.GreaterThan([Int(0)]),
                Bool(True),
            ),
            (
                sugar.GreaterThan([Int(1), Int(2)]),
                kernel.LessThan(Int(2), Int(1)),
            ),
            (
                sugar.GreaterThan([Int(1), Int(2), Int(3)]),
                If(
                    kernel.LessThan(Int(2), Int(1)),
                    kernel.LessThan(Int(3), Int(2)),
                    Bool(False),
                ),
            ),
        ]
    ),
)
def test_desugar_expr_greater_than(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                sugar.GreaterThanOrEqualTo([]),
                Bool(True),
            ),
            (
                sugar.GreaterThanOrEqualTo([Int(0)]),
                Bool(True),
            ),
            (
                sugar.GreaterThanOrEqualTo([Int(1), Int(2)]),
                kernel.GreaterThanOrEqualTo(Int(1), Int(2)),
            ),
            (
                sugar.GreaterThanOrEqualTo([Int(1), Int(2), Int(3)]),
                If(
                    kernel.GreaterThanOrEqualTo(Int(1), Int(2)),
                    kernel.GreaterThanOrEqualTo(Int(2), Int(3)),
                    Bool(False),
                ),
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
                Unit(),
                Unit(),
            ),
        ]
    ),
)
def test_desugar_expr_unit(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                Cell(Unit()),
                Cell(Unit()),
            ),
        ]
    ),
)
def test_desugar_expr_cell(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                Get(Var("x")),
                Get(Var("x")),
            ),
        ]
    ),
)
def test_desugar_expr_get(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                Set(Var("x"), Var("y")),
                Set(Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_desugar_expr_set(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                sugar.Do([]),
                Unit(),
            ),
            (
                sugar.Do([Int(0)]),
                Int(0),
            ),
            (
                sugar.Do([Unit(), Int(0)]),
                kernel.Do(Unit(), Int(0)),
            ),
        ]
    ),
)
def test_desugar_expr_begin(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Expression, kernel.Expression]](
        [
            (
                While(Var("x"), Var("y")),
                While(Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_desugar_expr_while(
    expr: sugar.Expression,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected
