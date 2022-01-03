#!/usr/bin/env python

""" LernSucks API Wrapper
"""

import asyncio
from typing import List, Union
import aiohttp
from lernsax.util import ApiClient
import atexit


class Client(ApiClient):
    """ Main object for handling LernSax access and responses. """

    def __init__(self, email: str, password: str) -> None:
        self.email: str = email
        self.password: str = password
        self.sid: str = ""
        self.member_of: List[str] = []
        self.root_url: str = "https://www.lernsax.de"
        self.api: str = f"{self.root_url}/jsonrpc.php"
        self.background: asyncio.Task

    def __await__(self):
        self.background = asyncio.create_task(self.background_task())
        atexit.register(self.__del__)
        return self._init().__await__()

    async def _init(self):
        self._session: aiohttp.ClientSession = aiohttp.ClientSession()
        return self

    def __del__(self):
        try:
            loop = asyncio.get_event_loop()
            loop.create_task(self._close_session())
        except RuntimeError:
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self._close_session())

    async def _close_session(self):
        if not self._session.closed:
            await self._session.close()

    async def post(self, json: Union[dict, str, list]) -> dict:
        async with self._session.post(self.api, json=json) as f:
            return await f.json()

    async def background_task(self) -> None:
        # refresh session every 5 minutes
        while True:
            await asyncio.sleep(60*5)
            print(await self.refresh_session())
