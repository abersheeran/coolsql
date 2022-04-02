from .expressions import Case, ExprForStringMixin, ExprMixin
from .field import Field as BaseField

__all__ = [
    "Case",
    "Field",
]


class Field(BaseField, ExprMixin, ExprForStringMixin):
    """
    Example:

    ```python
    name = Field("name")

    condition = ~name.isnull() & name.like("%a%")
    sql = f"SELECT * FROM table WHERE {condition}"

    cursor.execute(sql, condition.p())
    ```
    """
