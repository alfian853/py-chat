import uuid

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
        elif commands[0] == 'CREATE':
            self._create_group(session, request)
        elif commands[0] == 'JOIN':
            self._join_group(session, request)
        elif commands[0] == 'EXIT': 
            self._exit_group(session, request)

    def _handle_invite(self, session, request):
        request_code = request['code']
        group = self.group_repository.find_by_code(request_code)
        group_code = group.code
        group_name = group.group_name
        username = session.user.username
        group_members = group.members
        if username not in group_members:
            session.send_response({
                'FOR': 'GROUP-INVITE',
                'status': 'failed',
                'message': 'you are not belong to this group'
            })

        else:
            group_invite = {
                'code': group_code,
                'group_name': group_name
            }

            request_user = request['user_list']
            new_member = []
            for name in request_user:
                user_exist = self.user_repository.find_by_username(name)
                if user_exist is not None:
                    user_exist_group = user_exist.group_list
                    user_exist_group.append(group_invite)
                    self.user_repository.save(user_exist)
                    new_member.append(name)
                    session.send_response({
                        'FOR': 'GROUP-INVITE',
                        'status': 'success',
                        'message': name + ' has joined this group'
                    })
                else:
                    session.send_response({
                        'FOR': 'GROUP-INVITE',
                        'status': 'failed',
                        'message': name + ' failed to join this group'
                    })

            if len(new_member) > 0:
                group_members.extend(new_member)
                self.group_repository.save(group)
                session.send_response({
                    'FOR': 'GROUP-INVITE',
                    'status': 'success',
                    'message': 'new members have been added'
                })
            else:
                session.send_response({
                    'FOR': 'GROUP-INVITE',
                    'status': 'failed',
                    'message': 'no member added'
                })

    def _get_group_list(self, session: Session, request):
        user_entity: UserEntity = self.user_repository.find_by_username(session.user.username)

        session.send_response({
            'FOR': 'GROUP-GET',
            'group_list': user_entity.group_list
        })

    def _create_group(self, session: Session, request):
        user = [session.user.username]
        group_name = request['group_name']

        group = GroupEntity()
        group.group_name = group_name
        # if request['code'] is not None:
        #     group.code = request['code']
        unique_code = str(uuid.uuid4())[1:7]
        group.code = unique_code
        group.admins = user
        group.members = user
        # print (group.get_data)
        _id = self.group_repository.save(group)

        user_group_list = session.user.group_list

        user_group_append = {
            'code': unique_code,
            'group_name': group_name
        }
    
        # user_group_list.append(str(_id)) # hex encoded ObjectId https://github.com/ankhers/mongodb/issues/40
        # print('inserted_id: '  + str(_id))
        # user_group_list.append(group_name)
        user_group_list.append(user_group_append)
        # self.user_repository.pushGroup(session.user.username, bson.BSON.encode(group))

        self.user_repository.save(session.user)

        session.send_response({
            'FOR': 'GROUP-CREATE',
            'status': 'success',
            'message': 'group has been created'
        })

    def _join_group(self, session: Session, request):
        request_code = request['code']
        group = self.group_repository.find_by_code(request_code)
        if group is not None:
            print(group)
            print('code: ' + group.code)
            group_name = group.group_name
            group_code = group.code

            member_list = group.members
            username = session.user.username
            if username not in member_list:
                member_list.append(username)
            self.group_repository.save(group)

            user_group = session.user.group_list
            user_group_append = {
                'code': group_code,
                'group_name': group_name
            }
            user_group.append(user_group_append)
            self.user_repository.save(session.user)

            session.send_response({
                'FOR': 'GROUP-JOIN',
                'status': 'success',
                'message': 'you have joined this group'
            })

        else:
            session.send_response({
                'FOR': 'GROUP-JOIN',
                'status': 'failed',
                'message': 'group code is invalid'
            })

    def _exit_group(self, session: Session, request):
        request_code = request['code']
        group = self.group_repository.find_by_code(request_code)
        if group is not None:
            group_members = group.members
            username = session.user.username
            if username in group_members:
                group_members.remove(username)
                self.group_repository.save(group)

                user_group_list = session.user.group_list
                for i in range(len(user_group_list)):
                    if user_group_list[i]['code'] == request_code:
                        del user_group_list[i]
                        break

                self.user_repository.save(session.user)

                session.send_response({
                    'FOR': 'GROUP-EXIT',
                    'status': 'success',
                    'message': 'you have left this group'
                })
            else:
                session.send_response({
                    'FOR': 'GROUP-EXIT',
                    'status': 'failed',
                    'message': 'you are not belong to this group'
                })
        else:
            session.send_response({
                'FOR': 'GROUP-EXIT',
                'status': 'failed',
                'message': 'group is not available'
            })

