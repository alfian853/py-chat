from entities import FileEntity
from repositories import AbstractRepository


class FileRepository(AbstractRepository):
    instance = None

    def __init__(self):
        super().__init__('files')

    @staticmethod
    def get_instance():
        if FileRepository.instance is None:
            FileRepository.instance = FileRepository()
        return FileRepository.instance

    def find_by_file_code(self, file_code):
        res = self.db.find_one({'file_code': file_code})
        if res is not None:
            file = FileEntity()
            file.id = res['_id']
            file.file_code = res['file_code']
            file.file_path = res['file_path']
            file.owner = res['owner']
            return file
        return None
