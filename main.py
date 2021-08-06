from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from private import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(msg: types.Message):
    if msg.from_user.username == 'akulaalexa':
        await msg.answer(f'Здарова, Мать')
    elif msg.from_user.username == 'bzglve':
        await msg.answer(f'Приветствую вас хозяин')
    else:
        await msg.answer(f'Че надо псина?')


@dp.message_handler(content_types=['text'])
async def get_text_messages(msg: types.Message):
    if msg.text.lower() == 'привет':
        await msg.answer('Привет!')
    else:
        if msg.from_user.username == 'bzglve':
            await msg.answer('Хозяин, извните, но я пока не умею отвечать на это сообщение')
        elif msg.from_user.username == 'akulaalexa':
            await msg.answer('Мать, я пока что тупой, поэтому спроси хозяина, когда он меня допилит, окич?')
        else:
            await msg.answer('Ты осёл\nПо русски блин нахрен говори\nВ России жиш нахрен живешь блин')
        await bot.send_sticker(msg.chat.id, 'CAACAgIAAxkBAAECsYJhC_2UuwxnuNU84Spgx12ZzLTeEgACXQEAAj0N6AQo0z0f9lB-ZSAE')


if __name__ == '__main__':
    executor.start_polling(dp)
