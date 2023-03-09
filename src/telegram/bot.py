from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from .config import token
from parser import subjects, difficulties
from models import Task

bot = Bot(token=token)
dp = Dispatcher(bot=bot)

@dp.message_handler(commands='start')
async def start(message: types.Message) -> None:
    start_buttons = ['Сложность задачи', 'Тема задачи']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Выбрать задачу', reply_markup=keyboard)

@dp.message_handler(Text(equals='Тема задачи'))
async def task_topic(message: types.Message) -> None:
    await message.answer('Выберите тему задачи: ' + ', '.join(sorted(subjects)))

@dp.message_handler(Text(equals='Сложность задачи'))
async def task_difficulty(message: types.Message) -> None:
    await message.answer('Выберите сложность задачи: ' + ', '.join([str(dif) for dif in sorted(difficulties)]))

@dp.message_handler(lambda message: message.text in subjects)
async def task_topic_message(message: types.Message) -> None:
    for task in Task.filter_topic_data(message.text):
        await message.answer(task)

@dp.message_handler(lambda message: int(message.text) in difficulties)
async def task_difficulty_message(message: types.Message) -> None:
    for task in Task.filter_difficulty_data(int(message.text)):
        await message.answer(task)

@dp.message_handler(lambda message: message.text)
async def task_difficulty_message(message: types.Message) -> None:
    await message.answer('Я не понимаю к чему относится ваше сообщение')
