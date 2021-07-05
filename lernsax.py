#!/usr/bin/env python

""" LernSucks API Wrapper
"""

# Standard library
from lernsax.util import ApiClient
from typing import List, Union

# 3rd-party dependencies
import aiohttp
import asyncio

# Package modules

class Client(ApiClient):
    """ Main object for handling LernSax access and responses. """
    def __init__(self, email: str, password: str) -> None:
        self.email: str = email
        self.password: str = password
        self.sid: str = ""
        self.member_of: List[str] = []
        self.root_url: str = "https://www.lernsax.de"
        self.api: str = f"{self.root_url}/jsonrpc.php"
    def __await__(self):
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