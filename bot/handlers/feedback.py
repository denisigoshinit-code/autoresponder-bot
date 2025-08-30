import json  # ← добавлено
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

class FeedbackForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_question = State()
    waiting_for_contact = State()

@router.message(Command("feedback"))
async def cmd_feedback(message: Message, state: FSMContext):
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        await state.set_state(FeedbackForm.waiting_for_name)
        await message.answer(config["feedback_prompt"])
    except Exception as e:
        await message.answer("Ошибка загрузки формы.")

@router.message(FeedbackForm.waiting_for_name)
async def feedback_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(FeedbackForm.waiting_for_question)
    await message.answer("Теперь опишите ваш вопрос:")

@router.message(FeedbackForm.waiting_for_question)
async def feedback_question(message: Message, state: FSMContext):
    await state.update_data(question=message.text)
    await state.set_state(FeedbackForm.waiting_for_contact)
    await message.answer("Как с вами связаться (Telegram, email, телефон)?")

@router.message(FeedbackForm.waiting_for_contact)
async def feedback_contact(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user = message.from_user
    full_name = user.full_name or "Аноним"
    username = f"@{user.username}" if user.username else "не указан"

    try:
        with open(".env", "r") as f:
            env_data = f.read()
        admin_id = env_data.split("ADMIN_ID=")[1].strip().split("\n")[0]
    except Exception as e:
        await message.answer("Ошибка отправки. Попробуйте позже.")
        await state.clear()
        return

    bot = message.bot
    feedback_msg = (
        f"📩 <b>Новая обратная связь</b>\n"
        f"Имя: {user_data['name']}\n"
        f"Вопрос: {user_data['question']}\n"
        f"Контакт: {message.text}\n"
        f"От: {username} ({full_name})"
    )

    try:
        await bot.send_message(chat_id=admin_id, text=feedback_msg, parse_mode="HTML")
        await message.answer("Спасибо! Я передал ваше сообщение.")
    except Exception as e:
        await message.answer("Не удалось отправить. Проверьте ID админа.")
    await state.clear()