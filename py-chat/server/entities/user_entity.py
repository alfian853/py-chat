from entities import BaseEntity


class UserEntity(BaseEntity):
    def __init__(self):
        super().__init__()
        self.username = None  # string
        self.password = None  # string
        # joined and created group
        self.group_list = []
        self.contact_list = []
        self.inbox = {}

    def add_to_inbox(self, from_user, message):
        if from_user not in self.inbox.keys():
            self.inbox[from_user] = [message]
        else:
            self.inbox[from_user].append(message)

    def get_inbox_from(self, from_user):
        if from_user not in self.inbox.keys():
            return []
        return self.inbox[from_user]

    def get_data(self):
        return {
            'username': self.username,
            'password': self.password,
            'group_list': self.group_list,
            'contact_list': self.contact_list,
            'inbox': self.inbox
        }
