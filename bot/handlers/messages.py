import json  # ← добавлено
from aiogram import Router, F
from aiogram.types import Message
import logging
from bot.utils import load_faq

router = Router()
logger = logging.getLogger(__name__)

faq_cache = None

async def get_faq():
    global faq_cache
    if faq_cache is None:
        faq_cache = load_faq()
    return faq_cache

@router.message(F.text)
async def handle_message(message: Message):
    user = message.from_user
    text = message.text.strip().lower() if message.text else ""
    
    full_name = user.full_name or "Аноним"
    username = f"@{user.username}" if user.username else "не указан"
    
    logger.info(f"Сообщение от {full_name} ({username}): {text}")

    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as e:
        logger.error(f"Ошибка загрузки config.json: {e}")
        return

    if any(spam in text for spam in config["spam_keywords"]):
        await message.reply("❌ Сообщение отклонено.")
        return

    faq = await get_faq()
    for keyword, response in faq.items():
        if keyword in text:
            await message.reply(response)
            return

    try:
        with open(".env", "r") as f:
            env_data = f.read()
        admin_id = env_data.split("ADMIN_ID=")[1].strip().split("\n")[0]
    except Exception as e:
        logger.error("ADMIN_ID не найден в .env")
        return

    forward_msg = (
        f"📨 <b>Новое сообщение</b>\n"
        f"От: {full_name} ({username})\n"
        f"Текст: {text}"
    )

    try:
        await message.bot.send_message(
            chat_id=admin_id,
            text=forward_msg,
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Не удалось отправить админу: {e}")

    await message.reply("Спасибо! Я передал ваше сообщение менеджеру.")