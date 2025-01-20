from aiogram import Bot, Dispatcher, executor, types  # aiogram: Библиотека для создания Telegram-ботов.
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # Хранилище для состояний пользователя в памяти.
from aiogram.dispatcher.filters.state import State, StatesGroup  # Классы для управления состояниями пользователя.
from aiogram.dispatcher import FSMContext  # Контекст для работы с состояниями.
import asyncio  # Библиотека для асинхронного программирования.
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

api = ""  # Токен API бота.
bot = Bot(token=api)  # Объект бота, инициализированный с токеном API.
dp = Dispatcher(bot, storage=MemoryStorage())  # Диспетчер, который управляет обработкой сообщений и состояниями.


kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button1)
kb.add(button2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# Обработчик команды /start:Когда пользователь отправляет команду /start, бот отправляет приветственное сообщение.
@dp.message_handler(commands=['start'])
async def send_welcome(message):
    await message.reply("Привет!Я бот помогающий твоему здоровью.", reply_markup=kb)


# Обработчик текста 'Calories': Когда пользователь отправляет сообщение 'Calories',
# бот запрашивает возраст и устанавливает состояние age.
@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await  UserState.age.set()


# Обработчик состояния age: Когда пользователь вводит возраст, бот сохраняет его в состоянии и
# запрашивает рост, устанавливая состояние growth.
@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


# Обработчик состояния growth: Когда пользователь вводит рост, бот сохраняет его в состоянии и
# запрашивает вес, устанавливая состояние weight.
@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await  UserState.weight.set()


# Обработчик состояния weight: Когда пользователь вводит вес, бот сохраняет его в состоянии,
# извлекает все данные (возраст, рост, вес) и рассчитывает суточную норму калорий по формуле.
@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await  state.get_data()

    age = float(data['age'])
    growth = float(data['growth'])
    weight = float(data['weight'])

    form_ = 10 * weight + 6.25 * growth - 5 * age + 5
    # Затем бот отправляет результат пользователю и завершает состояние.
    await message.answer(f'Ваша норма калорий: {form_:.2f} ккал/день')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)