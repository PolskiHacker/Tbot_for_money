import re
from aiogram import types
from aiogram.filters import BaseFilter
from typing import Union, Dict, Any
from parsing_bd.DB_func import all_names


class IsDate(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return bool(re.search(r'^\d{2}\.\d{2}\.\d{4}$', message.text))


class SearchDate(BaseFilter):
    async def __call__(self, message: types.Message) -> Union[bool, Dict[str, Any]]:
        pattern = r'(.+?)\s(\d{2}\.\d{2}\.\d{4}-\d{2}\.\d{2}\.\d{4}|\d{2}\.\d{2}\.\d{4}|\d{4}-\d{4}|\d{4})$'
        pattern2 = r'^(\d{2}\.\d{2}\.\d{4}-\d{2}\.\d{2}\.\d{4}|\d{2}\.\d{2}\.\d{4}|\d{4}-\d{4}|\d{4})$'
        a = {"data": []}
        for text in message.text.split(', '):
            if len(text.split(' ')) > 1:
                match = re.search(pattern, text)
            else:
                match = re.search(pattern2, text)
            if match:
                if len(match.groups()) == 2:
                    a["data"].append([match.group(1).strip(), match.group(2).strip()])
                else:
                    a["data"].append(match.group(1).strip())
            else:
                if text.lower() in all_names():
                    a["data"].append(text)
                else:
                    return False
        return a


class KeyCheckFilter(BaseFilter):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    async def __call__(self, message: types.Message) -> bool:
        return self.key[-1] == self.value
