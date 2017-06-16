from django.db import models
from django_state_machines.fields import StateMachineCharField

from .machines import ProductHandler


class Product(models.Model):
    state = StateMachineCharField(
        max_length=50,
        handler=ProductHandler,
        default='not_accepted',
        state_choices=(
            ('accepted', 'Accepted state', 'accepted'),
            ('not_accepted', 'Not accepted state', 'not_accepted'),
            ('rejected', 'Rejected state', 'rejected'),
        )
    )
