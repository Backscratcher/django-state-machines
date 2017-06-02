# -*- coding: utf-8 -*-

from __future__ import unicode_literals


def make_list(value):
    return value if isinstance(value, (list, tuple)) else [value]
