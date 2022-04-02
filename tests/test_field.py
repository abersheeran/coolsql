import pytest

from coolsql import Field


def test_field():
    with pytest.raises(ValueError):
        Field("name' OR 1=1")

    assert format(Field("NaMe")) == '"NaMe"'
