import apiai, json
# import dialogflow_v2 as dialogflow
from google.cloud import dialogflow_v2 as dialogflow
from google.cloud import storage

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

BOT_TOKEN = ''
SPEECH_TOKEN = ''
PROJECT_ID = ''
SESSION_ID = ''
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(msg: types.Message):
    # await msg.reply_to_message(f'Здарова, Отец, {msg.from_user.first_name}')
    if msg.from_user.username == 'akulaalexa':
        await msg.answer(f'Здарова, Мать')
    elif msg.from_user.username == 'bzglve':
        await msg.answer(f'Приветствую вас хозяин')
    else:
        await msg.answer(f'Че надо псина?')
    print(msg.from_user)


@dp.message_handler(content_types=['text'])
async def get_text_messages(msg: types.Message):
    texts = msg.text
    # request = apiai.ApiAI(SPEECH_TOKEN).text_request()  # Токен API к Dialogflow
    # request.lang = 'ru'  # На каком языке будет послан запрос
    # request.session_id = 'Web client 1'  # ID Сессии диалога (нужно, чтобы потом учить бота)
    # request.query = msg.text.lower()  # Посылаем запрос к ИИ с сообщением от юзера
    # responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    # print(responseJson)
    # response = responseJson['result']['fulfillment']['speech']  # Разбираем

    storage_client = storage.Client()
    buckets = storage_client.list_buckets()
    print(buckets)

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(PROJECT_ID, SESSION_ID)
    print('Session path: {}\n'.format(session))

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code='ru-RU')

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(request={"session": session, "query_input": query_input})

        print('='*20)
        print("Query text: {}".format(response.query_result.query_text))
        print(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )
        print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))

    response = 'SHIT'
    if response:
        if msg.text.lower() == 'привет':
            await msg.answer('Привет!')
        else:
            if msg.from_user.username == 'bzglve':
                await msg.answer('Хозяин, извните, но я пока не умею отвечать на это сообщение')
            elif msg.from_user.username == 'akulaalexa':
                await msg.answer('Мать, я пока что тупой, поэтому спроси хозяина, когда он меня допилит, окич?')
            else:
                # await msg.answer('Ты осёл\nПо русски блин нахрен говори\nВ России жиш нахрен живешь блин')
                await msg.answer(response)
            # await bot.send_sticker(msg.chat.id, 'CAACAgIAAxkBAAECsYJhC_2UuwxnuNU84Spgx12ZzLTeEgACXQEAAj0N6AQo0z0f9lB-ZSAE')


if __name__ == '__main__':
    executor.start_polling(dp)
