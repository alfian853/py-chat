from entities import GroupEntity
from repositories import UserRepository, GroupRepository
from session import SessionManager, Session


class ChatService:
    instance = None

    @staticmethod
    def get_instance():
        if ChatService.instance is None:
            ChatService.instance = ChatService()
        return ChatService.instance

    def __init__(self):
        self.user_repository = UserRepository.get_instance()
        self.group_repository = GroupRepository.get_instance()

    def handle_request(self, session: Session, request, sub_commands: str):
        print(sub_commands)
        commands = sub_commands.split('-')

        if commands[0] == 'PRIVATE':
            if commands[1] == 'SEND':
                self._msg_private_send_handler(session, request)
            elif commands[1] == 'GET':
                self._msg_private_get_handler(session, request)
        elif commands[0] == 'GROUP':
            if commands[1] == 'SEND':
                self._msg_group_send_handler(session, request)
            elif commands[1] == 'GET':
                self._msg_group_get_handler(session, request)

    def _msg_private_get_handler(self, session: Session, request):
        session.send_response({
            'FOR': request['COMMAND'],
            'messages': self.user_repository.get_message_from(session.user.username, request['p_username'])
            # 'messages': session.user.get_inbox_from(request['p_username'])
        })

    def _msg_private_send_handler(self, session: Session, request):
        target_username = request['p_username']
        msg = request['message']

        target_session: Session = SessionManager.get_by_username(target_username)
        target_user = self.user_repository.find_by_username(target_username)

        if target_session is not None:
            target_session.send_response({
                'FOR': 'NOTIF',
                'from_user': session.user.username,
                'text': request['message']
            })

        if target_user is not None:
            session.send_response({
                'FOR': request['COMMAND'],
                'status': 'success'
            })
        else:
            session.send_response({
                'FOR': request['COMMAND'],
                'status': 'failed',
                'message': 'user not found'
            })

        if target_user is not None:
            message = dict()
            message['from_user'] = session.user.username
            message['text'] = request['message']

            # simpan message di 2 inbox
            session.user.add_to_inbox(target_user.username, message)
            self.user_repository.save(session.user)

            target_user.add_to_inbox(session.user.username, message)
            self.user_repository.save(target_user)

    def _msg_group_send_handler(self, session: Session, request):

        group_entity: GroupEntity = self.group_repository.find_by_id(request['group_id'])

        if session.user.username in group_entity.members:
            pass
        else:
            session.send_response({
                'FOR': 'MSG-GROUP-SEND',
                'status': 'failed',
                'message': 'You are not a member of the group!'
            })
            return

        members = group_entity.members
        for member in members:
            if member == session.user.username:
                continue
            member_session: Session = SessionManager.get_by_username(member)
            if member_session is not None:
                member_session.send_response({
                    'FOR': 'NOTIF',
                    'from_group': group_entity.group_name,
                    'from_user': session.user.username,
                    'text': request['message']
                })
                print('send to '+member_session.user.username)

        group_entity.inbox.append({
            'from_user': session.user.username,
            'text': request['message']
        })

        session.send_response({
            'FOR': 'MSG-GROUP-SEND',
            'status': 'success'
        })

        self.group_repository.save(group_entity)

    def _msg_group_get_handler(self, session: Session, request):
        group_entity: GroupEntity = self.group_repository.find_by_id(request['group_id'])

        if session.user.username in group_entity.members:
            session.send_response({
                'FOR': 'MSG-GROUP-GET',
                'messages': group_entity.inbox
            })
        else:
            session.send_response({
                'FOR': 'MSG-GROUP-GET',
                'status': 'failed',
                'message': 'You are not a member of the group!'
            })


