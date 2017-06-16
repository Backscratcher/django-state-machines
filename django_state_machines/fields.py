# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from .decorators import provide_method_name

import copy


class StateMachineMixin(object):
    def __init__(self, handler, *args, **kwargs):
        self.state_choices = kwargs.pop('state_choices', None)

        if self.state_choices:
            choices = []
            for id, value, state_helper_name in self.state_choices:
                choices.append((id, value))
            kwargs['choices'] = choices

        super(StateMachineMixin, self).__init__(*args, **kwargs)
        self.handler_class = handler

    def deconstruct(self):
        name, path, args, kwargs = super(StateMachineMixin, self).deconstruct()
        kwargs['handler'] = self.handler_class
        return name, path, args, kwargs

    def contribute_to_class(self, cls, name, **kwargs):
        super(StateMachineMixin, self).contribute_to_class(cls, name, **kwargs)
        field_type = self._get_field_type(cls)
        self.handler = self.handler_class(name, field_type, state_choices=self.state_choices)
        if not self.choices:
            self.choices = self.handler.choices

        def property_handler(self, method, instance):
            handler_name = '_{0}'.format(method)
            if handler_name not in self.__dict__:
                field_name, rest = method.split('_')
                field = self._meta.get_field(field_name)
                handler_copy = copy.deepcopy(field.handler)
                handler_copy.instance = instance
                self.__dict__[handler_name] = handler_copy
            return self.__dict__[handler_name]
        property_handler.name = "{0}_handler".format(self.handler.field_name)

        setattr(cls, "{0}_handler".format(self.handler.field_name), property(provide_method_name(property_handler, provide_instance=True)))

    def _get_field_type(self, cls):
        if isinstance(cls, models.IntegerField):
            return 'int'
        elif isinstance(cls, models.CharField):
            return 'str'


class StateMachineIntegerField(StateMachineMixin, models.IntegerField):
    pass


class StateMachineCharField(StateMachineMixin, models.CharField):
    pass
