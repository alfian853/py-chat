from handlers import AbstractHandler


# anggap seperti controller
class CoreHandler(AbstractHandler):

    instance = None

    @staticmethod
    def get_instance():
        if CoreHandler.instance is None:
            CoreHandler.instance = CoreHandler()
        return CoreHandler.instance

    def handle(self, request):
        print('chat handler')
        print(request)
        pass
