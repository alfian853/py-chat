from handlers import AbstractHandler


# untuk auth user sebelum masuk ke core service
class AuthHandler(AbstractHandler):

    def handle(self, request):
        print('auth handle')
        print(request)
        super(AuthHandler, self).handle(request)
        pass
