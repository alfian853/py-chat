from entities import BaseEntity


class GroupEntity(BaseEntity):
    def __init__(self):
        super().__init__()
        self.admins = []  # string
        self.code = ''  # untuk join group jika open
        self.type = 'open'  # [open,close]
        self.members = []
        self.inbox = []

    def get_data(self):
        return {
            'admin': self.admins,
            'type': self.type,
            'members': self.members,
            'inbox': self.inbox,
            'code': self.code
        }
