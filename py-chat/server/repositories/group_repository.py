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

    def find_by_id(self, id: str) -> GroupEntity:
        obj = super().find_by_id(id)

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




