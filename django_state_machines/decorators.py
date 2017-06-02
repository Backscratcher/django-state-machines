# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from functools import wraps


def provide_method_name(func, provide_instance=False):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if provide_instance:
            kwargs['instance'] = args[0]
        kwargs['method'] = func.name if hasattr(func, 'name') else func.__name__
        return func(*args, **kwargs)
    return wrapper
