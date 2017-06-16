from django_state_machines.logic import BaseStateHandler


class ProductHandler(BaseStateHandler):
    def accept(self, **kwargs):
        pass

    def reject(self, **kwargs):
        pass

    def add_transitions(self):
        self.add_transition(trigger='accept', start_state='not_accepted', end_state='accepted')
        self.add_transition(trigger='reject', start_state='not_accepted', end_state='rejected')
