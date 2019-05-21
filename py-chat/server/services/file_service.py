import json
import os
import uuid

from entities import FileEntity, GroupEntity
from repositories import UserRepository, FileRepository, GroupRepository
from session import Session, SessionManager


class FileService:
    instance = None

    @staticmethod
    def get_instance():
        if FileService.instance is None:
            FileService.instance = FileService()
        return FileService.instance

    def __init__(self):
        self.group_repository = GroupRepository.get_instance()
        self.user_repository = UserRepository.get_instance()
        self.file_repository = FileRepository.get_instance()

    def handle_request(self, session: Session, request, sub_commands: str):
        commands = sub_commands.split('-')

        if commands[0] == 'PRIVATE':
            if commands[1] == 'SEND':
                self._handle_private_send_file(session, request)
            elif commands[1] == 'GET':
                self._handle_get_file(session, request)

        elif commands[0] == 'GROUP':
            if commands[1] == 'SEND':
                self._handle_group_send_file(session, request)
            elif commands[1] == 'GET':
                self._handle_get_file(session, request)

    def _handle_group_send_file(self, session: Session, request):
        group_entity: GroupEntity = self.group_repository.find_by_id(request['group_id'])

        if session.user.username in group_entity.members:
            pass
        else:
            session.send_response({
                'FOR': 'FILE-GROUP-SEND',
                'status': 'failed',
                'message': 'You are not a member of the group!'
            })
            return

        session.send_response({
            'FOR': 'FILE-GROUP-SEND',
            'status': 'ready'
        })

        file_entity: FileEntity = self._handle_send_file(session, request)

        message = {
            'text': '[' + request['file_name'] + '], file_code: ' + file_entity.file_code,
            'from_user': session.user.username
        }

        group_entity.inbox.append(message)
        self.group_repository.save(group_entity)

        message['FOR'] = 'NOTIF'
        message['from_group'] = group_entity.group_name

        members = group_entity.members
        for member in members:
            if member == session.user.username:
                continue
            member_session: Session = SessionManager.get_by_username(member)
            if member_session is not None:
                member_session.send_response(message)
                print('send to ' + member_session.user.username)

        session.send_response({
            'FOR': 'MSG-GROUP-SEND',
            'status': 'success'
        })

    def _handle_private_send_file(self, session: Session, request):
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

        file_entity: FileEntity = self._handle_send_file(session, request)

        message = {
            'text': '[' + request['file_name'] + '], file_code: ' + file_entity.file_code,
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

    def _handle_send_file(self, session: Session, request: dict) -> FileEntity:

        unique_code = str(uuid.uuid4())[1:7]
        file_path = 'storage/' + unique_code + '-' + request['file_name']
        fd = open(file_path, 'wb+', 0)

        max_size = request['file_size']
        received = 0

        conn = session.connection
        while received < max_size:
            data = conn.recv(1024)
            print('receive')
            received += len(data)
            fd.write(data)

        fd.close()

        file_entity = FileEntity()
        file_entity.owner = session.user.username
        file_entity.file_path = file_path
        file_entity.file_code = unique_code

        self.file_repository.save(file_entity)
        return file_entity

    def _handle_get_file(self, session: Session, request):

        file_entity = self.file_repository.find_by_file_code(request['file_code'])

        if file_entity is None or not os.path.exists(file_entity.file_path):
            session.send_response({
                'FOR': request['command'],
                'status': 'failed',
                'message': 'file not found!'
            })
        else:
            file_name = file_entity.file_path.split('/')[1]
            file_path = file_entity.file_path
            fd = open(file_path, 'rb')
            session.send_response({
                'FOR': request['COMMAND'],
                'status': 'success',
                'file_name': file_name,
                'file_size': os.path.getsize(file_path)
            })

            resp = json.loads(session.connection.recv(1024).decode('utf-8'))

            if resp['status'] == 'ready':
                for data in fd:
                    session.connection.sendall(data)

                fd.close()
