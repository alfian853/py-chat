from entities import BaseEntity


class GroupEntity(BaseEntity):
    def __init__(self):
        super().__init__()
        self.admins = []  # string
        self.code = ''  # untuk join group jika open
        self.group_name = ''
        self.members = []
        self.inbox = []
        self.enabled = True # true = available, false = deleted (safe delete)

    def get_data(self):
        return {
            'name': self.group_name,
            'admin': self.admins,
            'members': self.members,
            'inbox': self.inbox,
            'code': self.code
        }
