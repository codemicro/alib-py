import datetime

import pytest

from alib.cache import *


@pytest.fixture()
def c():
    c = Cache()
    yield c
    del c


def test_set_value(c):
    key = "hi"
    value = 1234567

    c.set(key, value)
    assert c._store[key].value == value


def test_no_expiration(c):
    key = "hi"

    c.set(key, 123, cache.NO_EXPIRATION)
    assert c._store[key].expiration_time is None


def test_unhashable_key(c):
    with pytest.raises(ValueError):
        c.set({}, "hi")


def test_negative_time(c):
    with pytest.raises(ValueError):
        c.set("hi", "thing", time_until_expiration=datetime.timedelta(seconds=-12))


def test_expiration(c):
    key = "hi"
    value = 123456
    expiration = datetime.timedelta(minutes=5)
    expires_at = datetime.datetime.utcnow() + expiration

    c.set(key, value, expiration)

    xv = c._store[key]

    # the range is to account for some delay between setting and checking the value that'd cause too big a difference to
    # be an exact match
    assert (
        expires_at <= xv.expiration_time < (expires_at + datetime.timedelta(seconds=1))
    )

def test_data_copy(c):
    key = "foo"
    val = ["bar"]
    c.set(key, val)
    xval, _ = c.get(key)
    assert val is xval

    c.make_copy = True

    c.set(key, val)
    xval, _ = c.get(key)
    assert val is not xval
