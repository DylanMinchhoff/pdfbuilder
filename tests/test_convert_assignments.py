import pytest
import sucrose
from sucrose import (
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
    Assign,
)
import glucose
from convert_assignments import convert_assignments, convert_assignments_expresssion, mutable_free_variables


@pytest.mark.parametrize(
    "program, expected",
    list[tuple[sucrose.Program, glucose.Program]](
        [
            (
                sucrose.Program([], Int(0)),
                glucose.Program([], Int(0)),
            ),
            (
                sucrose.Program(["x"], Int(0)),
                glucose.Program(["x"], Int(0)),
            ),
        ]
    ),
)
def test_convert_assignments(
    program: sucrose.Program,
    expected: glucose.Expression,
) -> None:
    assert convert_assignments(program) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                Int(0),
                set(),
                Int(0),
            ),
        ]
    ),
)
def test_convert_assignments_expression_int(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assignments_expresssion(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                Add(Int(0), Int(0)),
                set(),
                Add(Int(0), Int(0)),
            ),
        ]
    ),
)
def test_convert_assignments_expression_add(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assignments_expresssion(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                Subtract(Int(0), Int(0)),
                set(),
                Subtract(Int(0), Int(0)),
            ),
        ]
    ),
)
def test_convert_assignments_expression_subtract(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assignments_expresssion(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                Multiply(Int(0), Int(0)),
                set(),
                Multiply(Int(0), Int(0)),
            ),
        ]
    ),
)
def test_convert_assignments_expression_multiply(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assignments_expresssion(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                Var("x"),
                set(),
                Var("x"),
            ),
            (
                Var("x"),
                {"x"},
                Get(Var("x"), Int(0)),
            ),
        ]
    ),
)
def test_convert_assignments_expression_var(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assignments_expresssion(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                Bool(True),
                set(),
                Bool(True),
            ),
        ]
    ),
)
def test_convert_assignments_expression_bool(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assignments_expresssion(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                If(Var("c"), Var("x"), Var("y")),
                set(),
                If(Var("c"), Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_convert_assignments_expression_if(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assignments_expresssion(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                LessThan(Int(0), Int(0)),
                set(),
                LessThan(Int(0), Int(0)),
            ),
        ]
    ),
)
def test_convert_assignments_expression_less_than(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assignments_expresssion(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                EqualTo(Int(0), Int(0)),
                set(),
                EqualTo(Int(0), Int(0)),
            ),
        ]
    ),
)
def test_convert_assignments_expression_equal_to(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assignments_expresssion(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                GreaterThanOrEqualTo(Int(0), Int(0)),
                set(),
                GreaterThanOrEqualTo(Int(0), Int(0)),
            ),
        ]
    ),
)
def test_convert_assignments_expression_greater_than_or_equal_to(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assignments_expresssion(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                Unit(),
                set(),
                Unit(),
            ),
        ]
    ),
)
def test_convert_assignments_expression_unit(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assignments_expresssion(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                Tuple([Unit()]),
                set(),
                Tuple([Unit()]),
            ),
        ]
    ),
)
def test_convert_assignments_expression_cell(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assignments_expresssion(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                Get(Var("x"), Int(0)),
                set(),
                Get(Var("x"), Int(0)),
            ),
        ]
    ),
)
def test_convert_assignments_expression_get(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assignments_expresssion(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                Set(Var("x"), Int(0), Var("y")),
                set(),
                Set(Var("x"), Int(0), Var("y")),
            ),
        ]
    ),
)
def test_convert_assignments_expression_set(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assignments_expresssion(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                Lambda([], Int(0)),
                set(),
                Lambda([], Int(0)),
            ),
            (
                Lambda[sucrose.Expression](["x"], Assign("x", Unit())),
                set(),
                Lambda[glucose.Expression](
                    ["x"],
                    Apply(
                        Lambda(["x"], Set(Var("x"), Int(0), Unit())),
                        [Tuple([Var("x")])],
                    ),
                ),
            ),
        ]
    ),
)
def test_convert_assignments_expression_lambda(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assignments_expresssion(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                Apply(Var("x"), []),
                set(),
                Apply(Var("x"), []),
            ),
        ]
    ),
)
def test_convert_assignments_expression_apply(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assignments_expresssion(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                Assign("x", Int(0)),
                set(),
                Set(Var("x"), Int(0), Int(0)),
            ),
        ]
    ),
)
def test_convert_assignments_expression_assign(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assignments_expresssion(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sucrose.Expression, set[str]]](
        [
            (Int(0), set()),
            (Add(Int(0), Int(0)), set()),
            (Subtract(Int(0), Int(0)), set()),
            (Multiply(Int(0), Int(0)), set()),
            (Var("x"), set()),
            (Bool(True), set()),
            (If(Var("x"), Var("x"), Var("y")), set()),
            (LessThan(Int(0), Int(0)), set()),
            (EqualTo(Int(0), Int(0)), set()),
            (GreaterThanOrEqualTo(Int(0), Int(0)), set()),
            (Unit(), set()),
            (Tuple([]), set()),
            (Get(Var("x"), Int(0)), set()),
            (Set(Var("x"), Int(0), Var("y")), set()),
            (Assign("x", Var("y")), {"x"}),
            (Lambda("x", Var("y")), set()),
            (Apply(Var("x"), []), set()),
        ]
    ),
)
def test_mutable_variables(
    expr: sucrose.Expression,
    expected: set[str],
) -> None:
    assert mutable_free_variables(expr) == expected
