from __future__ import annotations

from typing import Any, List, Optional, Tuple

from .field import Field


class ExprMixin:
    def __lt__(self, other):
        """
        self < other
        """
        return CompareExpr(self, "<", other)

    def __le__(self, other):
        """
        self <= other
        """
        return CompareExpr(self, "<=", other)

    def __eq__(self, other):
        """
        self == other
        """
        return CompareExpr(self, "==", other)

    def __ne__(self, other):
        """
        self != other
        """
        return CompareExpr(self, "!=", other)

    def __gt__(self, other):
        """
        self > other
        """
        return CompareExpr(self, ">", other)

    def __ge__(self, other):
        """
        self >= other
        """
        return CompareExpr(self, ">=", other)

    def __add__(self, other):
        """
        self + other
        """
        return ArithmeticExpr(self, "+", other)

    def __radd__(self, other):
        """
        other + self
        """
        return ArithmeticExpr(other, "+", self)

    def __sub__(self, other):
        """
        self - other
        """
        return ArithmeticExpr(self, "-", other)

    def __rsub__(self, other):
        """
        other - self
        """
        return ArithmeticExpr(other, "-", self)

    def __mul__(self, other):
        """
        self * other
        """
        return ArithmeticExpr(self, "*", other)

    def __rmul__(self, other):
        """
        other * self
        """
        return ArithmeticExpr(other, "*", self)

    def __truediv__(self, other):
        """
        self / other
        """
        return ArithmeticExpr(self, "/", other)

    def __rtruediv__(self, other):
        """
        other / self
        """
        return ArithmeticExpr(other, "/", self)

    def __mod__(self, other):
        """
        self % other
        """
        return ArithmeticExpr(self, "%", other)

    def __rmod__(self, other):
        """
        other % self
        """
        return ArithmeticExpr(other, "%", self)

    def isin(self, *values: Any):
        """
        SQL: IN (value0, value1, ...)
        """
        return CompareExpr(self, "IN", *values)

    def between(self, start: Any, end: Any):
        """
        SQL: BETWEEN start AND end
        """
        return CompareExpr(self, "BETWEEN", start, end)

    def isnull(self):
        """
        SQL: IS NULL
        """
        return CompareExpr(self, "ISNULL")


class ExprForStringMixin:
    def like(self, pattern: str):
        """
        SQL: LIKE pattern
        """
        return CompareExpr(self, "LIKE", pattern)


def compile_value(value: Any, placeholder: str = "?") -> Tuple[str, List[Any]]:
    if isinstance(value, (int, float)):
        return str(value), []
    elif hasattr(value, "field_name"):
        return f'"{value.field_name}"', []
    elif isinstance(value, Expr):
        return value.compile()
    else:
        return placeholder, [value]


class Expr:
    def compile(self, placeholder: str = "?") -> Tuple[str, List[Any]]:
        raise NotImplementedError

    def __format__(self, __format_spec: str) -> str:
        return self.compile(__format_spec)[0]

    def parameters(self) -> List[Any]:
        return self.compile()[1]

    p = parameters  # shortcut

    def __invert__(self) -> NotExpr:
        """
        ~self
        """
        if isinstance(self, NotExpr):
            return self.expr
        else:
            return NotExpr(self)

    def __and__(self, other):
        """
        self & other
        """
        if not isinstance(other, Expr):
            return NotImplemented
        return ExprCombine("AND", self, other)

    def __rand__(self, other):
        """
        other & self
        """
        if not isinstance(other, Expr):
            return NotImplemented
        return ExprCombine("AND", other, self)

    def __or__(self, other):
        """
        self | other
        """
        if not isinstance(other, Expr):
            return NotImplemented
        return ExprCombine("OR", self, other)

    def __ror__(self, other):
        """
        other | self
        """
        if not isinstance(other, Expr):
            return NotImplemented
        return ExprCombine("OR", other, self)


