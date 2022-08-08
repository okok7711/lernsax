#!/usr/bin/env python

""" LernSucks API Wrapper
"""

import asyncio
from typing import List, Union
from aiohttp import ClientSession, BasicAuth, ClientResponse
from lernsax.util import ApiClient
import aiodav
from importlib.util import find_spec
from logging import getLogger

from time import asctime

logger = getLogger(__name__)

_ORJSON = find_spec("orjson")

if _ORJSON: import orjson as json
else: import json

class HttpClient(ClientSession):
    def __init__(self, *args, **kwargs) -> None:
        self.api: str = kwargs.pop("api_uri", "https://www.lernsax.de/jsonrpc.php")
        super().__init__(
            *args,
            **kwargs,
            json_serialize= lambda obj, *args, **kwargs: json.dumps(obj).decode() if _ORJSON else json.dumps(obj)
        )
        
    async def request(self, method: str, *args, **kwargs):
        response = await super().request(method, self.api, *args, **kwargs)
        self.log_req(response)
        return response

    @staticmethod
    def log_req(response: ClientResponse):
        logger.debug(
            f"{response.request_info.method} [{asctime()}] -> {response.url}: {response.status} [{response.content_type}]"\
            f"Received Headers: {response.headers}"
            )
        
class Client(ApiClient, aiodav.Client):
    """ Main object for handling LernSax access and responses. """

    def __init__(self, email: str, password: str) -> None:
        self.email: str = email
        self.password: str = password
        self.sid: str = ""
        self.member_of: List[str] = []
        self.background: asyncio.Task = asyncio.create_task(self.background_task())
        
        self.http: HttpClient = HttpClient()
        self.dav_session: HttpClient = HttpClient(
            auth = BasicAuth(self.email, self.password))
        self.dav: aiodav.Client = aiodav.Client(
            'https://www.lernsax.de/webdav.php/', login=self.email, password=self.password, session=self.dav_session)
        
        #* Copying Functions to this client so you don't need to call self.dav.func, higly bogded but it works
        for func in dir(self.dav):
            #* dont overwrite functions that already exist
            if func not in dir(self):
                #* copy the function or attr
                setattr(self, func, getattr(self.dav, func)) 

    async def post(self, json: Union[dict, list]) -> dict:
        return await (await self.http.request("POST", json=json)).json()

    async def exists(self, *args, **kwargs) -> bool:
        """
        Workaroung for LernSax WebDav not passing .exist() checks in aiodav even if the dir exists.
        """
        return True

    async def background_task(self) -> None:
        """
        background task to run cleanup after shutting down and to continuously refresh the sesion
        """
        async def refresher():
            #! refresh session every 5 minutes
            while True:
                if self.sid: print(await self.refresh_session())
                await asyncio.sleep(60*5)
        try:
            await refresher()
        finally:
            await self.__cleanup()
    
    async def __cleanup(self):
        if self.sid: await self.logout()
        if not self.http.closed: await self.http.close()
        if not self.dav_session.closed: await self.dav_session.close()