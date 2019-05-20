from activities.abstract_activity import AbstractActivity


class ActivityContainer(object):
    def __init__(self, default_activity: AbstractActivity):
        self.activity = default_activity
        self.activity.set_container(self)

    def set_activity(self, activity: AbstractActivity):
        self.activity = activity

    def run_activity(self):
        print(self.activity.__class__)
        commands = input(self.activity.get_activity_input_line())
        self.activity.handle_input(commands)

