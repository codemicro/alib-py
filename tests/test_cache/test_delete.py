import pytest

from alib.cache import *
from alib.cache.cache import _CacheValue

key = "hello"
value = 1234567


@pytest.fixture()
def c():
    x = Cache()
    x._store[key] = _CacheValue(None, value)
    yield x
    del x


def test_unhashable_key(c):
    with pytest.raises(ValueError):
        c.delete({})


def test_delete(c):
    c.delete(key)
    with pytest.raises(KeyError):
        _ = c._store[key]
