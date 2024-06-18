import re
import asyncio
from telethon import TelegramClient, events
from config import API_ID, API_HASH, GROUP_ID
from texts import ALL_WORDS, DONT_TAKE

def check_words(text, words):
    return any(re.search(rf'\b\w*{word}\w*\b', text, re.IGNORECASE) for word in words)

client = TelegramClient('userbot_new', API_ID, API_HASH)  # 'userbot_new' - yangi session nomi

@client.on(events.NewMessage)
async def handler(event):
    message = event.message
    if message.is_group and message.chat_id != GROUP_ID:
        if check_words(message.message, DONT_TAKE):
            return  # Agar DONT_TAKE ichidagi so'zlar bo'lsa, funksiyani to'xtatish
        
        if check_words(message.message, ALL_WORDS):
            await asyncio.sleep(5)  # 5 soniya kutish
            try:
                # Habarning hali ham mavjudligini tekshirish
                await client.get_messages(message.chat_id, ids=message.id)
            except:
                return  # Agar habarning mavjud emasligi haqida xatolik bo'lsa, funksiyani to'xtatish
            
            chat_id = event.chat_id
            message_id = message.id
            if str(chat_id).startswith('-100'):
                chat_id_str = str(chat_id)[4:]  # Remove '-100' prefix
            else:
                chat_id_str = str(chat_id)
            
            message_link = f"https://t.me/c/{chat_id_str}/{message_id}"
            sender = await client.get_entity(message.sender_id)  # Foydalanuvchini olish
            sender_link = f"tg://user?id={message.sender_id}"  # Foydalanuvchi uchun link yaratish
            
            text_with_link = f"{message.message}\n\n\n🔗 <a href='{message_link}'>Xabar havolasi</a>\n\n👤 <a href='{sender_link}'>Yuborgan foydalanuvchi</a>"
            await client.send_message(GROUP_ID, message=text_with_link, parse_mode='html')
    elif message.is_private:
        await message.reply(message.message)

client.start()
client.run_until_disconnected()
