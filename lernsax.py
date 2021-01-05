import requests, json, time
from util import exceptions
from bs4 import BeautifulSoup

# LernSucks API Wrapper


def jsonrpc(list):
    return [
        {"id": k[0],
        "jsonrpc": "2.0",
        "method": k[1],
        "params": k[2]
        }
        for k in list
    ]

class Client:
    def __init__(self, email, password) -> None:
        self.email = email
        self.password = password
        self.sid = ""
        self.api = "https://www.lernsax.de/jsonrpc.php"
    def post(self, json):
        return requests.post(self.api, json=json).json()
    def login(self):
        res = self.post(jsonrpc([[1, "login", {"login": self.email, "password": self.password, "get_miniature": True}], [999, "get_information", {}]]))
        if res[0]["result"]["return"] == "OK":
            self.sid = res[1]["result"]["session_id"]
            return res
        else:
            if res[0]["result"]["errno"] == "107": raise exceptions.AccessDenied(res[0]["result"])
            else: raise exceptions.LoginError(res[0]["result"])
    def getTasks(self):
        res = self.post(jsonrpc([[1,"set_session",  {"session_id": str(self.sid)}], [2, "set_focus", {"object": "trusts"}], [3, "get_url_for_autologin", {"disable_logout": True, "disable_reception_of_quick_messages": True, "enslave_session": True, "locale": "en", "ping_master": 1, "target_url_path": "/wws/105500.php"}]]))
        if res[-1]["result"]["return"] == "OK":
            resHtml = requests.get(res[-1]["result"]["url"], allow_redirects= True).text
            soup = BeautifulSoup(resHtml, "html.parser")
            tasks = soup.find_all('a', attrs={"href": "#", "class": "oc", "data-popup": True})
            return tasks