# CoolSQL

[![PyPI](https://img.shields.io/pypi/v/coolsql?style=flat-square)](https://pypi.org/project/coolsql)

Makes it easier to write raw SQL in Python.

## Usage

### Quick Start

```python
from coolsql import Field

score = Field("score")

condition = (score >= 60) & ((score * score / 100) >= 60)
...
cursor.execute(f"SELECT * FROM table WHERE {condition}", condition.p())
...
```

---

Documentation is in progress, you can start by looking at the test cases under [tests](https://github.com/abersheeran/coolsql/blob/master/tests/test_expressions.py).
