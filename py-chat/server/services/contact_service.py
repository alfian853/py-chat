from repositories import UserRepository
from session import Session


class ContactService:
    instance = None

    @staticmethod
    def get_instance():
        if ContactService.instance is None:
            ContactService.instance = ContactService()
        return ContactService.instance

    def __init__(self):
        self.user_repository = UserRepository.get_instance()

    def handle_request(self, session: Session, request: dict, sub_commands: str):
        user = session.user
        response = dict()
        response['FOR'] = request['COMMAND']
        commands = sub_commands.split('-')

        if commands[0] == 'GET':
            response['contact_list'] = user.contact_list
            session.send_response(response)

        elif commands[0] == 'ADD':
            self._add_contact(session, request)

        elif commands[0] == 'DEL':
            self._del_contact(session, request)

    def _add_contact(self, session: Session, request: dict):
        new_contacts = request['contact_list']
        contact_list = session.user.contact_list
        counter = 0
        for contact in new_contacts:
            if contact not in contact_list \
                    and self.user_repository.find_by_username(contact) \
                    and contact != session.user.username:
                contact_list.append(contact)
                counter += 1

        self.user_repository.save(session.user)
        response = dict()
        response['FOR'] = request['COMMAND']
        response['message'] = str(counter) + ' new contact added'

        session.send_response(response)

    def _del_contact(self, session: Session, request: dict):
        target_contacts = request['contact_list']
        contact_list = session.user.contact_list
        counter = 0
        for contact in target_contacts:
            if contact in contact_list:
                contact_list.remove(contact)
                counter += 1

        self.user_repository.save(session.user)
        response = dict()
        response['FOR'] = request['COMMAND']
        response['message'] = str(counter) + ' contact deleted'

        session.send_response(response)
