import datetime

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



def test_get(c):
    x, found = c.get(key)
    assert found
    assert x == value


def test_get_expired(c):
    c._store[key] = _CacheValue(
        datetime.datetime.utcnow() - datetime.timedelta(minutes=5), value
    )
    x, found = c.get(key)
    assert not found
    assert x is None


def test_unhashable_key(c):
    with pytest.raises(ValueError):
        c.get({})
