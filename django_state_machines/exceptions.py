# -*- coding: utf-8 -*-

from __future__ import unicode_literals


class WrongStateError(Exception):
    pass


class DuplicateTransitionTriggerError(Exception):
    pass


class NoSuchStateError(Exception):
    pass


class TransitionNotPossibleError(Exception):
    pass


class WrongTriggerTypeError(Exception):
    pass
