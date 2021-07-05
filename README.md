**This project is in no way associated with LernSax, WebWeaver, DigiOnline GmbH or Freistaat Sachsen**

## What is this?

This is an API Wrapper for the LernSax API using aiohttp. Please note that we do not encourage taking any harmful actions against anyone using this wrapper.


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

client = lernsax.Client()
client.login("realmail@lernsax.de", "gutePass")
print(client.get_emails("494e424f58"))
```

## WebDAV?
Instead of maintaining the sync version of LernSax.py I will focus on completing the async branch which will have WebDAV access to implement a nicer way to read-/write files