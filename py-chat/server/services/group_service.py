from entities import GroupEntity, UserEntity
from repositories import GroupRepository, UserRepository
from session import Session


class GroupService:
    def __init__(self):
        self.user_repository = UserRepository.get_instance()
        self.group_repository = GroupRepository.get_instance()
        pass

    def handle_request(self, session: Session, request, commands: str):
        commands = commands.split('-')

        if commands[0] == 'INVITE':
            self._handle_invite(session, request)
        elif commands[0] == 'GET':
            self._get_group_list(session, request)

    def _handle_invite(self, session, request):
        pass

    def _get_group_list(self, session: Session, request):
        user_entity: UserEntity = self.user_repository.find_by_username(session.user.username)
        session.send_response({
            'FOR': 'GROUP-GET',
            'group_list': user_entity.group_list
        })
