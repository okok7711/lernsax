**This project is in no way associated with LernSax, WebWeaver, DigiOnline GmbH or Freistaat Sachsen**

## What is this?
This is an API Wrapper for the LernSax API using aiohttp and asyncdav for file access. Please note that we do not encourage taking any harmful actions against anyone using this wrapper.

## Documentation?
There is no documentation just yet. However I would refer you to [this repo](https://github.com/TKFRvisionOfficial/lernsax-webweaver-api-research) for getting a hang of the API.

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
