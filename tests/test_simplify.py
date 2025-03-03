from collections.abc import Callable
import pytest
import fructose
from fructose import (
    Int,
    Let,
    LetStar,
    LetRec,
    Var,
    Bool,
    Not,
    And,
    Or,
    If,
    Cond,
    Unit,
    Cell,
    Begin,
    While,
    Assign,
    Lambda,
    Apply,
)
import sucrose
from sucrose import Tuple
from simplify import simplify, simplify_expression
from util import SequentialNameGenerator


@pytest.mark.xfail
@pytest.mark.parametrize(
    "program, fresh, expected",
    list[tuple[fructose.Program, Callable[[str], str], sucrose.Program]](
        [
            (
                fructose.Program([], [], Int(0)),
                SequentialNameGenerator(),
                sucrose.Program([], Int(0)),
            ),
        ]
    ),
)
def test_desugar(
    program: fructose.Program,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify(program, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                Int(0),
                SequentialNameGenerator(),
                Int(0),
            ),
        ]
    ),
)
def test_simplify_expression_int(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                fructose.Add([]),
                SequentialNameGenerator(),
                Int(0),
            ),
            (
                fructose.Add([Int(1)]),
                SequentialNameGenerator(),
                Int(1),
            ),
            (
                fructose.Add([Int(1), Int(1)]),
                SequentialNameGenerator(),
                sucrose.Add(Int(1), Int(1)),
            ),
        ]
    ),
)
def test_simplify_expression_add(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                fructose.Subtract([Int(1)]),
                SequentialNameGenerator(),
                sucrose.Subtract(Int(0), Int(1)),
            ),
            (
                fructose.Subtract([Int(2), Int(1)]),
                SequentialNameGenerator(),
                sucrose.Subtract(Int(2), Int(1)),
            ),
            (
                fructose.Subtract([Int(3), Int(2), Int(1)]),
                SequentialNameGenerator(),
                sucrose.Subtract(Int(3), sucrose.Subtract(Int(2), Int(1))),
            ),
        ]
    ),
)
def test_simplify_expression_subtract(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                fructose.Multiply([]),
                SequentialNameGenerator(),
                Int(1),
            ),
            (
                fructose.Multiply([Int(1)]),
                SequentialNameGenerator(),
                Int(1),
            ),
            (
                fructose.Multiply([Int(2), Int(1)]),
                SequentialNameGenerator(),
                sucrose.Multiply(Int(2), Int(1)),
            ),
        ]
    ),
)
def test_simplify_expression_multiply(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.xfail
@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                Let([("x", Int(0))], Var("x")),
                SequentialNameGenerator(),
                Apply(Lambda(["x"], Var("x")), [Int(0)]),
            ),
        ]
    ),
)
def test_simplify_expression_let(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.xfail
@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                LetStar([], Var("x")),
                SequentialNameGenerator(),
                Var("x"),
            ),
            (
                LetStar([("x", Int(0))], Var("x")),
                SequentialNameGenerator(),
                Apply(Lambda(["x"], Var("x")), [Int(0)]),
            ),
            (
                LetStar([("x", Int(0)), ("y", Int(1))], Var("x")),
                SequentialNameGenerator(),
                Apply(Lambda(["x"], Apply(Lambda(["y"], Var("x")), [Int(1)])), [Int(0)]),
            ),
        ]
    ),
)
def test_simplify_expression_letstar(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.xfail
@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                LetRec([], Var("x")),
                SequentialNameGenerator(),
                Var("x"),
            ),
            (
                LetRec([("x", Int(0))], Var("x")),
                SequentialNameGenerator(),
                Apply(Lambda(["x"], Apply(Lambda(["_t0"], Var("x")), [Assign("x", Int(0))])), [Unit()]),
            ),
            (
                LetRec([("x", Int(0)), ("y", Int(1))], Var("x")),
                SequentialNameGenerator(),
                Apply(
                    Lambda(
                        ["x", "y"],
                        Apply(
                            Lambda(["_t0"], Apply(Lambda(["_t1"], Var("x")), [Assign("y", Int(1))])),
                            [Assign("x", Int(0))],
                        ),
                    ),
                    [Unit(), Unit()],
                ),
            ),
        ]
    ),
)
def test_simplify_expression_letrec(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                Var("x"),
                SequentialNameGenerator(),
                Var("x"),
            ),
        ]
    ),
)
def test_simplify_expression_var(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                Bool(True),
                SequentialNameGenerator(),
                Bool(True),
            ),
        ]
    ),
)
def test_simplify_expression_bool(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                Not(Var("x")),
                SequentialNameGenerator(),
                If(sucrose.EqualTo(Var("x"), Bool(True)), Bool(False), Bool(True)),
            ),
        ]
    ),
)
def test_simplify_expression_not(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                And([]),
                SequentialNameGenerator(),
                Bool(True),
            ),
            (
                And([Bool(True)]),
                SequentialNameGenerator(),
                Bool(True),
            ),
            (
                And([Bool(True), Bool(False)]),
                SequentialNameGenerator(),
                If(Bool(True), Bool(False), Bool(False)),
            ),
            (
                And([Bool(True), Bool(True), Bool(False)]),
                SequentialNameGenerator(),
                If(Bool(True), If(Bool(True), Bool(True), Bool(False)), Bool(False)),
            ),
        ]
    ),
)
def test_simplify_expression_and(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                Or([]),
                SequentialNameGenerator(),
                Bool(False),
            ),
            (
                Or([Bool(True)]),
                SequentialNameGenerator(),
                Bool(True),
            ),
            (
                Or([Bool(True), Bool(False)]),
                SequentialNameGenerator(),
                If(Bool(True), Bool(True), Bool(False)),
            ),
            (
                Or([Bool(False), Bool(False), Bool(True)]),
                SequentialNameGenerator(),
                If(Bool(False), Bool(True), If(Bool(False), Bool(True), Bool(False))),
            ),
        ]
    ),
)
def test_simplify_expression_or(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                If(Bool(True), Var("x"), Var("y")),
                SequentialNameGenerator(),
                If(Bool(True), Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_simplify_expression_if(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                Cond([], Int(0)),
                SequentialNameGenerator(),
                Int(0),
            ),
            (
                Cond([(Bool(True), Int(1))], Int(0)),
                SequentialNameGenerator(),
                If(Bool(True), Int(1), Int(0)),
            ),
        ]
    ),
)
def test_simplify_expression_cond(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                fructose.LessThanOrEqualTo([]),
                SequentialNameGenerator(),
                Bool(True),
            ),
            (
                fructose.LessThanOrEqualTo([Int(0)]),
                SequentialNameGenerator(),
                Bool(True),
            ),
            (
                fructose.LessThanOrEqualTo([Int(1), Int(2)]),
                SequentialNameGenerator(),
                sucrose.GreaterThanOrEqualTo(Int(2), Int(1)),
            ),
            (
                fructose.LessThanOrEqualTo([Int(1), Int(2), Int(3)]),
                SequentialNameGenerator(),
                If(
                    sucrose.GreaterThanOrEqualTo(Int(2), Int(1)),
                    sucrose.GreaterThanOrEqualTo(Int(3), Int(2)),
                    Bool(False),
                ),
            ),
        ]
    ),
)
def test_simplify_expression_less_than_or_equal_to(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                fructose.LessThan([]),
                SequentialNameGenerator(),
                Bool(True),
            ),
            (
                fructose.LessThan([Int(0)]),
                SequentialNameGenerator(),
                Bool(True),
            ),
            (
                fructose.LessThan([Int(1), Int(2)]),
                SequentialNameGenerator(),
                sucrose.LessThan(Int(1), Int(2)),
            ),
            (
                fructose.LessThan([Int(1), Int(2), Int(3)]),
                SequentialNameGenerator(),
                If(
                    sucrose.LessThan(Int(1), Int(2)),
                    sucrose.LessThan(Int(2), Int(3)),
                    Bool(False),
                ),
            ),
        ]
    ),
)
def test_simplify_expression_less_than(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                fructose.EqualTo([]),
                SequentialNameGenerator(),
                Bool(True),
            ),
            (
                fructose.EqualTo([Int(0)]),
                SequentialNameGenerator(),
                Bool(True),
            ),
            (
                fructose.EqualTo([Int(1), Int(2)]),
                SequentialNameGenerator(),
                sucrose.EqualTo(Int(1), Int(2)),
            ),
            (
                fructose.EqualTo([Int(1), Int(2), Int(3)]),
                SequentialNameGenerator(),
                If(
                    sucrose.EqualTo(Int(1), Int(2)),
                    sucrose.EqualTo(Int(2), Int(3)),
                    Bool(False),
                ),
            ),
        ]
    ),
)
def test_simplify_expression_equal_to(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                fructose.GreaterThan([]),
                SequentialNameGenerator(),
                Bool(True),
            ),
            (
                fructose.GreaterThan([Int(0)]),
                SequentialNameGenerator(),
                Bool(True),
            ),
            (
                fructose.GreaterThan([Int(1), Int(2)]),
                SequentialNameGenerator(),
                sucrose.LessThan(Int(2), Int(1)),
            ),
            (
                fructose.GreaterThan([Int(1), Int(2), Int(3)]),
                SequentialNameGenerator(),
                If(
                    sucrose.LessThan(Int(2), Int(1)),
                    sucrose.LessThan(Int(3), Int(2)),
                    Bool(False),
                ),
            ),
        ]
    ),
)
def test_simplify_expression_greater_than(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                fructose.GreaterThanOrEqualTo([]),
                SequentialNameGenerator(),
                Bool(True),
            ),
            (
                fructose.GreaterThanOrEqualTo([Int(0)]),
                SequentialNameGenerator(),
                Bool(True),
            ),
            (
                fructose.GreaterThanOrEqualTo([Int(1), Int(2)]),
                SequentialNameGenerator(),
                sucrose.GreaterThanOrEqualTo(Int(1), Int(2)),
            ),
            (
                fructose.GreaterThanOrEqualTo([Int(1), Int(2), Int(3)]),
                SequentialNameGenerator(),
                If(
                    sucrose.GreaterThanOrEqualTo(Int(1), Int(2)),
                    sucrose.GreaterThanOrEqualTo(Int(2), Int(3)),
                    Bool(False),
                ),
            ),
        ]
    ),
)
def test_simplify_expression_greater_than_or_equal_to(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                Unit(),
                SequentialNameGenerator(),
                Unit(),
            ),
        ]
    ),
)
def test_simplify_expression_unit(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                Cell(Unit()),
                SequentialNameGenerator(),
                Tuple([Unit()]),
            ),
        ]
    ),
)
def test_simplify_expression_cell(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                fructose.Get(Var("x")),
                SequentialNameGenerator(),
                sucrose.Get(Var("x"), Int(0)),
            ),
        ]
    ),
)
def test_simplify_expression_get(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                fructose.Set(Var("x"), Var("y")),
                SequentialNameGenerator(),
                sucrose.Set(Var("x"), Int(0), Var("y")),
            ),
        ]
    ),
)
def test_simplify_expression_set(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.xfail
@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                Begin([]),
                SequentialNameGenerator(),
                Unit(),
            ),
            (
                Begin([Int(0)]),
                SequentialNameGenerator(),
                Int(0),
            ),
            (
                Begin([Unit(), Int(0)]),
                SequentialNameGenerator(),
                Apply(Lambda(["_t0"], Int(0)), [Unit()]),
            ),
        ]
    ),
)
def test_simplify_expression_begin(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.xfail
@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                While(Var("x"), Var("y")),
                SequentialNameGenerator(),
                Apply(
                    Lambda(
                        ["_loop0"],
                        Apply(
                            Lambda(["_t0"], Apply(Var("_loop0"), [])),
                            [
                                Assign(
                                    "_loop0",
                                    Lambda(
                                        [],
                                        If(
                                            condition=Var("x"),
                                            consequent=Apply(
                                                Lambda(
                                                    ["_t1"],
                                                    Apply(Var("_loop0"), []),
                                                ),
                                                [Var("y")],
                                            ),
                                            alternative=Unit(),
                                        ),
                                    ),
                                )
                            ],
                        ),
                    ),
                    [Unit()],
                ),
            ),
        ]
    ),
)
def test_simplify_expression_while(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.xfail
@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                Lambda("x", Var("y")),
                SequentialNameGenerator(),
                Lambda("x", Var("y")),
            ),
        ]
    ),
)
def test_simplify_expression_lambda(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.xfail
@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                Apply(Var("x"), []),
                SequentialNameGenerator(),
                Apply(Var("x"), []),
            ),
        ]
    ),
)
def test_simplify_expression_apply(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.xfail
@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                Assign("x", Var("y")),
                SequentialNameGenerator(),
                Assign("x", Var("y")),
            ),
        ]
    ),
)
def test_simplify_expression_assign(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected
