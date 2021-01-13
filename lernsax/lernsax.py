#!/usr/bin/env python

""" LernSucks API Wrapper
"""

# Standard library
import json, time

# 3rd-party dependencies
import requests

from bs4 import BeautifulSoup

# Package modules
from .util import exceptions


def jsonrpc(list):
    return [
        {"id": k[0], "jsonrpc": "2.0", "method": k[1], "params": k[2]} for k in list
    ]


class Client:
    def __init__(self) -> None:
        self.email = ""
        self.password = ""
        self.sid = ""
        self.api = "https://www.lernsax.de/jsonrpc.php"

    def post(self, json):
        return requests.post(self.api, json=json).json()

    def login(self, email, password):
        res = self.post(
            jsonrpc(
                [
                    [
                        1,
                        "login",
                        {"login": email, "password": password, "get_miniature": True},
                    ],
                    [999, "get_information", {}],
                ]
            )
        )
        if res[0]["result"]["return"] == "OK":
            self.sid, self.email, self.password = (
                res[1]["result"]["session_id"],
                email,
                password,
            )
            return res
        else:
            if res[0]["result"]["errno"] == "107":
                raise exceptions.AccessDenied(res[0]["result"])
            elif res[0]["result"]["errno"] == "9999":
                raise exceptions.ConsequentialError(res[0]["result"])
            else:
                raise exceptions.LoginError(res[0]["result"])

    def logout(self):
        res = self.post(
            jsonrpc(
                [
                    [1, "set_session", {"session_id": self.sid}],
                    [2, "set_focus", {"object": "settings"}],
                    [3, "logout", {}],
                ]
            )
        )
        if res[-1]["result"]["return"] == "OK":
            self.sid = ""
            return res
        else:
            raise exceptions.LogoutError(res[-1]["result"])

    def getTasks(self):
        if self.sid:
            try:
                url = f"https://www.lernsax.de//wws/105500.php?sid={self.sid}"
                res = requests.get(url, allow_redirects=True)
                resHtml = res.text
                soup = BeautifulSoup(resHtml, "html.parser")
                tasks = soup.find_all(
                    "a", attrs={"href": "#", "class": "oc", "data-popup": True}
                )
                return tasks
            except:
                raise exceptions.TaskError()
        else:
            raise exceptions.NotLoggedIn()
