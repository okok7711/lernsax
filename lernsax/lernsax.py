#!/usr/bin/env python

""" LernSucks API Wrapper
"""

# 3rd-party dependencies
import requests

# Package modules
from .util.communicator import get_lernsax_tasks, login_to_lernsax, logout_from_lernsax, get_lernsax_notes, get_lernsax_board, get_lernsax_files, get_storage_state, delete_lernsax_note, add_lernsax_note


class Client:
    """ Main object for handling LernSax access and responses. """
    email = ""
    password = ""
    sid = ""
    root_url = "https://www.lernsax.de"  # without trailing slash
    api = f"{root_url}/jsonrpc.php"

    def post(self, json):
        return requests.post(self.api, json=json).json()

    def login(self, email, password):
        return login_to_lernsax(self, email, password)

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
    
    def add_note(self, title, text):
        return add_lernsax_note(self, title, text)
    
    def delete_note(self, id):
        return delete_lernsax_note(self, id)