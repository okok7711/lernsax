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