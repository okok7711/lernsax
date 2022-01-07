import lernsax
import asyncio

async def main():
    client = await lernsax.Client(
        email="",
        password=""
    )
    await client.login(client.email, client.password)
    print(client.member_of)

asyncio.get_event_loop().run_until_complete(main())