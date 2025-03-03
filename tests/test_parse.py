import pytest
from fructose import (
    Program,
    Expression,
    Int,
    Add,
    Subtract,
    Multiply,
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
    LessThanOrEqualTo,
    LessThan,
    EqualTo,
    GreaterThan,
    GreaterThanOrEqualTo,
    Unit,
    Cell,
    Get,
    Set,
    Begin,
    While,
    Lambda,
    Apply,
    Assign,
)
from parse import parse, parse_expression


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Program]](
        [
            (
                "(program () 0)",
                Program([], [], Int(0)),
            ),
            (
                "(program (x) x)",
                Program(["x"], [], Var("x")),
            ),
            (
                "(program () (def x 5) #u)",
                Program([], [("x", Int(5))], Unit()),
            ),
            (
                "(program () (def (id x) x) #u)",
                Program([], [("id", Lambda(["x"], Var("x")))], Unit()),
            ),
        ]
    ),
)
def test_parse(
    source: str,
    expected: Int,
) -> None:
    assert parse(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "0",
                Int(0),
            ),
        ]
    ),
)
def test_parse_expression_int(
    source: str,
    expected: Int,
) -> None:
    assert parse_expression(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(+)",
                Add([]),
            ),
            (
                "(+ 1 2)",
                Add([Int(1), Int(2)]),
            ),
        ]
    ),
)
def test_parse_expression_add(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expression(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(- 2)",
                Subtract([Int(2)]),
            ),
            (
                "(- 2 1)",
                Subtract([Int(2), Int(1)]),
            ),
        ]
    ),
)
def test_parse_expression_subtract(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expression(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(*)",
                Multiply([]),
            ),
            (
                "(* 1 2)",
                Multiply([Int(1), Int(2)]),
            ),
        ]
    ),
)
def test_parse_expression_multiply(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expression(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(let () x)",
                Let([], Var("x")),
            ),
            (
                "(let ((x 1)) x)",
                Let([("x", Int(1))], Var("x")),
            ),
        ]
    ),
)
def test_parse_expression_let(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expression(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(let* () x)",
                LetStar([], Var("x")),
            ),
            (
                "(let* ((x 1)) x)",
                LetStar([("x", Int(1))], Var("x")),
            ),
        ]
    ),
)
def test_parse_expression_letstar(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expression(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(letrec () x)",
                LetRec([], Var("x")),
            ),
            (
                "(letrec ((x 1)) x)",
                LetRec([("x", Int(1))], Var("x")),
            ),
        ]
    ),
)
def test_parse_expression_letrec(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expression(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "x",
                Var("x"),
            ),
        ]
    ),
)
def test_parse_expression_var(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expression(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "#t",
                Bool(True),
            ),
            (
                "#f",
                Bool(False),
            ),
        ]
    ),
)
def test_parse_expression_bool(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expression(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(not #t)",
                Not(Bool(True)),
            ),
        ]
    ),
)
def test_parse_expression_not(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expression(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(and)",
                And([]),
            ),
            (
                "(and #t)",
                And([Bool(True)]),
            ),
        ]
    ),
)
def test_parse_expression_and(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expression(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(or)",
                Or([]),
            ),
            (
                "(or #t)",
                Or([Bool(True)]),
            ),
        ]
    ),
)
def test_parse_expression_or(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expression(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(if x 1 0)",
                If(Var("x"), Int(1), Int(0)),
            ),
        ]
    ),
)
def test_parse_expression_if(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expression(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(cond (else #u))",
                Cond([], Unit()),
            ),
            (
                "(cond ((> x 0) 5) (else #u))",
                Cond([(GreaterThan([Var("x"), Int(0)]), Int(5))], Unit()),
            ),
        ]
    ),
)
def test_parse_expression_cond(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expression(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(<=)",
                LessThanOrEqualTo([]),
            ),
            (
                "(<= 1 0)",
                LessThanOrEqualTo([Int(1), Int(0)]),
            ),
        ]
    ),
)
def test_parse_expression_less_than_or_equal_to(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expression(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(<)",
                LessThan([]),
            ),
            (
                "(< 1 0)",
                LessThan([Int(1), Int(0)]),
            ),
        ]
    ),
)
def test_parse_expression_less_than(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expression(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(==)",
                EqualTo([]),
            ),
            (
                "(== 1 0)",
                EqualTo([Int(1), Int(0)]),
            ),
        ]
    ),
)
def test_parse_expression_equal_to(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expression(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(>)",
                GreaterThan([]),
            ),
            (
                "(> 1 0)",
                GreaterThan([Int(1), Int(0)]),
            ),
        ]
    ),
)
def test_parse_expression_greater_than(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expression(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(>= 1 0)",
                GreaterThanOrEqualTo([Int(1), Int(0)]),
            ),
        ]
    ),
)
def test_parse_expression_greater_than_or_equal_to(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expression(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "#u",
                Unit(),
            ),
        ]
    ),
)
def test_parse_expression_unit(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expression(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(cell #u)",
                Cell(Unit()),
            ),
        ]
    ),
)
def test_parse_expression_cell(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expression(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(^ x)",
                Get(Var("x")),
            ),
        ]
    ),
)
def test_parse_expression_get(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expression(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(:= x #u)",
                Set(Var("x"), Unit()),
            ),
        ]
    ),
)
def test_parse_expression_set(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expression(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(begin)",
                Begin([]),
            ),
            (
                "(begin x #u)",
                Begin([Var("x"), Unit()]),
            ),
        ]
    ),
)
def test_parse_expression_begin(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expression(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(while #t #u)",
                While(Bool(True), Unit()),
            ),
        ]
    ),
)
def test_parse_expression_while(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expression(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(lambda () #u)",
                Lambda([], Unit()),
            ),
        ]
    ),
)
def test_parse_expression_lambda(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expression(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(x)",
                Apply(Var("x"), []),
            ),
        ]
    ),
)
def test_parse_expression_apply(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expression(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(set! x #u)",
                Assign("x", Unit()),
            ),
        ]
    ),
)
def test_parse_expression_assign(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expression(source) == expected
