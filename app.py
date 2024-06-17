import re
from telethon import TelegramClient, events
from config import API_ID, API_HASH, GROUP_ID
from texts import ALL_WORDS

def check_words(text, words):
    return any(re.search(rf'\b\w*{word}\w*\b', text, re.IGNORECASE) for word in words)

client = TelegramClient('userbot_new', API_ID, API_HASH)  # 'userbot_new' - yangi session nomi

@client.on(events.NewMessage)
async def handler(event):
    message = event.message
    if message.is_group and check_words(message.message, ALL_WORDS):
        sender = await event.get_sender()
        if sender:
            user_link = f'<a href="tg://user?id={sender.id}">{sender.first_name}</a>'
            text_with_link = f"{message.message}\n\n👤 <b>{user_link}</b>"
            await client.send_message(GROUP_ID, text_with_link, parse_mode='html')
        else:
            text_with_link = f"{message.message}\n\n👤 <b>Anonim foydalanuvchi</b>"
            await client.send_message(GROUP_ID, text=text_with_link, parse_mode='html')
    elif message.is_private:
        await message.reply(message.message)

client.start()
client.run_until_disconnected()
