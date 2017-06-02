Django finite state machine implementation
============================================

New approach to the finite state machines, the idea is to avoid declaring
machine logic on models, instead, create machines.py file in your app and
define your example state handler:

.. code:: python
    
    from django_state_machines.logic import BaseStateHandler
    
    class TestHandler(BaseStateHandler):
        def accept(self, **kwargs):
            pass

        def reject(self, **kwargs):
            print('reject')

        def add_transitions(self):
            self.add_transition(trigger='accept', start_state='notaccepted', end_state='accepted')
            self.add_transition(trigger='reject', start_state='notaccepted', end_state='rejected')

and for the model:

.. code:: python
    
    from django_state_machines.fields import StateMachineCharField
    from test_app.machines import TestHandler


    class Test(models.Model):
        state = StateMachineCharField(
            max_length=50,
            handler=TestHandler,
            state_choices=(
                ('accepted', 'Accepted state', 'accepted'),
                ('notaccepted', 'Not accepted state', 'notaccepted'),
                ('rejected', 'Rejected state', 'rejected'),

            ))

Installation
------------

.. code:: bash

    $ pip install django-state-machines

