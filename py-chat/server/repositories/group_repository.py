from entities import GroupEntity
from repositories import AbstractRepository


class GroupRepository(AbstractRepository):
    instance = None

    def __init__(self):
        super().__init__('groups')

    @staticmethod
    def get_instance():
        if GroupRepository.instance is None:
            GroupRepository.instance = GroupRepository()
        return GroupRepository.instance

    def find_by_code(self, code: str) -> GroupEntity:
        obj = self.db.find_one({
            'code': code
        })

        if obj is None:
            return None
        else:
            entity = GroupEntity()
            entity.id = obj['_id']
            entity.group_name = obj['group_name']
            entity.inbox = obj['inbox']
            entity.members = obj['members']
            entity.admins = obj['admins']
            entity.code = obj['code']
            return entity

    def find_by_name(self, name):
        res = self.db.find_one({'group_name': name})
        if res is not None:
            entity = GroupEntity()
            entity.id = res['_id']
            entity.group_name = res['name']
            entity.inbox = res['inbox']
            entity.members = res['members']
            entity.admins = res['admins']
            entity.code = res['code']
            return entity
        return None

    def find_by_code(self, code):
        res = self.db.find_one({'code': code})
        if res is not None:
            entity = GroupEntity()
            entity.id = res['_id']
            entity.group_name = res['name']
            entity.inbox = res['inbox']
            entity.members = res['members']
            entity.admin = res['admin']
            entity.code = res['code']
            return entity
        return None



