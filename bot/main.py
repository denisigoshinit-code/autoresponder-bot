# bot/main.py
from server import run_http_server  
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from dotenv import load_dotenv

# Загружаем .env
load_dotenv()

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Импортируем обработчики
from bot.handlers import start, messages, feedback

async def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        logger.error("❌ BOT_TOKEN не найден в .env")
        return

    # ✅ Исправлено: parse_mode теперь через DefaultBotProperties
    bot = Bot(
        token=token,
        default=None  # можно убрать, aiogram сам подставит
    )
    bot.default.parse_mode = ParseMode.HTML  # или установите глобально

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Подключаем роутеры
    dp.include_router(start.router)
    dp.include_router(messages.router)
    dp.include_router(feedback.router)

    # Устанавливаем команды
    await bot.set_my_commands([
        BotCommand(command="start", description="Начать"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="feedback", description="Связаться с менеджером")
    ])

    logger.info("✅ Бот запущен и готов к работе")
    run_http_server()  # ← Запускаем сервер
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен вручную")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")