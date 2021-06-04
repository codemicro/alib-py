# cache

cache is a Python clone of [go-cache](https://github.com/patrickmn/go-cache). It's an in-memory key-value data store with per-key expiration times (or none, if you'd rather) suitable for applications running on a single machine. It's thread-safe, too!

## Usage

```python
from datetime import timedelta
import alib.cache as cache

# Creates a cache with a default expiration time of 5 minutes that cleans old entries once every 10 minutes
c = cache.Cache()

# You can set custom values for these too
c = cache.Cache(
    default_expiration_time=timedelta(minute=5),
    cleanup_interval=timedelta(minutes=10),
)

# Store a value with the key "myThing" using the default expiration time
# Any value can be stored and any value that can be hashed can be used as a key
c.set("myThing", "hello world!")

# You can store a value a custom amount of time
c.set("myOtherThing", 12345, time_until_expiration=timedelta(minutes=15))

# Or for an unlimited amount of time!
c.set("myOtherThing", 12345, time_until_expiration=cache.NO_EXPIRATION)

# Values are retrieved by their key
value, found = c.get("myThing")
if found:
    print(value)  # -> "hello world!"

# Values can also be manually deleted prior to their automatic removal
c.delete("foo")
```

## A note about references

If a mutable value is stored in a cache using `c.set`, any change made to the value returned by `c.get` for that item **will also change the value stored in cache**. In order to prevent this, a copy of your data needs to be made either before storing or after retrieving this value from the cache. 

Setting `c.make_copy = True` will copy every value when inserting a value into the cache using `copy.copy()`. While this fixes the problem outlined above, it can come with a performance penalty.