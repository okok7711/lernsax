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


def pack_responses(results: list, main_answer_index: int) -> dict:
    """Packs multiple method responses together.
    The main response is accessible through the "result" key.
    Helper method responses are accessible through the "helpers" key of the returned dict."""
    packed_results = Box({"result": results.pop(main_answer_index), "helpers": results})
    return packed_results.to_dict()


def jsonrpc(data: list):
    return [{"id": k[0], "jsonrpc": "2.0", "method": k[1], "params": k[2]} for k in data]


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

    if not results[0].result["return"] == "OK":
        if results[0].result.errno == "107" or results[0].result.errno == "103":
            raise exceptions.AccessDenied(results[0].result)
        elif results[0].result.errno == "9999":
            raise exceptions.ConsequentialError(results[0].result)
        else:
            raise exceptions.LoginError(results[0].result)

    client.sid, client.email, client.password, client.member_of = (
        results[1].result.session_id,
        email,
        password,
        [member.login for member in results[0].result.member],
    )
    return pack_responses(results_raw, 0)


def refresh_lernsax_session(client) -> dict:
    """ Refreshes current LernSax session. """
    if not client.sid:
        raise exceptions.NotLoggedIn()
    results_raw = client.post(jsonrpc([[1, "set_session", {"session_id": client.sid}]]))
    return pack_responses(results_raw, 0)


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
    if not results[-1].result["return"] == "OK":
        raise exceptions.LogoutError(results[-1].result)

    client.sid = ""
    return pack_responses(results_raw, 2)


def get_lernsax_tasks(client) -> BeautifulSoup:
    """ Get LernSax tasks """
    if not client.sid:
        raise exceptions.NotLoggedIn()
    url = f"{client.root_url}/wws/105500.php?sid={client.sid}"
    res = requests.get(url, allow_redirects=True)
    resHtml = res.text
    try:
        soup = BeautifulSoup(resHtml, "html.parser")
        tasks = soup.find_all("a", attrs={"href": "#", "class": "oc", "data-popup": True})
        return tasks
    except:
        raise exceptions.TaskError()


# FileRequest


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
    if not results[-1].result["return"] == "OK":
        raise exceptions.FileError(results_raw[-1])
    return pack_responses(results_raw, 2)


def get_storage_state(client, login: str) -> dict:
    """ Gets amount of used storage and free storage """
    if not client.sid:
        raise exceptions.NotLoggedIn()
    results_raw = client.post(
        jsonrpc(
            [
                [1, "set_session", {"session_id": client.sid}],
                [2, "set_focus", {"login": login, "object": "files"}],
                [3, "get_state", {}],
            ]
        )
    )
    return pack_responses(results_raw, 2)


# ForumRequest


def get_lernsax_board(client, login: str) -> dict:
    """ Gets messages board for specified login """
    if not client.sid:
        raise exceptions.NotLoggedIn()
    results_raw = client.post(
        jsonrpc(
            [
                [1, "set_session", {"session_id": client.sid}],
                [2, "set_focus", {"login": login, "object": "files"}],
                [3, "get_entries", {}],
            ]
        )
    )
    return pack_responses(results_raw, 2)


def add_lernsax_board_entry(client, login: str, title: str, text: str, color: str) -> dict:
    """Adds board entry for specified (group-)login.
    color must be a hexadecimal color code
    """
    if not client.sid:
        raise exceptions.NotLoggedIn()
    results_raw = client.post(
        jsonrpc(
            [
                [1, "set_session", {"session_id": client.sid}],
                [2, "set_focus", {"login": login, "object": "board"}],
                [
                    3,
                    "add_entry",
                    {"title": title, "text": text, "color": color},
                ],
            ]
        )
    )
    results = [Box(res) for res in results_raw]
    if not results[-1].result["return"] == "OK":
        raise exceptions.BoardError(results_raw[-1])
    return pack_responses(results_raw, 2)


# NotesRequest


def get_lernsax_notes(client, login: str) -> dict:
    """ Gets notes for specified login """
    if not client.sid:
        raise exceptions.NotLoggedIn()
    results_raw = client.post(
        jsonrpc(
            [
                [1, "set_session", {"session_id": client.sid}],
                [2, "set_focus", {"login": login, "object": "notes"}],
                [3, "get_entries", {}],
            ]
        )
    )
    return pack_responses(results_raw, 2)


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
    if not results[-1].result["return"] == "OK":
        raise exceptions.NoteError(results_raw[-1])
    return pack_responses(results_raw, 2)


def delete_lernsax_note(client, id: str) -> dict:
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
    if not results[-1].result["return"] == "OK":
        raise exceptions.NoteError(results_raw[-1])
    return pack_responses(results_raw, 2)


#  EmailRequest


def send_lernsax_email(client, to: str, subject: str, body: str) -> dict:
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
    if not results[-1].result["return"] == "OK":
        raise exceptions.EmailError(results_raw[-1])
    return pack_responses(results_raw, 2)


