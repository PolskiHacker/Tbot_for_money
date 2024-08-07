from aiogram import Router, F
from typing import Union, List, Any
from aiogram.types import Message, BufferedInputFile
from Filters.date_filter import IsDate, SearchDate, KeyCheckFilter
from parsing_bd.DB_func import take_current_day_info, all_names, search, new_graph, check_graph


router = Router()
key = [0]


@router.message(F.text == "курсы за число")
async def today_prices(message: Message):
    await message.answer("Введите дату за которую хотите увидеть курсы валют")


@router.message(IsDate())
async def take_date(message: Message):
    data = take_current_day_info(message.text)
    if data:
        await message.answer(data, parse_mode='HTML')


@router.message(F.text == "все названия")
async def all_currency_names(message: Message):
    data = all_names()
    text = "Всё, что я нашел:\n"
    for i, j in enumerate(data, start=1):
        text += f"{i}) {j}\n"
    await message.answer(text)


@router.message(F.text == "поиск")
async def currency_search(message: Message):
    key.append(1)
    await message.answer("Введите запрос в следующем формате: (название валюты) (дата)\n"
                         "Датой может быть: конкретная дата или промежуток в полном формате либо только год\n"
                         "И дата и название выстапают не обязательными параметрами, то есть без даты будут выведены "
                         "цены за валюту за все время")


@router.message(SearchDate(), KeyCheckFilter(key=key, value=1))
async def searching(message: Message, data: Union[str, List[str]]):
    info = search(data[0])
    if len(info) == 0:
        await message.answer("Возможно вы ввели что то не так")
        return
    tmp = info[0][4]
    text = f"<u>{tmp}</u>\n"
    for i, j in enumerate(info, start=1):
        if j[4] != tmp:
            tmp = j[4]
            text += f"<u>{tmp}</u>\n"
        if j[2] == 1:
            text += f"{i}) {j[0]}: <b>1</b> единица этой валюты стоит <b>{j[3]}₽</b>\n"
        else:
            text += f"{i}) {j[0]}: <b>{j[2]}</b> единиц этой валюты стоят <b>{j[3]}₽</b>\n"
    key.append(0)
    if len(text) <= 4096:
        await message.answer(text, parse_mode='HTML')
    else:
        data = []
        temp = ''
        for i in range(len(text)):
            if i > 4000 + 4000 * len(data) and text[i - 1:i] == "\n":
                temp += text[i]
                data.append(temp)
                temp = ''
            else:
                temp += text[i]
        data.append(temp)
        for mes in data:
            await message.answer(mes, parse_mode='HTML')


@router.message(F.text == "построить график")
async def paint_graph(message: Message):
    key.append(2)
    await message.answer("Вводить запрос надо также как и при поиски, "
                         "но название валюты обязательно и можно через запятую указать несколько валют")


@router.message(SearchDate(), KeyCheckFilter(key=key, value=2))
async def painting(message: Message, data: Union[str, List[Any]]):
    key.append(0)
    im_data = check_graph(message.text)
    if im_data:
        await message.answer_photo(BufferedInputFile(im_data[1], filename='graph.png'))
    else:
        file = new_graph(message.text, data)
        await message.answer_photo(BufferedInputFile(file, filename='graph.png'))
