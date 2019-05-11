from handlers import AbstractHandler


# anggap seperti controller
class CoreHandler(AbstractHandler):

    def handle(self, request):
        print('chat handler')
        print(request)
        pass
