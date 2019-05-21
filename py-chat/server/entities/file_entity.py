from entities import BaseEntity


class FileEntity(BaseEntity):

    def __init__(self):
        super().__init__()
        self.file_code = None
        self.owner = None
        self.file_path = None

    def get_data(self):
        return {
            'file_code': self.file_code,
            'owner': self.owner,
            'file_path': self.file_path
        }
