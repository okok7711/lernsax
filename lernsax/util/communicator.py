""" Communicator code to talk with LernSax.de
"""

# Standard library
import json, time

# 3rd-party dependencies
import requests

from box import Box
from bs4 import BeautifulSoup

# Package modules
from . import exceptions


def jsonrpc(data):
    return [
        {"id": k[0], "jsonrpc": "2.0", "method": k[1], "params": k[2]} for k in data
    ]


def login_to_lernsax(client, email, password):
    """ Enter the LernSax session """
    results_raw = client.post(
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
    results = [Box(res) for res in results_raw]
    if (
        results[0].result["return"] == "OK"
    ):  # "return" can't be accessed using attribute (provided by Box) because it is has the same name as the python statement
        client.sid, client.email, client.password = (
            results[1].result.session_id,
            email,
            password,
        )
        return results_raw
    else:
        if results[0].result.errno == "107":
            raise exceptions.AccessDenied(results[0].result)
        elif results[0].result.errno == "9999":
            raise exceptions.ConsequentialError(results[0].result)
        else:
            raise exceptions.LoginError(results[0].result)


def logout_from_lernsax(client):
    """ Exit the LernSax session """
    results_raw = client.post(
        jsonrpc(
            [
                [1, "set_session", {"session_id": client.sid}],
                [2, "set_focus", {"object": "settings"}],
                [3, "logout", {}],
            ]
        )
    )
    results = [Box(res) for res in results_raw]
    if results[-1].result["return"] == "OK":
        client.sid = ""
        return results_raw
    else:
        raise exceptions.LogoutError(results[-1].result)


def get_lernsax_tasks(client):
    """ Get LernSax tasks """
    if not client.sid:
        raise exceptions.NotLoggedIn()

    url = f"{client.root_url}/wws/105500.php?sid={client.sid}"
    res = requests.get(url, allow_redirects=True)
    resHtml = res.text

    try:
        soup = BeautifulSoup(resHtml, "html.parser")
        tasks = soup.find_all(
            "a", attrs={"href": "#", "class": "oc", "data-popup": True}
        )
        return tasks
    except:
        raise exceptions.TaskError()