class NotExpr(Expr):
    def __init__(self, expr):
        self.expr = expr

    def compile(self, placeholder="?"):
        sql_format, paramaters = self.expr.compile(placeholder=placeholder)
        return "NOT ({})".format(sql_format), paramaters


class ExprCombine(Expr):
    def __init__(self, operator, left, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return "ExprCombine({}, {}, {})".format(
            repr(self.operator), repr(self.left), repr(self.right)
        )

    def compile(self, placeholder="?"):
        sql_formats = []
        parameters = []
        for expr in [self.left, self.right]:
            s, p = expr.compile(placeholder=placeholder)
            parameters.extend(p)
            sql_formats.append("(" + s + ")")
        return (
            "(" + " {} ".format(self.operator).join(sql_formats) + ")",
            parameters,
        )


class CompareExpr(Expr):
    format_mapping = {
        ">=": "{} >= {}",
        "<=": "{} <= {}",
        ">": "{} > {}",
        "<": "{} < {}",
        "==": "{} = {}",
        "!=": "{} <> {}",
        "LIKE": "{} LIKE {}",
        "BETWEEN": "{} BETWEEN {} AND {}",
        "IN": "{} IN ({})",
        "ISNULL": "{} IS NULL",
    }

    def __init__(self, field, operator, *args):
        self.field = field
        self.operator = operator
        self.args = args

    def __repr__(self):
        return "Expr({}, {}, *{})".format(
            repr(self.field), repr(self.operator), repr(self.args)
        )

    def compile(self, placeholder="?"):
        field_format, field_paramaters = compile_value(self.field, placeholder)
        args_format, args_paramaters = [], []
        for arg in self.args:
            arg_format, arg_paramaters = compile_value(arg, placeholder=placeholder)
            args_format.append(arg_format)
            args_paramaters.extend(arg_paramaters)
        if self.operator == "IN":
            args_format = [", ".join(map(str, args_format))]
        return (
            self.format_mapping[self.operator].format(field_format, *args_format),
            field_paramaters + args_paramaters,
        )


class ArithmeticExpr(ExprMixin, Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return "ArithmeticExpr({}, {}, {})".format(
            repr(self.left), repr(self.operator), repr(self.right)
        )

    def compile(self, placeholder="?"):
        left_format, left_paramaters = compile_value(self.left, placeholder)
        right_format, right_paramaters = compile_value(self.right, placeholder)
        return (
            "{} {} {}".format(left_format, self.operator, right_format),
            left_paramaters + right_paramaters,
        )


class _CaseEnd(Expr):
    def __init__(
        self, field: Optional[Field], cases: list[tuple[Any, Any]], default: Any
    ) -> None:
        self._field = field
        self._cases = cases
        self._default = default

    def compile(self, placeholder="?"):
        sql_formats = []
        case_formats = []
        parameters = []
        for case in self._cases:
            st = []
            for i in case:
                if isinstance(i, Expr):
                    s, p = i.compile(placeholder=placeholder)
                    parameters.extend(p)
                    st.append(s)
                else:
                    s, p = compile_value(i, placeholder=placeholder)
                    parameters.extend(p)
                    st.append(s)
            case_formats.append("WHEN {} THEN {}".format(*st))
        sql_formats.append(" ".join(case_formats))

        if self._default is not None:
            s, p = compile_value(self._default)
            sql_formats.append("ELSE {}".format(s))
            parameters.extend(p)

        if self._field is not None:
            return (
                "CASE {} {} END".format(f'"{self._field}"', " ".join(sql_formats)),
                parameters,
            )
        else:
            return "CASE {} END".format(" ".join(sql_formats)), parameters


class Case(_CaseEnd):
    def __init__(self, field: Optional[Field] = None) -> None:
        super().__init__(field, [], None)

    def when(self, condition: Any, value: Any) -> Case:
        self._cases.append((condition, value))
        return self

    def else_(self, value: Any) -> _CaseEnd:
        self.default = value
        return _CaseEnd(self._field, self._cases, self.default)
