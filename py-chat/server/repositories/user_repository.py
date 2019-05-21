from repositories import AbstractRepository
from entities import UserEntity


class UserRepository(AbstractRepository):
    instance = None

    def __init__(self):
        super().__init__('users')

    @staticmethod
    def get_instance():
        if UserRepository.instance is None:
            UserRepository.instance = UserRepository()
        return UserRepository.instance

    def find_by_username(self, username):
        """

        :rtype: UserEntity
        """
        res = self.db.find_one({'username': username})
        if res is not None:
            user = UserEntity()
            user.id = res['_id']
            user.username = res['username']
            user.password = res['password']
            user.contact_list = res['contact_list']
            user.inbox = res['inbox']
            user.group_list = res['group_list']
            return user
        return None

    def get_message_from(self, username, from_username):
        res = self.db.find_one({'username': username})

        if from_username in res['inbox'].keys():
            return res['inbox'][from_username]
        else:
            return []
