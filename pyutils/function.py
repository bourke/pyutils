import functools
from types import *

def apply_f(applied_f):
    def decorator(f):
        def _wrapped(*args, **kwargs):
            return applied_f(f(*args, **kwargs))
        if isinstance(f, (BuiltinMethodType, MethodType,
               BuiltinFunctionType, FunctionType)):
            return functools.wraps(f)(_wrapped)
        else:
            return _wrapped
    return decorator


def reverse_args(f):
    @functools.wraps(f)
    def _wrapped(*args):
        return f(*reversed(args))
    return _wrapped


s = [1, 2.4, 3, 5.234, 0]

print filter(functools.partial(reverse_args(isinstance), float), s)