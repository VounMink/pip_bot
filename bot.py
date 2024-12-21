import asyncio
import asyncpg
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties

import config
import db

TOKEN = config.BOT_TOKEN

dp = Dispatcher()

kb = [
    [
        KeyboardButton(text='Мои списки')
    ]
]

keyboard__my_lists = ReplyKeyboardMarkup(
    keyboard=kb,
    resize_keyboard=True
)

pip_user = 0
conn = 0

class PIP_user:
    
    def __init__(self, PIP_user_id):
        self.PIP_user_id = str(PIP_user_id)
        # self.conn = 0

    # async def __call__(self):
    #     print('Call')
    #     await self.PIP__conn_db()

    # async def PIP__conn_db(self):
    #     print(1)
    #     self.conn = await asyncpg.connect(user=db.USER, password=db.PASSWORD, database=db.DATABASE, host=db.HOST)
    
    async def PIP__existence_user(self):
        conn = asyncpg.connect(user=db.USER, password=db.PASSWORD, database=db.DATABASE, host=db.HOST)
        user_record = await conn.fetch('SELECT * FROM pip_users WHERE ident_id = ' + self.PIP_user_id)

        if len(user_record) == 0:
            await conn.fetch('INSERT INTO pip_users (ident_id) VALUES ('+ self.PIP_user_id +')')

        # await conn.close()

    async def PIP__user_lists(self):
        user_lists = await conn.fetch('SELECT * FROM pip_user_lists WHERE ident_id = ' + self.PIP_user_id)

        if len(user_lists) == 0:
            return 0
        else:
            return len(user_lists)


class FilteringMessage:
    def __init__(self, my_text: str):
        self.my_text = my_text
    
    async def __call__(self, message: Message):
        return message.text == self.my_text

@dp.message(CommandStart())
async def command_start_handler(message: Message):
    pip_user = PIP_user(message.from_user.id)

    await pip_user.PIP__existence_user()
    await message.reply('Салют!',reply_markup=keyboard__my_lists)

@dp.message(FilteringMessage('Мои списки'))
async def my_lists(message: Message):
    user_lists = await pip_user.PIP__user_lists()
    await message.answer(user_lists)

# @router.message(Command("start"))
# def start(msg: Message) -> None:
#     # user = PIP_user(msg.chat.id)
#     msg.reply('Салют!')

async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)
#     bot = Bot(token=config.BOT_TOKEN)
#     dp = Dispatcher(storage=MemoryStorage())
#     dp.include_router(router)
#     bot.delete_webhook(drop_pending_updates=True)
#     dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())