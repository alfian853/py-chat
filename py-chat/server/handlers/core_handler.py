import traceback

from handlers import AbstractHandler
from services import *


# anggap seperti controller
from session import Session


class CoreHandler(AbstractHandler):

    instance = None

    @staticmethod
    def get_instance():
        if CoreHandler.instance is None:
            CoreHandler.instance = CoreHandler()
        return CoreHandler.instance

    def __init__(self):
        super().__init__()
        self.services = {
            'CONTACT': ContactService(),
            'GROUP': GroupService(),
            'MSG': ChatService(),
            'FILE': FileService()
        }

    def handle(self, session: Session, request):
        commands: str = request['COMMAND'].split('-', 1)
        # request['COMMAND'] = '-'.join(commands[1:])
        try:
            self.services[commands[0]].handle_request(session, request, commands[1])
        except Exception as e:
            traceback.print_exc()
