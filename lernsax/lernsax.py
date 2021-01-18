#!/usr/bin/env python

""" LernSucks API Wrapper
"""

# 3rd-party dependencies
import requests

# Package modules
from .util.communicator import *


class Client:
    """ Main object for handling LernSax access and responses. """

    email = ""
    password = ""
    sid = ""
    member_of = []
    root_url = "https://www.lernsax.de"  # without trailing slash
    api = f"{root_url}/jsonrpc.php"

    def post(self, json):
        return requests.post(self.api, json=json).json()

    def login(self, email, password):
        return login_to_lernsax(self, email, password)

    def refresh_session(self):
        return refresh_lernsax_session(self)

    def logout(self):
        return logout_from_lernsax(self)

    def get_state(self, login):
        return get_storage_state(self, login)

    def get_files(self, login, recursive):
        return get_lernsax_files(self, login, recursive)

    def get_tasks(self):
        return get_lernsax_tasks(self)

    def get_notes(self, login):
        return get_lernsax_notes(self, login)

    def get_board(self, login):
        return get_lernsax_board(self, login)
    
    def add_board_entry(self, login, title, text, color):
        return add_lernsax_board_entry(self, login, title, text, color)

    def add_note(self, title, text):
        return add_lernsax_note(self, title, text)

    def delete_note(self, id):
        return delete_lernsax_note(self, id)

    def send_email(self, subject, body, to):
        return send_lernsax_email(self, body, to, subject)

    def get_emails(self, folder_id):
        return get_lernsax_emails(self, folder_id)

    def read_email(self, folder_id, message_id):
        return read_lernsax_email(self, folder_id, message_id)

    def get_email_folders(self):
        return get_lernsax_email_folders(self)

    def get_quickmessages(self):
        return read_lernsax_quickmessages(self)
    
    def get_quickmessage_history(self):
        return get_lernsax_quickmessage_history(self)

    def send_quickmessage(self, login, text):
        return send_lernsax_quickmessage(self, login, text)
