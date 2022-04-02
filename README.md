# CoolSQL

[![PyPI](https://img.shields.io/pypi/v/coolsql?style=flat-square)](https://pypi.org/project/coolsql)

Makes it easier to write raw SQL in Python.

## Usage

### Quick Start

```python
from coolsql import Field

name = Field("name")

condition = name.isnull() & field_age.between(18, 24)
...
cursor.execute(f"SELECT * FROM table WHERE {condition}", condition.p())
...
```
