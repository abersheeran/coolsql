import pytest

from coolsql import Case, Field

field_name = Field("name")
field_age = Field("age")


@pytest.mark.parametrize(
    "expr,sql,parameters",
    [
        (
            field_age > 10,
            '"age" > 10',
            [],
        ),
        (
            field_age >= 10,
            '"age" >= 10',
            [],
        ),
        (field_age < 10, '"age" < 10', []),
        (
            field_age <= 10,
            '"age" <= 10',
            [],
        ),
        (
            field_age == 10,
            '"age" = 10',
            [],
        ),
        (
            field_age != 10,
            '"age" <> 10',
            [],
        ),
        (
            field_age + 10 == 20,
            '"age" + 10 = 20',
            [],
        ),
        (
            field_age - 10 == 20,
            '"age" - 10 = 20',
            [],
        ),
        (
            field_age * 10 == 20,
            '"age" * 10 = 20',
            [],
        ),
        (
            field_age / 10 == 20,
            '"age" / 10 = 20',
            [],
        ),
        (
            field_age % 10 == 20,
            '"age" % 10 = 20',
            [],
        ),
        (
            10 + field_age == 20,
            '10 + "age" = 20',
            [],
        ),
        (
            10 - field_age == 20,
            '10 - "age" = 20',
            [],
        ),
        (
            10 * field_age == 20,
            '10 * "age" = 20',
            [],
        ),
        (
            10 / field_age == 20,
            '10 / "age" = 20',
            [],
        ),
        (
            10 % field_age == 20,
            '10 % "age" = 20',
            [],
        ),
        (
            (field_age + 10) / 10 == 20,
            '("age" + 10) / 10 = 20',
            [],
        ),
        (
            (field_age - 10) / (field_age + 10) == 20,
            '("age" - 10) / ("age" + 10) = 20',
            [],
        ),
        (
            ~(field_age > 10),
            'NOT ("age" > 10)',
            [],
        ),
        (
            ~(~(field_age > 10)),
            '"age" > 10',
            [],
        ),
        (
            field_age.between(18, 24),
            '"age" BETWEEN 18 AND 24',
            [],
        ),
        (
            field_name.like("%a%"),
            '"name" LIKE ?',
            ["%a%"],
        ),
        (
            field_name.isnull(),
            '"name" IS NULL',
            [],
        ),
        (
            ~field_name.isnull() & field_name.like("%a%"),
            '(NOT ("name" IS NULL)) AND ("name" LIKE ?)',
            ["%a%"],
        ),
        (
            field_name.isnull() | field_age.between(0, 18),
            '("name" IS NULL) OR ("age" BETWEEN 0 AND 18)',
            [],
        ),
        (
            field_age.isin([10, 20, 30]),
            '"age" IN (?)',
            [[10, 20, 30]],
        ),
        (
            Case().when(1, 0).else_(1),
            "CASE WHEN 1 THEN 0 ELSE 1 END",
            [],
        ),
        (
            Case(field_age).when(18, 1).else_(0),
            'CASE "age" WHEN 18 THEN 1 ELSE 0 END',
            [],
        ),
        (
            Case(field_age).when(field_age >= 18, 1).else_(0),
            'CASE "age" WHEN "age" >= 18 THEN 1 ELSE 0 END',
            [],
        ),
    ],
)
def test_expr(expr, sql, parameters):
    assert expr.compile() == (sql, parameters)


@pytest.mark.parametrize(
    "expr",
    [
        lambda: 0 & (field_age < 80),
        lambda: 0 | (field_age < 80),
    ],
)
def test_type_error(expr):
    with pytest.raises(TypeError):
        expr()


def test_expr_format_and_p():
    expr = (field_age - 18) / 100
    assert expr.compile() == (format(expr), expr.p())
