**This project is in no way associated with LernSax, WebWeaver, DigiOnline GmbH or Freistaat Sachsen**

## What is this?

This is an API Wrapper for the LernSax API using aiohttp. Please note that we do not encourage taking any harmful actions against anyone using this wrapper.


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
Use aiodav for async webdav access to LernSax, please refer to [this repo](https://github.com/jorgeajimenezl/aiodav) for more info on aiodav

```
import aiodav
import asyncio

async def main():
    async with Client('https://lernsax.de/webdav.php', login='', password='') as client:
        await client.download_file('/remote/file.zip', 
                                    '/local/file.zip',
                                    progress=progress)
```
