import re
import asyncio
from telethon import TelegramClient, events
from config import API_ID, API_HASH, GROUP_ID
from texts import ALL_WORDS, DONT_TAKE


def check_words(text, words):
    return any(re.search(rf'\b\w*{word}\w*\b', text, re.IGNORECASE) for word in words)
# 🆔


def contains_emoji(text):
    emoji_pattern = re.compile(
        r'[\U0001F600-\U0001F64F]|'  # Emoticons
        r'[\U0001F300-\U0001F5FF]|'  # Symbols & Pictographs
        r'[\U0001F680-\U0001F6FF]|'  # Transport & Map Symbols
        r'[\U0001F700-\U0001F77F]|'  # Alchemical Symbols
        r'[\U0001F780-\U0001F7FF]|'  # Geometric Shapes Extended
        r'[\U0001F800-\U0001F8FF]|'  # Supplemental Arrows-C
        r'[\U0001F900-\U0001F9FF]|'  # Supplemental Symbols and Pictographs
        r'[\U0001FA00-\U0001FA6F]|'  # Chess Symbols
        r'[\U0001FA70-\U0001FAFF]|'  # Symbols and Pictographs Extended-A
        r'[\U00002702-\U000027B0]|'  # Dingbats
        r'[\U000024C2-\U0001F251]|'  # Enclosed Characters
        r'[\U0001F900-\U0001F9FF]|'  # Supplemental Symbols and Pictographs
        r'[\U00002600-\U000026FF]',  # Miscellaneous Symbols
        flags=re.UNICODE
    )
    return bool(emoji_pattern.search(text))


client = TelegramClient('userbot_new', API_ID, API_HASH)  # 'userbot_new' - yangi session nomi


@client.on(events.NewMessage)
async def handler(event):
    message = event.message
    if (message.is_group or message.is_channel) and message.chat_id != GROUP_ID:
        if len(message.message) > 100 or contains_emoji(message.message):
            return  # Agar xabar 230 tadan uzun bo'lsa, funksiyani to'xtatish

        if check_words(message.message, DONT_TAKE):
            return  # Agar DONT_TAKE ichidagi so'zlar bo'lsa, funksiyani to'xtatish

        if check_words(message.message, ALL_WORDS):
            await asyncio.sleep(2)  # 2 soniya kutish
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


            user_number = sender.phone if sender.phone else None  # Telefon raqamini olish
            contact_info = f"📞 Aloqa: +{user_number}" if user_number else ""  # Agar telefon raqami mavjud bo'lsa, qo'shish

            if message.sender_id:
                text_with_link = f"<b>📧 Xabar:</b> {message.message}\n\n\n🔗 <a href='{message_link}'>Xabar</a>\n\n👤 <a href='{sender_link}'>Yuborgan foydalanuvchi</a>\n\n<b>{contact_info}</b>"
            else:
                text_with_link = f"<b>📧 Xabar:</b> {message.message}\n\n\n🔗 <a href='{message_link}'>Xabar</a>\n\n<b>{contact_info}</b>"
            await client.send_message(GROUP_ID, message=text_with_link, parse_mode='html')
    elif message.is_private:
        if 'test' in message.message.lower():
            await message.reply("✅ Ishlayapman")

client.start()
client.run_until_disconnected()
