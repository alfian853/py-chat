from entities import BaseEntity


class GroupEntity(BaseEntity):
    def __init__(self):
        super().__init__()
        self.admin = ''  # string
        self.type = 'open'  # [open,close]
        self.join_request = []  # used if self.type == close
        self.members = []
        self.inbox = []

    def get_data(self):
        return {
            'admin': self.admin,
            'type': self.type,
            'join_request': self.join_request,
            'members': self.members,
            'inbox': self.inbox
        }
