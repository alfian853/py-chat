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
            user.username = res['username']
            user.password = res['password']
            user.inbox = res['inbox']
            user.joined_groups = res['joined_groups']
            user.id = res['_id']
            return user
        return None
