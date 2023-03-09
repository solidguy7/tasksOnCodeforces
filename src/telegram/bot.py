from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from .config import token
from utils import append_params
from parser import difficulties
from models import Task

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

topics = []

class TaskState(StatesGroup):
    difficulty = State()
    topic = State()

@dp.message_handler(commands='start')
async def start(message: types.Message) -> None:
    await message.answer('Выберите сложность для задачи: ' + ', '.join([str(dif) for dif in sorted(difficulties)]))
    await TaskState.difficulty.set()

@dp.message_handler(state=TaskState.difficulty)
async def task_difficulty_message(message: types.Message, state: FSMContext) -> None:
    if not message.text.isdigit() or int(message.text) not in difficulties:
        await message.answer('Что-то пошло не так...')
        return
    await state.update_data(difficulty=message.text)
    for topic in Task.filter_difficulty_data(int(message.text)):
        append_params(topic, topics)
    await message.answer('Выберите тему для задачи: ' + ', '.join(sorted(topics)))
    await TaskState.next()

@dp.message_handler(state=TaskState.topic)
async def task_topic_message(message: types.Message, state: FSMContext) -> None:
    if message.text not in topics:
        await message.answer('Упс... Попробуй ещё раз')
        return
    await state.update_data(topic=message.text)
    data = await state.get_data()
    for task in Task.filter_diff_topic_data(diff=data['difficulty'], topic=data['topic']):
        await message.answer(task)
    await state.finish()

@dp.message_handler(lambda message: message.text)
async def task_unknown_message(message: types.Message) -> None:
    await message.answer('Я не понимаю к чему относится ваше сообщение')