def get_lernsax_emails(client, folder_id: str) -> dict:
    """ Gets emails from a folder id """
    if not client.sid:
        raise exceptions.NotLoggedIn()
    results_raw = client.post(
        jsonrpc(
            [
                [1, "set_session", {"session_id": client.sid}],
                [2, "set_focus", {"object": "mailbox"}],
                [3, "get_messages", {"folder_id": folder_id}],
            ]
        )
    )
    return pack_responses(results_raw, 2)


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
    results = [Box(res) for res in results_raw]
    if not results[-1].result["return"] == "OK":
        raise exceptions.EmailError(results_raw[-1])
    return pack_responses(results_raw, 2)


def get_lernsax_email_folders(client):
    """ returns the folders to get the id """
    if not client.sid:
        raise exceptions.NotLoggedIn()
    results_raw = client.post(
        jsonrpc(
            [
                [1, "set_session", {"session_id": client.sid}],
                [2, "set_focus", {"object": "mailbox"}],
                [3, "get_folders", {}],
            ]
        )
    )

    return pack_responses(results_raw, 2)


# MessengerRequest


def read_lernsax_quickmessages(client) -> dict:
    """ returns quickmessages """
    if not client.sid:
        raise exceptions.NotLoggedIn()
    results_raw = client.post(
        jsonrpc(
            [
                [1, "set_session", {"session_id": client.sid}],
                [2, "set_focus", {"object": "messenger"}],
                [3, "read_quick_messages", {"export_session_file": 0}],
            ]
        )
    )
    return pack_responses(results_raw, 2)


def send_lernsax_quickmessage(client, login: str, text: str) -> dict:
    """ Sends a quickmessage to an email holder """
    if not client.sid:
        raise exceptions.NotLoggedIn()
    results_raw = client.post(
        jsonrpc(
            [
                [1, "set_session", {"session_id": client.sid}],
                [2, "set_focus", {"object": "messenger"}],
                [3, "send_quick_message", {"login": login, "text": text, "import_session_file": 0}],
            ]
        )
    )
    results = [Box(res) for res in results_raw]
    if not results[-1].result["return"] == "OK":
        raise exceptions.QuickMessageError(results_raw[-1])
    return pack_responses(results_raw, 2)


def get_lernsax_quickmessage_history(client, start_id: int) -> dict:
    """ get quickmessage history """
    if not client.sid:
        raise exceptions.NotLoggedIn()
    results_raw = client.post(
        jsonrpc(
            [
                [1, "set_session", {"session_id": client.sid}],
                [2, "set_focus", {"object": "messenger"}],
                [3, "get_history", {"start_id": start_id, "export_session_file": 0}],
            ]
        )
    )
    results = [Box(res) for res in results_raw]
    if not results[-1].result["return"] == "OK":
        if results[-1].result.errno == "107" or results[-1].result.errno == "103":
            raise exceptions.AccessDenied(results[-1].result)
        else:
            raise exceptions.QuickMessageError(results_raw[-1])
    return pack_responses(results_raw, 2)


def group_lernsax_quickmessage_history_by_chat(quickmsg_history: list):
    """Groups LernSax quickmessage history by chat email and date.
    The returned LernSax quickmessage history only includes a list of all messages. They are not grouped by chat emails yet.
    This function will group all quickmessages for same chat emails together.
    In the returned dict the messages associated to a chat are sorted by the date they were sent.
    Parse the returned data from get_lernsax_quickmessage_history() as quickmsg_history attr.
    """
    messages = quickmsg_history["result"]["result"]["messages"]

    grouped_messages = Box({})
    for msg in messages:
        msg = Box(msg)
        msg.date = int(msg.date)
        receiving_chat_email = msg.to.login
        receiving_chat_name = msg.to.name_hr
        receiving_chat_type = msg.to.type

        if not receiving_chat_email in grouped_messages:
            grouped_messages[receiving_chat_email] = {
                "chat_name": receiving_chat_name,
                "chat_type": receiving_chat_type,
                "messages": [],
            }

        new_message = {
            "id": msg.id,
            "text": msg.text,
            "date": msg.date,
            "flags": msg.flags,
        }

        if (
            len(grouped_messages[receiving_chat_email].messages) == 0
            or msg.date >= grouped_messages[receiving_chat_email].messages[-1].date
        ):
            grouped_messages[receiving_chat_email].messages.append(new_message)
        else:
            # By default the messages in the quickmessage history should be sorted by date. If there is a mistake in the sorting
            # those statements are called.
            current_index = 0
            for existing_msg in grouped_messages[receiving_chat_email].messages:
                if existing_msg.date >= msg.date:
                    grouped_messages[receiving_chat_email].messages.insert(current_index, new_message)
                    break

                current_index += 1

    return grouped_messages.to_dict()
