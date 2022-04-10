import logging
import time
import os

from aiogram import Bot, Dispatcher, types, executor

from gtts import gTTS

from keyboards import *

API_TOKEN = ''


logging.basicConfig(level=logging.INFO)

bot = Bot(API_TOKEN)
dp = Dispatcher(bot)

db = {}
langs = {
    "English \U0001F1FA\U0001F1F8": "en",
    "Russian \U0001F1F7\U0001F1FA": "ru",
    "French \U0001F1EB\U0001F1F7": "fr",
    "German \U0001F1E9\U0001f1EA": "de"
}


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    db[message.from_user.id] = {"mode": "started", "lang": ""}
    await message.answer(f"Welcome {message.from_user.first_name}!", reply_markup=start_keyboard())


@dp.message_handler(content_types=["text"])
async def handle(message: types.Message):
    try:
        user = db[message.from_user.id]
        if user['mode'] == "started":
            msg = message.text
            if msg == "Choose language":
                db[message.from_user.id]['mode'] = "lang"
                db[message.from_user.id]['prev'] = "started"
                await message.answer("Please choose language from which you want to make a voice", reply_markup=langs_keyboard())
            elif msg == "Help":
                await message.answer("Here should have been help message, but I hope you can get bot logic without it\U0001F606", reply_markup=start_keyboard())
        elif user['mode'] == "lang":
            if message.text in langs:
                db[message.from_user.id] = {
                    "mode": "default",
                    "lang": langs[message.text],
                }
                await message.answer("New language is set", reply_markup=default_menu())
            elif message.text == "<< Go back":
                if user['prev'] == "started":
                    await message.answer("Back", reply_markup=start_keyboard())
                elif user['prev'] == "default":
                    await message.answer("Back", reply_markup=default_menu())
                db[message.from_user.id]['mode'] = user['prev']
                db[message.from_user.id]['prev'] = ""
        elif user['mode'] == "default":
            msg = message.text
            if msg == "Change language":
                db[message.from_user.id]['prev'] = "default"
                db[message.from_user.id]['mode'] = "lang"
                await message.answer("Select language", reply_markup=langs_keyboard())
            elif msg == "Convert message":
                keyboard = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(types.reply_keyboard.KeyboardButton(text="<< Go back"))
                db[message.from_user.id]['prev'] = "default"
                db[message.from_user.id]['mode'] = "convert"
                await message.answer("Send me the message to convert it to voice", reply_markup=keyboard)
            elif msg == "Help":
                await message.answer("Here should have been help message, but I hope you can get bot logic without it\U0001F606", reply_markup=default_menu())
        elif user['mode'] == "convert":
            msg = message.text
            if msg == "<< Go back":
                db[message.from_user.id]['mode'] = "default"
                db[message.from_user.id]['prev'] = ""
                await message.answer("Back", reply_markup=default_menu())
            else:
                tts = gTTS(message.text, lang=db[message.from_user.id]['lang'])
                filename = str(time.time() * 1000)
                tts.save(filename + ".ogg")
                voice = types.input_file.InputFile(filename+".ogg")
                await message.answer_voice(voice, caption=f"<i>{message.text}</i>", parse_mode="html")
                del voice, tts
                os.remove(filename + ".ogg")
    except KeyError:
        db[message.from_user.id] = {"mode": "started", "lang": ""}
        await message.answer(f"Welcome {message.from_user.first_name}! Please select language", reply_markup=start_keyboard())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
