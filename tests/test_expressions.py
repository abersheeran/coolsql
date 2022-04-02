import pytest

from coolsql import Field, Case


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
    ],
)
def test_expr(expr, sql, parameters):
    assert expr.compile() == (sql, parameters)
