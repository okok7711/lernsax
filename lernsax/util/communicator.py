""" Communicator code to talk with LernSax.de
"""

# Standard library
import json, time
from re import sub

# 3rd-party dependencies
import requests

from box import Box
from bs4 import BeautifulSoup

# Package modules
from . import exceptions


def jsonrpc(data: list):
    return [
        {"id": k[0], "jsonrpc": "2.0", "method": k[1], "params": k[2]} for k in data
    ]


def login_to_lernsax(client, email: str, password: str) -> dict:
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


def refresh_lernsax_session(client) -> dict:
    """ Refreshes current LernSax session. """
    if not client.sid:
        raise exceptions.NotLoggedIn()
    return client.post(jsonrpc([[1, "set_session", {"session_id": client.sid}]]))


def logout_from_lernsax(client) -> dict:
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


def get_lernsax_tasks(client) -> BeautifulSoup:
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


def get_lernsax_files(client, login: str, recursive: bool) -> dict:
    """ Gets directories via lernsax login email """
    if not client.sid:
        raise exceptions.NotLoggedIn()
    results_raw = client.post(
        jsonrpc(
            [
                [1, "set_session", {"session_id": client.sid}],
                [2, "set_focus", {"login": login, "object": "files"}],
                [
                    3,
                    "get_entries",
                    {
                        "folder_id": "",
                        "get_files": 1,
                        "get_folders": 1,
                        "recursive": int(recursive),
                    },
                ],
            ]
        )
    )
    results = [Box(res) for res in results_raw]
    if results[-1].result["return"] == "OK":
        return results_raw
    else:
        raise exceptions.FileError(results_raw[-1])


def get_storage_state(client, login: str) -> dict:
    """ Gets amount of used storage and free storage """
    if not client.sid:
        raise exceptions.NotLoggedIn()
    return client.post(
        jsonrpc(
            [
                [1, "set_session", {"session_id": client.sid}],
                [2, "set_focus", {"login": login, "object": "files"}],
                [3, "get_state", {}],
            ]
        )
    )


def get_lernsax_board(client, login: str) -> dict:
    """ Gets messages board for specified login """
    if not client.sid:
        raise exceptions.NotLoggedIn()
    return client.post(
        jsonrpc(
            [
                [1, "set_session", {"session_id": client.sid}],
                [2, "set_focus", {"login": login, "object": "files"}],
                [3, "get_entries", {}],
            ]
        )
    )


def get_lernsax_notes(client, login: str) -> dict:
    """ Gets messages board for specified login """
    if not client.sid:
        raise exceptions.NotLoggedIn()
    return client.post(
        jsonrpc(
            [
                [1, "set_session", {"session_id": client.sid}],
                [2, "set_focus", {"login": login, "object": "notes"}],
                [3, "get_entries", {}],
            ]
        )
    )


def add_lernsax_note(client, title: str, text: str) -> dict:
    """ adds a note """
    if not client.sid:
        raise exceptions.NotLoggedIn()
    results_raw = client.post(
        jsonrpc(
            [
                [1, "set_session", {"session_id": client.sid}],
                [2, "set_focus", {"object": "notes"}],
                [3, "add_entry", {"text": text, "title": title}],
            ]
        )
    )
    results = [Box(res) for res in results_raw]
    if results[-1].result["return"] == "OK":
        return results_raw
    else:
        raise exceptions.NoteError(results_raw[-1])


def delete_lernsax_note(client, id: int) -> dict:
    """ deletes a note """
    if not client.sid:
        raise exceptions.NotLoggedIn()
    results_raw = client.post(
        jsonrpc(
            [
                [1, "set_session", {"session_id": client.sid}],
                [2, "set_focus", {"object": "notes"}],
                [3, "delete_entry", {"id": id}],
            ]
        )
    )
    results = [Box(res) for res in results_raw]
    if results[-1].result["return"] == "OK":
        return results_raw
    else:
        raise exceptions.NoteError(results_raw[-1])


def send_lernsax_email(client, body: str, to: str, subject: str) -> dict:
    """ Sends an email """
    if not client.sid:
        raise exceptions.NotLoggedIn()
    results_raw = client.post(
        jsonrpc(
            [
                [1, "set_session", {"session_id": client.sid}],
                [2, "set_focus", {"object": "mailbox"}],
                [3, "send_mail", {"to": to, "subject": subject, "body_plain": body}],
            ]
        )
    )
    results = [Box(res) for res in results_raw]
    if results[-1].result["return"] == "OK":
        return results_raw
    else:
        raise exceptions.EmailError(results_raw[-1])


def get_lernsax_emails(client, folder_id: str) -> dict:
    """ Gets emails from a folder id """
    if not client.sid:
        raise exceptions.NotLoggedIn()
    results = client.post(
        jsonrpc(
            [
                [1, "set_session", {"session_id": client.sid}],
                [2, "set_focus", {"object": "mailbox"}],
                [3, "get_messages", {"folder_id": folder_id}],
            ]
        )
    )
    return results


def read_lernsax_email(client, folder_id: str, message_id: int) -> dict:
    """ reads an email with a certain message id """
    if not client.sid:
        raise exceptions.NotLoggedIn()
    results_raw = client.post(
        jsonrpc(
            [
                [1, "set_session", {"session_id": client.sid}],
                [2, "set_focus", {"object": "mailbox"}],
                [3, "read_message", {"folder_id": folder_id, "message_id": message_id}],
            ]
        )
    )
    try:
        results = [Box(res) for res in results_raw]
        if results[1].result["return"]:
            return results_raw
    except:
        raise exceptions.EmailError(results_raw)
    else:
        raise exceptions.EmailError(results_raw[-1])


def get_lernsax_email_folders(client):
    """ returns the folders to get the id """
    if not client.sid:
        raise exceptions.NotLoggedIn()
    results = client.post(
        jsonrpc(
            [
                [1, "set_session", {"session_id": client.sid}],
                [2, "set_focus", {"object": "mailbox"}],
                [3, "get_folders", {}],
            ]
        )
    )
    return results
