from functools import wraps
from threading import Thread


def run_in_thread(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        thread = Thread(target=function, args=args, kwargs=kwargs, daemon=True)
        thread.start()
        return thread

    return wrapper


def run_in_thread2(**arguments):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            thread = Thread(target=function, args=args, kwargs=kwargs, daemon=True)
            thread.start()
            return thread

        return wrapper

    return decorator
