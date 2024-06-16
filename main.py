import re
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, GROUP_ID
from texts import ALL_WORDS

# Funktsiya, regulyar ifoda orqali so'zni tekshiradi
def check_words(text, words):
    return any(re.search(rf'\b\w*{word}\w*\b', text, re.IGNORECASE) for word in words)

app = Client("my_account", api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.chat(GROUP_ID) & filters.text)
async def bot_echo(client, message: Message):
    if check_words(message.text, ALL_WORDS):
        user_link = f'<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>'
        text_with_link = f"{message.text}\n\n👤<b>{user_link}</b>"
        await client.send_message(chat_id=GROUP_ID, text=text_with_link, parse_mode='html')

app.run()
