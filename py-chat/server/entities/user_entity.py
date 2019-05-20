from entities import BaseEntity


class UserEntity(BaseEntity):
    def __init__(self):
        super().__init__()
        self.username = None  # string
        self.password = None  # string
        # joined and created group
        self.joined_groups = []
        self.inbox = []

    def get_data(self):
        return {
            'username': self.username,
            'password': self.password,
            'joined_groups': self.joined_groups,
            'inbox': self.inbox
        }
