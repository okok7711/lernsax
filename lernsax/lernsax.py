#!/usr/bin/env python

""" LernSucks API Wrapper
"""

# Standard library
from lernsax.util import client
from typing import List

# 3rd-party dependencies
import aiohttp
import asyncio

# Package modules

class Client(client.ApiClient):
    """ Main object for handling LernSax access and responses. """
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.sid = ""
        self.member_of: List[str] = []
        self.root_url = "https://www.lernsax.de"
        self.api = f"{self.root_url}/jsonrpc.php"
    def __await__(self):
        return self._init().__await__()
    async def _init(self):
        self._session = aiohttp.ClientSession()
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
    async def post(self, json) -> dict:
        async with self._session.post(self.api, json=json) as f:
            return await f.json()