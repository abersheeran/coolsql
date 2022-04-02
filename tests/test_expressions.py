import pytest

from coolsql import Case, Field

field_name = Field("name")
field_age = Field("age")


@pytest.mark.parametrize(
    "expr,sql,parameters",
    [
        (field_age.between(18, 24), '"age" BETWEEN 18 AND 24', []),
        (field_name.like("%a%"), '"name" LIKE ?', ["%a%"]),
        (field_name.isnull(), '"name" IS NULL', []),
        (
            field_name.isnull() & field_age.between(18, 24),
            '(("name" IS NULL) AND ("age" BETWEEN 18 AND 24))',
            [],
        ),
        (
            Case().when(1, 0).else_(1),
            "CASE WHEN 1 THEN 0 ELSE 1 END",
            [],
        ),
    ],
)
def test_expr(expr, sql, parameters):
    assert expr.compile() == (sql, parameters)
