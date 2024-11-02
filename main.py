import os

from discord import Intents, Client, Message, TextChannel
from dotenv import load_dotenv
from responses import get_response

load_dotenv()

TOKEN: str = os.getenv("TOKEN")
intents: Intents = Intents.default()
intents.message_content = True # NOQA
client: Client = Client(intents=intents)

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("Message empty cuz intent not enable probably")

    if is_private := user_message[0] == "?":
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

@client.event
async def on_ready() -> None:
    print(f"{client.user} has connected to Discord!")

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = message.author.name
    user_message: str = message.content
    channel: TextChannel = message.channel
    print(f"[{channel.name}] {username}: {user_message}")
    await send_message(message, user_message)

def main() -> None:
    client.run(TOKEN)

if __name__ == "__main__":
    main()