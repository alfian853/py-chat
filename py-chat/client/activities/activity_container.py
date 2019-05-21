import json
import threading
import traceback

from activities.abstract_activity import AbstractActivity


class ActivityContainer(threading.Thread):
    def __init__(self, default_activity: AbstractActivity):
        self.activity = default_activity
        self.activity.set_container(self)
        threading.Thread.__init__(self)
        self.start()

    def set_activity(self, activity: AbstractActivity):
        self.activity = activity

    def run_activity(self):
        print(self.activity.__class__)
        commands = input(self.activity.get_activity_input_line()+'\n')
        self.activity.handle_input(commands)

    def run(self):
        while True:
            recv = self.activity.get_connection().recv(1024).decode('utf-8')
            try:
                json_resp = json.loads(recv)
                self.activity.response_handler(json_resp, True)

            except Exception as e:
                traceback.print_exc()
                self.activity.response_handler(recv, False)

