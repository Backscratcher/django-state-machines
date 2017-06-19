# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from .data_classes import State, Transition
from .decorators import provide_method_name
from .exceptions import TransitionNotPossibleError, WrongTriggerTypeError
from .state_map import StateMachineMap

from collections import defaultdict
from six import string_types


class StateCache(object):
    """
    StateCache class works as a State factory and cache, at the given
    handler_key which is generated automatically at the init of a handler
    and by state_name you retrieve the state you want.

    The `type` parameter indicates the type of a field, if there are no
    kwargs provided for state initialization then StateCache inserts
    values basing on `type`.
    If the type is `int` then it will try to insert item with id + 1,
    If the type is `str` then it will try to insert item with state_name key

    Example:
    defaultdict(dict, {
        'TestHandler_state': {
            'accepted': <State: 'accepted'>,
            'notaccepted': <State: 'notaccepted'>,
            'rejected': <State: 'rejected'>
        }
    })
    """
    _state_objects = defaultdict(dict)

    @classmethod
    def get_state(cls, handler_key, state_name, field_type=None, **kwargs):
        """
        Create or get a state basing on the `handler_key` and `state_name`.
        If kwargs are not provided then generate auto values.
        """
        if state_name in cls._state_objects[handler_key].keys():
            return cls._state_objects[handler_key][state_name]
        if not kwargs and field_type:
            state = cls._create_auto_values(handler_key, state_name, field_type)
        else:
            state = State(state_name, **kwargs)
        cls._state_objects[handler_key][state_name] = state
        return state

    @classmethod
    def _create_auto_values(cls, handler_key, state_name, field_type):
        """
        This method automatically creates dummy state values if only
        transitions are provided for handler.
        """
        if field_type == 'int':
            states = cls._state_objects[handler_key].values()
            ids = sorted(state.id for state in states) or [1]
            id = ids[-1]
            value = state_name.lower().title()
            return State(state_name, id=id, value=value)
        elif field_type == 'str':
            value = state_name.lower().title()
            return State(state_name, id=state_name, value=value)


class TransitionProcessMixin(object):
    def process(self, transition, **kwargs):
        """
        Transition processing starts with checking if transition can be made:
        1) if no - exception `TransitionNotPossibleError` is raised.
        2) if yes - then:
            - kwargs parameter will be passed to every method in steps below.
            - every function in transition `before` is called.
            - handler `trigger` is called.
            - handler updates instance state value.
            - every function in transition `after` is called.
        """
        if not self.can_make_transition(transition):
            raise TransitionNotPossibleError("Can't make transition from '{0}' to '{1}', instance value: '{2}'".format(
                transition.start_state, transition.end_state, self.get_instance_field_value()
            ))
        self._call_before(transition, **kwargs)
        self._call_trigger(transition, **kwargs)
        self.update_state(transition)
        self._call_after(transition, **kwargs)

    def _call_before(self, transition, **kwargs):
        """
        Call every function in `before` attribute. Kwargs are
        provided from `process` method.
        """
        for before_function in transition.before:
            before_function(**kwargs)

    def _call_trigger(self, transition, **kwargs):
        """
        Call trigger function from handler class. Because of the
        nature of implementation of handler classes, the trigger
        function in the runtime is prefixed with '_'. Kwargs are
        provided from `process` method.
        """
        trigger_name = transition.trigger.__name__
        handler_trigger = getattr(self, '_' + trigger_name)
        handler_trigger(**kwargs)

    def _call_after(self, transition, **kwargs):
        """
        Call every function in `after` attribute. Kwargs are
        provided from `process` method.
        """
        for after_function in transition.after:
            after_function(**kwargs)

    def can_make_transition(self, transition):
        """
        Check if instance qualifies for transition. It checks instance value
        and compares it with transition start state.

        :return: True or False
        """
        if transition.start_state == '*':
            pass

        if self.get_instance_field_value() == transition.start_state.id:
            return True
        return False

    def update_state(self, transition):
        setattr(self.instance, self.field_name, transition.end_state.id)


class TransitionAddingMixin(object):
    def add_transitions(self):
        """
        After subclassing `BaseStateHandler` override this method to add transitions for example it could look
        like this:
            def add_transitions(self):
                self.add_transition('accept', 'initial', 'accepted')
                self.add_transition('reject', 'initial', 'rejected')
        """

    def add_transition(self, trigger, start_state, end_state, before=None, after=None):
        """
        General method for adding transitions to your handler, first it checks if the name
        exists in already defined methods, if yes, throw an error, if not, proceed to
        creating states and transition, map transition to `self.states_map` then create and
        assign a template function for this trigger.
        Template function will take the place of the current trigger function, when the one implemented
        on the handler will be moved to the name with underscore.
        """
        handler_method = self._check_trigger(trigger)
        start_state = StateCache.get_state(self.handler_key, start_state, field_type=self.field_type)
        end_state = StateCache.get_state(self.handler_key, end_state, field_type=self.field_type)
        transition = Transition(handler_method, start_state, end_state, before, after)
        self.states_map.add_transition(transition)

        def add_trigger(self, method, **kwargs):
            transition = self.states_map.transitions[method]
            kwargs['instance'] = self.instance
            self.process(transition, **kwargs)
        add_trigger.__name__ = handler_method.__name__

        setattr(self.__class__, "_" + trigger, handler_method)
        setattr(self.__class__, trigger, provide_method_name(add_trigger))

    def _check_trigger(self, trigger):
        """
        Checks whether the provided trigger is a method on a handler, if it exists and is a callable.
        trigger: can be a callable or a string that refers to a method implemented on handler
        """
        if isinstance(trigger, string_types):
            if hasattr(self.__class__, trigger) and callable(getattr(self.__class__, trigger)):
                return getattr(self.__class__, trigger)
        elif callable(getattr(self.__class__, trigger.__name__)):
            return trigger
        raise WrongTriggerTypeError("Provided {0} trigger is not a string or a callable".format(trigger))


class BaseStateHandler(TransitionProcessMixin, TransitionAddingMixin):
    def __init__(self, field_name, field_type, **kwargs):
        self.field_name = field_name
        self.field_type = field_type
        self.handler_key = "{0}_{1}".format(self.__class__, field_name)
        self.states_map = StateMachineMap()
        self.state_choices = kwargs.get('state_choices', [])
        self.instance = None
        if self.state_choices:
            self._init_state_choices()
        self.add_transitions()

    def _init_state_choices(self):
        for state_values_row in self.state_choices:
            id, value, name = state_values_row
            state = StateCache.get_state(self.handler_key, name, id=id, value=value)
            self.states_map.add_state(state)

    def get_instance_field_value(self):
        """Get value of a instance field value"""
        return getattr(self.instance, self.field_name)

    @property
    def choices(self):
        choices = []
        for node in self.states_map.machine_map.values():
            choices.append((node.state.id, node.state.value))
        return choices
