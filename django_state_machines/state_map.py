# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from .data_classes import State
from .exceptions import DuplicateTransitionTriggerError, NoSuchStateError

from six import string_types


class StateMapNode(object):
    """
    Atomic node class for `StateMachineMapDict` it holds informations about single state and
    where you can proceed: to which states and with which transitions and from which states and
    with which transitions you can get to this state.
    """
    def __init__(self, state):
        self.state = state
        self.allowed_transitions = []
        self.allowed_states = []
        self.from_transitions = []
        self.from_states = []

    def __repr__(self):
        return "<Node {0}: allowed_states={1}, allowed_transitions={2}, from_states={3}, from_transitions={4}>".format(
            self.state, self.allowed_states, self.allowed_transitions, self.from_states, self.from_transitions)


class StateMachineMapDict(dict):
    """ Dictionary that holds objects of `StateMapNode`."""
    def alter_key(self, key):
        if isinstance(key, State):
            return key.name
        return key

    def __getitem__(self, key):
        return super(StateMachineMapDict, self).__getitem__(self.alter_key(key))

    def __contains__(self, key):
        return super(StateMachineMapDict, self).__contains__(self.alter_key(key))


class StateMachineMap(object):
    """
    Instances of this class have two attributes:
     - Dictionary transitions, which serves as a fast hash-map for getting transitions.
     - Dictionary machine_map , which is a representation of a `StateMachineMapDict`.
    Purpose of this class is to hold whole structure of state machine and to give
    nice API to for example: get allowed states for some state value.
    """
    def __init__(self):
        self.transitions = {}
        self.machine_map = StateMachineMapDict()

    def _add_states(self, states):
        for state in states:
            self.machine_map[state.name] = StateMapNode(state)

    def _update_states(self, transition):
        transition_start = transition.start_state
        self.machine_map[transition_start.name].allowed_transitions.append(transition)
        self.machine_map[transition_start.name].allowed_states.append(transition.end_state)
        transition_end = transition.end_state
        self.machine_map[transition_end.name].from_transitions.append(transition)
        self.machine_map[transition_end.name].from_states.append(transition.start_state)

    def _map_transition(self, transition):
        states = []
        if transition.start_state not in self.machine_map.keys():
            states.append(transition.start_state)
        if transition.end_state not in self.machine_map.keys():
            states.append(transition.end_state)
        self._add_states(states)
        self._update_states(transition)

    def add_transition(self, transition):
        callback_name = transition.trigger if \
            isinstance(transition.trigger, string_types) else transition.trigger.__name__
        if callback_name in self.transitions.keys():
            raise DuplicateTransitionTriggerError(
                "Trigger with name '{0}' already exists.".format(callback_name))

        self.transitions[callback_name] = transition
        self._map_transition(transition)

    def add_state(self, state):
        if state not in self.machine_map.keys():
            self._add_states([state])

    def get_state_info(self, state):
        """
        Method returns `StateMapNode` of the provided state from `machine_map`.
        """
        try:
            return self.machine_map[state]
        except KeyError:
            raise NoSuchStateError("'{0}' state not found in map.".format(state))

    def get_states_info(self):
        return self.machine_map.values()
