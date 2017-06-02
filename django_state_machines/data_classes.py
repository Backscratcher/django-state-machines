# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from .helpers import make_list

from six import string_types


class State(object):
    """
    Atomic class for transition class.
    """
    def __init__(self, name, id=None, value=None):
        """
        :param name: name of the state
        :param id: integer or string basing on field
        :param value: display name of the state
        :type name: string
        :type id: integer or string
        :type value: string
        """
        self.name = name
        self.id = id
        self.value = value

    def __eq__(self, other):
        if isinstance(other, string_types):
            return self.name == other
        elif isinstance(other, State):
            return self.name == other.name

    def __str__(self):
        return self.name
    __unicode__ = __str__

    def __repr__(self):
        return "<{0}: '{1}'>".format(self.__class__.__name__, self.name)


class Transition(object):
    """
    Atomic class for handler, holds data about transition.
    """
    def __init__(self, trigger, start_state, end_state, before=None, after=None):
        """
        :param trigger: function that triggers instance state change
        :param start_state: name of a start state
        :param end_state: name of a end state
        :param before: methods that should be fired before trigger function
        :param after: methods that should be fired after trigger function
        :type trigger: string or handler method
        :type start_state: string
        :type end_state: string
        :type before: single method, function or list of function, methods
        :type after: single method, function or list of function, methods
        """
        self.trigger = trigger
        self.start_state = start_state
        self.end_state = end_state
        self.before = make_list(before) if before else []
        self.after = make_list(after) if after else []

    def __str__(self):
        return "From '{0}' -> '{1}', trigger: {2}".format(self.start_state or '*', self.end_state, self.trigger)
    __unicode__ = __str__

    def __repr__(self):
        return "<{0}: From '{1}' -> '{2}'>".format(self.__class__.__name__, self.start_state or '*', self.end_state)
