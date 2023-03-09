from aiogram import executor
from telegram.bot import dp
from database import Base, engine

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    executor.start_polling(dispatcher=dp)
