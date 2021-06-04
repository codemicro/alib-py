import copy
import threading
import time
from dataclasses import dataclass
from datetime import timedelta, datetime
from typing import Hashable, Any, Dict, Union, Tuple

DEFAULT_EXPIRATION = timedelta()
NO_EXPIRATION = timedelta(seconds=-1)


@dataclass
class _CacheValue:
    expiration_time: Union[datetime, None]
    value: Any


def _is_hashable(x: Any) -> bool:
    try:
        hash(x)
        return True
    except:
        return False


class Cache:
    _store: Dict[Hashable, _CacheValue]
    _lock: threading.Lock
    _default_expiration_time: timedelta
    _cleanup_interval: timedelta
    make_copy: bool

    def __init__(
        self,
        default_expiration_time: timedelta = timedelta(minutes=5),
        cleanup_interval: timedelta = timedelta(minutes=10),
    ):
        self._store = {}
        self._default_expiration_time = default_expiration_time
        self._lock = threading.Lock()
        self._cleanup_interval = cleanup_interval
        self.make_copy = False

        threading.Thread(target=self._cleanup_thread, daemon=True).start()

    def _cleanup_thread(self):
        while True:
            time.sleep(self._cleanup_interval.seconds)

            self._lock.acquire()

            now = datetime.utcnow()
            to_delete = []

            for key in self._store:
                val = self._store[key]
                if val.expiration_time is not None:
                    if val.expiration_time < now:
                        to_delete.append(key)

            for item in to_delete:
                self._delete(item)

            self._lock.release()

    def set(
        self,
        key: Hashable,
        value: Any,
        time_until_expiration: timedelta = DEFAULT_EXPIRATION,
    ):

        if not _is_hashable(key):
            raise ValueError("key must be hashable")

        expiration_time = None
        if time_until_expiration == DEFAULT_EXPIRATION:
            expiration_time = datetime.utcnow() + self._default_expiration_time
        elif time_until_expiration is not NO_EXPIRATION:

            if time_until_expiration < NO_EXPIRATION:
                raise ValueError("expiration timedelta cannot be negative")

            expiration_time = datetime.utcnow() + time_until_expiration

        if self.make_copy:
            value = copy.copy(value)

        self._lock.acquire()
        self._store[key] = _CacheValue(expiration_time, value)
        self._lock.release()

    def get(self, key: Hashable) -> Tuple[Any, bool]:

        if not _is_hashable(key):
            raise ValueError("key must be hashable")

        self._lock.acquire()
        try:
            val = self._store[key]
        except KeyError:
            self._lock.release()
            return None, False
        self._lock.release()

        if val.expiration_time is not None and val.expiration_time < datetime.utcnow():
            self.delete(key)
            return None, False

        return val.value, True

    def _delete(self, key: Hashable):
        try:
            del self._store[key]
        except KeyError:
            pass

    def delete(self, key: Hashable):

        if not _is_hashable(key):
            raise ValueError("key must be hashable")

        self._lock.acquire()
        self._delete(key)
        self._lock.release()

    def erase(self):
        self._lock.acquire()
        self._store = {}
        self._lock.release()
