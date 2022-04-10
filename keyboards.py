from aiogram import types


def start_keyboard():
    keyboard = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.reply_keyboard.KeyboardButton(text="Choose language"))
    keyboard.add(types.reply_keyboard.KeyboardButton(text="Help"))
    return keyboard


def default_menu():
    keyboard = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.reply_keyboard.KeyboardButton(text="Convert message"))
    keyboard.add(types.reply_keyboard.KeyboardButton(text="Change language"))
    keyboard.add(types.reply_keyboard.KeyboardButton(text="Help"))
    return keyboard


def langs_keyboard():
    keyboard = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.reply_keyboard.KeyboardButton(text="English \U0001F1FA\U0001F1F8"))
    keyboard.add(types.reply_keyboard.KeyboardButton(text="Russian \U0001F1F7\U0001F1FA"))
    keyboard.add(types.reply_keyboard.KeyboardButton(text="French \U0001F1EB\U0001F1F7"))
    keyboard.add(types.reply_keyboard.KeyboardButton(text="German \U0001F1E9\U0001f1EA"))
    keyboard.add(types.reply_keyboard.KeyboardButton(text="<< Go back"))
    return keyboard
