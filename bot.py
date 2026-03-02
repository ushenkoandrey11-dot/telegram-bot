import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = "8706233018:AAEnGY--F_qJhdaHuRgPp-gDbm6Zu9vcV10"
ADMIN_ID = 1713043427  # твой id

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


# --------- КНОПКИ ---------
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📦 Услуги")],
        [KeyboardButton(text="💰 Прайс")],
        [KeyboardButton(text="📩 Оставить заявку")]
    ],
    resize_keyboard=True
)


# --------- СОСТОЯНИЯ ---------
class Form(StatesGroup):
    name = State()
    phone = State()


# --------- START ---------
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Добро пожаловать! Выберите действие:",
        reply_markup=main_keyboard
    )


# --------- УСЛУГИ ---------
@dp.message(F.text == "📦 Услуги")
async def services(message: Message):
    await message.answer("Мы создаём Telegram-ботов для бизнеса.")


# --------- ПРАЙС ---------
@dp.message(F.text == "💰 Прайс")
async def price(message: Message):
    await message.answer("Стоимость разработки от $50.")


# --------- ЗАЯВКА ---------
@dp.message(F.text == "📩 Оставить заявку")
async def leave_request(message: Message, state: FSMContext):
    await message.answer("Введите ваше имя:")
    await state.set_state(Form.name)


@dp.message(Form.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите ваш номер телефона:")
    await state.set_state(Form.phone)


@dp.message(Form.phone)
async def get_phone(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data["name"]
    phone = message.text

    text = (
        f"📩 Новая заявка!\n\n"
        f"👤 Имя: {name}\n"
        f"📞 Телефон: {phone}"
    )

    await bot.send_message(ADMIN_ID, text)
    await message.answer("✅ Ваша заявка отправлена!")
    await state.clear()


# --------- ЗАПУСК ---------
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())