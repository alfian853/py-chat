class BaseEntity(object):
    def __init__(self):
        self.id = None

    def get_data(self):
        raise NotImplementedError

