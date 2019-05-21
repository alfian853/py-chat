from session import Session


class AbstractHandler(object):

    def __init__(self):
        self.next_handler = None

    def set_next_handler(self, handler):
        self.next_handler = handler

    def handle(self, session: Session, request):
        """
        :param session:
        :param dict request:
        """
        if self.next_handler is not None:
            self.next_handler.handle(session, request)
