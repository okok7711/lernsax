#!/usr/bin/env python

""" LernSucks API Wrapper
"""

# Standard library
from typing import List

# 3rd-party dependencies
import requests

# Package modules
from .util.communicator import *


class Client:
    """ Main object for handling LernSax access and responses. """

    email = ""
    password = ""
    sid = ""
    member_of: List[str] = []
    root_url = "https://www.lernsax.de"  # without trailing slash
    api = f"{root_url}/jsonrpc.php"

    def post(self, json) -> dict:
        return requests.post(self.api, json=json).json()

    def login(self, email: str, password: str) -> list:
        return login_to_lernsax(self, email, password)

    def refresh_session(self) -> list:
        return refresh_lernsax_session(self)

    def logout(self) -> list:
        return logout_from_lernsax(self)

    def get_state(self, login: str) -> list:
        return get_storage_state(self, login)

    def get_files(self, login: str, recursive: bool) -> list:
        return get_lernsax_files(self, login, recursive)

    def get_tasks(self) -> list:
        return get_lernsax_tasks(self)

    def get_notes(self, login: str) -> list:
        return get_lernsax_notes(self, login)

    def get_board(self, login: str) -> list:
        return get_lernsax_board(self, login)

    def add_board_entry(self, login: str, title: str, text: str, color: str) -> list:
        return add_lernsax_board_entry(self, login, title, text, color)

    def add_note(self, title: str, text: str) -> list:
        return add_lernsax_note(self, title, text)

    def delete_note(self, id: str) -> list:
        return delete_lernsax_note(self, id)

    def get_email_folders(self) -> list:
        return get_lernsax_email_folders(self)

    def get_emails(self, folder_id: str) -> list:
        return get_lernsax_emails(self, folder_id)

    def read_email(self, folder_id: str, message_id: int) -> list:
        return read_lernsax_email(self, folder_id, message_id)

    def send_email(self, to: str, subject: str, body: str) -> list:
        return send_lernsax_email(self, to, subject, body)

    def get_quickmessages(self) -> list:
        return read_lernsax_quickmessages(self)

    def get_quickmessage_history(self, start_id: int) -> list:
        return get_lernsax_quickmessage_history(self, start_id)

    def group_quickmessage_history_by_chat(self, quickmsg_history: list) -> list:
        return group_lernsax_quickmessage_history_by_chat(quickmsg_history)

    def send_quickmessage(self, login: str, text: str) -> list:
        return send_lernsax_quickmessage(self, login, text)
