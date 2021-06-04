import datetime
import time

import pytest

from alib.cache import *
from alib.cache.cache import _CacheValue


@pytest.fixture()
def c():
    c = Cache(cleanup_interval=datetime.timedelta(seconds=1))
    yield c
    del c


def test_cleanup(c):
    key = "hi"
    c._store[key] = _CacheValue(datetime.datetime.utcnow(), 12345)

    time.sleep(2)

    with pytest.raises(KeyError):
        _ = c._store[key]


def test_no_expiration(c):
    key = "hi"
    c._store[key] = _CacheValue(datetime.datetime.utcnow(), None)

    time.sleep(2)

    with pytest.raises(KeyError):
        _ = c._store[key]
