from functools import wraps
from time import sleep
from trakt.errors import RateLimitException

from plex_trakt_sync.logging import logging


def rate_limit(retries=5):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            retry = 0
            while True:
                try:
                    return fn(*args, **kwargs)
                except RateLimitException as e:
                    if retry == retries:
                        raise e

                    delay = int(e.response.headers.get("Retry-After", 1))
                    logging.warning('RateLimitException, retrying after {} seconds'.format(delay))
                    sleep(delay)
                    retry += 1

        return wrapper

    return decorator
