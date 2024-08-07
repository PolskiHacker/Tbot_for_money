import configparser
from aiogram import Router, types
from aiogram.filters import Command
from keybords.create_keybord import new_keybord

router = Router()
con = configparser.ConfigParser()
con.read('data/help_info.ini', encoding='utf-8')


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(con["Help"]["help_s"], reply_markup=new_keybord(), parse_mode='HTML')


@router.message(Command("help"))
async def cmd_hello(message: types.Message):
    await message.answer(con["Help"]["help"], parse_mode='HTML')


@router.message(Command("info"))
async def help_info(message: types.Message):
    await message.answer(con["Info"]["info"], parse_mode='HTML')