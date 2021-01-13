#!/usr/bin/env python

""" LernSucks API Wrapper
"""

# 3rd-party dependencies
import requests

# Package modules
from .util.communicator import get_lernsax_tasks, login_to_lernsax, logout_from_lernsax


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

    def get_tasks(self):
        return get_lernsax_tasks(self)
