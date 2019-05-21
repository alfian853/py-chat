import uuid

from repositories import UserRepository
from session import Session, SessionManager


class FileService:
    instance = None

    @staticmethod
    def get_instance():
        if FileService.instance is None:
            FileService.instance = FileService()
        return FileService.instance

    def __init__(self):
        self.user_repository = UserRepository.get_instance()

    def handle_request(self, session: Session, request, sub_commands: str):
        commands = sub_commands.split('-')

        if commands[0] == 'PRIVATE':
            if commands[1] == 'SEND':
                self._handle_send_file(session, request)
        elif commands[0] == 'GROUP':
            pass

    def _handle_send_file(self, session: Session, request):

        p_user = self.user_repository.find_by_username(request['p_username'])

        if p_user is None:
            session.send_response({
                'FOR': 'FILE-PRIVATE-SEND',
                'status': 'rejected',
                'message': 'user not exist'
            })
            return

        session.send_response({
            'FOR': 'FILE-PRIVATE-SEND',
            'status': 'ready'
        })

        unique_code = str(uuid.uuid4())[1:5]
        file_path = 'storage/'+unique_code + '-' + request['file_name']
        fd = open(file_path, 'wb+', 0)

        max_size = request['file_size']
        received = 0

        conn = session.connection
        while received < max_size:
            data = conn.recv(1024)
            print('receive data')
            received += len(data)
            fd.write(data)

        fd.close()
        print('complete receive')
        message = {
            'file_id': unique_code,
            'file_path': file_path,
            'text': '[' + request['file_name'] + '], file_code: ' + unique_code,
            'from_user': session.user.username
        }

        p_user.add_to_inbox(session.user.username, message)
        session.user.add_to_inbox(p_user.username, message)
        self.user_repository.save(p_user)
        self.user_repository.save(session.user)

        message['FOR'] = 'NOTIF'
        target_session: Session = SessionManager.get_by_username(p_user.username)
        if target_session is not None:
            target_session.send_response(message)

        session.send_response(message)

