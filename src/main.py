from aiogram import executor
from telegram.bot import dp
from parser import check_fresh_tasks
from database import Base, engine

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    check_fresh_tasks()
    executor.start_polling(dispatcher=dp)
