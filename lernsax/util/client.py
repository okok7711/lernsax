"""
Communicator code to talk with LernSax.de
"""

from abc import ABC
from box import Box
from . import exceptions

# Abstract ApiClient only as a skeleton


class ApiClient(ABC):
    def pack_responses(self, results: list, main_answer_index: int) -> dict:
        """
        Packs multiple method responses together.
        The main response is accessible through the "result" key.
        Helper method responses are accessible through the "helpers" key of the returned dict.
        """
        packed_results = Box({"result": results.pop(
            main_answer_index), "helpers": results})
        return packed_results.to_dict()

    def jsonrpc(self, data: list):
        """
        Prepares Data to be sent to the API in correct jsonrpc format
        """
        return [{"id": k[0], "jsonrpc": "2.0", "method": k[1], "params": k[2]} for k in data]

    async def login(self, email: str = "", password: str = "") -> dict:
        """ Enter the LernSax session """
        if not email or not password:
            email, password = self.email, self.password
        results_raw = await self.post(
            self.jsonrpc(
                [
                    [
                        1,
                        "login",
                        {"login": email, "password": password,
                            "get_miniature": True},
                    ],
                    [999, "get_information", {}],
                ]
            )
        )
        results = [Box(res) for res in results_raw]

        if not results[0].result["return"] == "OK":
            raise exceptions.error_handler(
                results[0].result.errno)(results_raw[0]["result"])

        self.sid, self.email, self.password, self.member_of = (
            results[1].result.session_id,
            email,
            password,
            [member.login for member in results[0].result.member],
        )
        return self.pack_responses(results_raw, 0)

    async def refresh_session(self) -> dict:
        """ Refreshes current LernSax session. """
        if not self.sid:
            raise exceptions.NotLoggedIn()
        results_raw = await self.post(self.jsonrpc([[1, "set_session", {"session_id": self.sid}]]))
        return self.pack_responses(results_raw, 0)

    async def logout(self) -> dict:
        """ Exit the LernSax session """
        results_raw = await self.post(
            self.jsonrpc(
                [
                    [1, "set_session", {"session_id": self.sid}],
                    [2, "set_focus", {"object": "settings"}],
                    [3, "logout", {}],
                ]
            )
        )
        results = [Box(res) for res in results_raw]
        if not results[-1].result["return"] == "OK":
            raise exceptions.error_handler(
                results[-1].result.errno)(results_raw[-1]["result"])
        self.sid = ""
        return self.pack_responses(results_raw, 2)

    async def get_tasks(self, group: str) -> dict:
        """ Get LernSax tasks, thanks to  TKFRvisionOfficial for finding the json rpc request """
        if not self.sid:
            raise exceptions.NotLoggedIn()
        results_raw = await self.post(
            self.jsonrpc(
                [
                    [1, "set_session", {"session_id": self.sid}],
                    [2, "set_focus", {"login": group, "object": "tasks"}],
                    [3, "get_entries", {}],
                ]
            )
        )
        return self.pack_responses(results_raw, 2)

    # FileRequest

    async def get_files(self, login: str, recursive: bool) -> dict:
        """ Gets directories via lernsax login email """
        if not self.sid:
            raise exceptions.NotLoggedIn()
        results_raw = await self.post(
            self.jsonrpc(
                [
                    [1, "set_session", {"session_id": self.sid}],
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
        if not results[-1].result["return"] in ["OK", "RESUME"]:
            print(results_raw[-1]["result"])
            raise exceptions.error_handler(
                results[-1].result.errno)(results_raw[-1]["result"])
        return self.pack_responses(results_raw, 2)

    async def get_state(self, login: str) -> dict:
        """ Gets amount of used storage and free storage """
        if not self.sid:
            raise exceptions.NotLoggedIn()
        results_raw = await self.post(
            self.jsonrpc(
                [
                    [1, "set_session", {"session_id": self.sid}],
                    [2, "set_focus", {"login": login, "object": "files"}],
                    [3, "get_state", {}],
                ]
            )
        )
        return self.pack_responses(results_raw, 2)

    async def get_download_url(self, login: str, id: str) -> dict:
        """ Gets download id with the file id """
        if not self.sid:
            raise exceptions.NotLoggedIn()
        results_raw = await self.post(
            self.jsonrpc(
                [
                    [1, "set_session", {"session_id": self.sid}],
                    [2, "set_focus", {"login": login, "object": "files"}],
                    [3, "get_file_download_url", {"id": id}],
                ]
            )
        )
        return self.pack_responses(results_raw, 2)

    async def edit_file(self, login: str, id: str, description: str, name: str = None) -> dict:
        """ Edits a File's description and or name """
        if not self.sid:
            raise exceptions.NotLoggedIn()
        if not name:
            name = id[:id.rfind(",") + 1]
        results_raw = await self.post(
            self.jsonrpc(
                [
                    [1, "set_session", {"session_id": self.sid}],
                    [2, "set_focus", {"login": login, "object": "files"}],
                    [3, "set_file", {"id": id, "folder_id": id[:id.rfind(
                        "/")], "name": name, "description": description}],
                ]
            )
        )
        return self.pack_responses(results_raw, 2)

    # ForumRequest

    async def get_board(self, login: str) -> dict:
        """ Gets messages board for specified login """
        if not self.sid:
            raise exceptions.NotLoggedIn()
        results_raw = await self.post(
            self.jsonrpc(
                [
                    [1, "set_session", {"session_id": self.sid}],
                    [2, "set_focus", {"login": login, "object": "files"}],
                    [3, "get_entries", {}],
                ]
            )
        )
        return self.pack_responses(results_raw, 2)

    async def add_board_entry(self, login: str, title: str, text: str, color: str) -> dict:
        """Adds board entry for specified (group-)login.
        color must be a hexadecimal color code
        """
        if not self.sid:
            raise exceptions.NotLoggedIn()
        results_raw = await self.post(
            self.jsonrpc(
                [
                    [1, "set_session", {"session_id": self.sid}],
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
            raise exceptions.error_handler(
                results[-1].result.errno)(results_raw[-1]["result"])
        return self.pack_responses(results_raw, 2)

    # NotesRequest

    async def get_notes(self, login: str) -> dict:
        """ Gets notes for specified login """
        if not self.sid:
            raise exceptions.NotLoggedIn()
        results_raw = await self.post(
            self.jsonrpc(
                [
                    [1, "set_session", {"session_id": self.sid}],
                    [2, "set_focus", {"login": login, "object": "notes"}],
                    [3, "get_entries", {}],
                ]
            )
        )
        return self.pack_responses(results_raw, 2)

    async def add_note(self, title: str, text: str) -> dict:
        """ adds a note """
        if not self.sid:
            raise exceptions.NotLoggedIn()
        results_raw = await self.post(
            self.jsonrpc(
                [
                    [1, "set_session", {"session_id": self.sid}],
                    [2, "set_focus", {"object": "notes"}],
                    [3, "add_entry", {"text": text, "title": title}],
                ]
            )
        )
        results = [Box(res) for res in results_raw]
        if not results[-1].result["return"] == "OK":
            raise exceptions.error_handler(
                results[-1].result.errno)(results_raw[-1]["result"])
        return self.pack_responses(results_raw, 2)

    async def delete_note(self, id: str) -> dict:
        """ deletes a note """
        if not self.sid:
            raise exceptions.NotLoggedIn()
        results_raw = await self.post(
            self.jsonrpc(
                [
                    [1, "set_session", {"session_id": self.sid}],
                    [2, "set_focus", {"object": "notes"}],
                    [3, "delete_entry", {"id": id}],
                ]
            )
        )
        results = [Box(res) for res in results_raw]
        if not results[-1].result["return"] == "OK":
            raise exceptions.error_handler(
                results[-1].result.errno)(results_raw[-1]["result"])
        return self.pack_responses(results_raw, 2)

    #  EmailRequest

    async def send_email(self, to: str, subject: str, body: str) -> dict:
        """ Sends an email """
        if not self.sid:
            raise exceptions.NotLoggedIn()
        results_raw = await self.post(
            self.jsonrpc(
                [
                    [1, "set_session", {"session_id": self.sid}],
                    [2, "set_focus", {"object": "mailbox"}],
                    [3, "send_mail", {
                        "to": to, "subject": subject, "body_plain": body}],
                ]
            )
        )
        results = [Box(res) for res in results_raw]
        if not results[-1].result["return"] == "OK":
            raise exceptions.error_handler(
                results[-1].result.errno)(results_raw[-1]["result"])
        return self.pack_responses(results_raw, 2)

    async def get_emails(self, folder_id: str) -> dict:
        """ Gets emails from a folder id """
        if not self.sid:
            raise exceptions.NotLoggedIn()
        results_raw = await self.post(
            self.jsonrpc(
                [
                    [1, "set_session", {"session_id": self.sid}],
                    [2, "set_focus", {"object": "mailbox"}],
                    [3, "get_messages", {"folder_id": folder_id}],
                ]
            )
        )
        return self.pack_responses(results_raw, 2)

    async def read_email(self, folder_id: str, message_id: int) -> dict:
        """ reads an email with a certain message id """
        if not self.sid:
            raise exceptions.NotLoggedIn()
        results_raw = await self.post(
            self.jsonrpc(
                [
                    [1, "set_session", {"session_id": self.sid}],
                    [2, "set_focus", {"object": "mailbox"}],
                    [3, "read_message", {
                        "folder_id": folder_id, "message_id": message_id}],
                ]
            )
        )
        results = [Box(res) for res in results_raw]
        if not results[-1].result["return"] == "OK":
            raise exceptions.error_handler(
                results[-1].result.errno)(results_raw[-1])["result"]
        return self.pack_responses(results_raw, 2)

    async def get_email_folders(self):
        """ returns the folders to get the id """
        if not self.sid:
            raise exceptions.NotLoggedIn()
        results_raw = await self.post(
            self.jsonrpc(
                [
                    [1, "set_session", {"session_id": self.sid}],
                    [2, "set_focus", {"object": "mailbox"}],
                    [3, "get_folders", {}],
                ]
            )
        )

        return self.pack_responses(results_raw, 2)

    # MessengerRequest

    async def read_quickmessages(self) -> dict:
        """ returns quickmessages """
        if not self.sid:
            raise exceptions.NotLoggedIn()
        results_raw = await self.post(
            self.jsonrpc(
                [
                    [1, "set_session", {"session_id": self.sid}],
                    [2, "set_focus", {"object": "messenger"}],
                    [3, "read_quick_messages", {"export_session_file": 0}],
                ]
            )
        )
        return self.pack_responses(results_raw, 2)

    async def send_quickmessage(self, login: str, text: str) -> dict:
        """ Sends a quickmessage to an email holder """
        if not self.sid:
            raise exceptions.NotLoggedIn()
        results_raw = await self.post(
            self.jsonrpc(
                [
                    [1, "set_session", {"session_id": self.sid}],
                    [2, "set_focus", {"object": "messenger"}],
                    [3, "send_quick_message", {
                        "login": login, "text": text, "import_session_file": 0}],
                ]
            )
        )
        results = [Box(res) for res in results_raw]
        if not results[-1].result["return"] == "OK":
            raise exceptions.error_handler(
                results[-1].result.errno)(results_raw[-1]["result"])
        return self.pack_responses(results_raw, 2)

    async def get_quickmessage_history(self, start_id: int) -> dict:
        """ get quickmessage history """
        if not self.sid:
            raise exceptions.NotLoggedIn()
        results_raw = await self.post(
            self.jsonrpc(
                [
                    [1, "set_session", {"session_id": self.sid}],
                    [2, "set_focus", {"object": "messenger"}],
                    [3, "get_history", {
                        "start_id": start_id, "export_session_file": 0}],
                ]
            )
        )
        results = [Box(res) for res in results_raw]
        if (not results[-1].result["return"] == "OK") and (results[-1].result.errno == "107" or results[-1].result.errno == "103"):
            raise exceptions.error_handler(
                results[-1].result.errno)(results_raw[-1]["result"])
        return self.pack_responses(results_raw, 2)

    async def group_lernsax_quickmessage_history_by_chat(self, quickmsg_history: list):
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
                grouped_messages[receiving_chat_email].messages.append(
                    new_message)
            else:
                # By async default the messages in the quickmessage history should be sorted by date. If there is a mistake in the sorting
                # those statements are called.
                current_index = 0
                for existing_msg in grouped_messages[receiving_chat_email].messages:
                    if existing_msg.date >= msg.date:
                        grouped_messages[receiving_chat_email].messages.insert(
                            current_index, new_message)
                        break

                    current_index += 1
        return grouped_messages.to_dict()
