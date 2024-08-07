import configparser
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder



def new_keybord() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    config = configparser.ConfigParser()
    config.read('data/buttons.ini', encoding='utf-8')
    for button in config["Buttons"]["buttons"].split(","):
        builder.add(KeyboardButton(text=button.strip()))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)