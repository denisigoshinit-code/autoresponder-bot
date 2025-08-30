from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
import json

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        await message.answer(config["welcome_message"])
    except Exception as e:
        await message.answer("Привет! Готов помочь с автоматизацией.")

@router.message(Command("help"))
async def cmd_help(message: Message):
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        await message.answer(config["help_message"])
    except Exception as e:
        await message.answer("Используйте /start")