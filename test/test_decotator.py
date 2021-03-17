from typing import Callable


def add_return_parma(func: Callable):
    def wrapper(*args, **kwargs):
        return (func(*args), func.__name__)
    return wrapper


@add_return_parma
def now():
    print("now")


qwe = now()
print(qwe)
