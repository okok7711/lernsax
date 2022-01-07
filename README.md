**This project is in no way associated with LernSax, WebWeaver, DigiOnline GmbH or Freistaat Sachsen**

## What is this?

This is an API Wrapper for the LernSax API using aiohttp. Please note that we do not encourage taking any harmful actions against anyone using this wrapper.

## Installation
LernSax is available on pip!
`pip install lernsax`
You can also install directly from the repo via
`python -m pip install git+https://github.com/okok7711/lernsax.git`


## Documentation?
Basic Documentation, generated with pdoc, for this module is available [here](https://okok7711.github.io/lernsax/)
For Documentation of the actual LernSax jsonrpc API you should probably still stick to  [this repo](https://github.com/TKFRvisionOfficial/lernsax-webweaver-api-research)

## Example Usage
```
import lernsax
import asyncio

async def main():
    client = await lernsax.Client(
    email="",
    password=""
    )
    await client.login(client.email, client.password)
    print(await client.get_emails("494e424f58"))

asyncio.get_event_loop().run_until_complete(main())
```

## Accessing Files via WebDav
This module has built-in support for WebDav via aiodav \
just use the lernsax.Client() class the same as if it was the aiodav.Client().\
visit [this repo](https://github.com/jorgeajimenezl/aiodav) for more info and examples for aiodav\
\
Example (as in [the examples dir](https://github.com/okok7711/lernsax/tree/main/examples)):
```
import lernsax
import asyncio

async def main():
    client = await lernsax.Client(
        email="",
        password=""
    )
    await client.login(client.email, client.password)
    dirs = await client.list()
    print(dirs)

asyncio.get_event_loop().run_until_complete(main())
```
