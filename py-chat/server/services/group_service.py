from entities import GroupEntity, UserEntity
from repositories import GroupRepository, UserRepository
from session import Session
import bson


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
        elif commands[0] == 'CREATE':
            self._create_group(session, request)

    def _handle_invite(self, session, request):
        pass

    def _get_group_list(self, session: Session, request):
        user_entity: UserEntity = self.user_repository.find_by_username(session.user.username)

        # group_list_name = []

        # for group_id in user_entity.group_list:
        #     group: GroupEntity = self.group_repository.find_by_id(group_id)
        #     print(group)
        #     print('Named: ' + str(group.group_name))
            # group_list_name.append(group.group_name)

        session.send_response({
            'FOR': 'GROUP-GET',
            'group_list': user_entity.group_list
            # 'group_list_name': group_list_name
        })

    def _create_group(self, session: Session, request):
        user = [session.user.username]
        group_name = request['group_name']

        group = GroupEntity()
        group.group_name = group_name
        if request['code'] is not None:
            group.code = request['code']
        group.admins = user
        group.members = user
        # print (group.get_data)
        _id = self.group_repository.save(group)

        user_group_list = session.user.group_list
    
        # user_group_list.append(str(_id)) # hex encoded ObjectId https://github.com/ankhers/mongodb/issues/40
        # print('inserted_id: '  + str(_id))
        # user_group_list.append(group_name)
        self.user_repository.pushGroup(session.user.username, bson.BSON.encode(group))

        # self.user_repository.save(session.user)

        session.send_response({
            'FOR': 'GROUP-CREATE',
            'status': 'success',
            'message': 'group has been created'
        });


