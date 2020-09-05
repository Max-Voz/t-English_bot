from telebot import types
from typing import List


def make_menu_buttons(
        row_w: int, menu_array: List[List[str]]) -> types.InlineKeyboardMarkup:
    """
    :param row_w: quantity of items in row
    :param menu_array: has to come in the next format:
                      [[text, callback data], [text, callback data]]
    :return: returns ready markup
    """

    markup = types.InlineKeyboardMarkup(row_width=row_w)
    markup.add(
        *[
            types.InlineKeyboardButton(
                text=f"{item[0]}", callback_data=f"{item[1]}"
            )
            for item in menu_array
        ]
    )
    return markup


def make_resources_buttons(
        row_w: int, menu_array: List[List[str]]) -> types.InlineKeyboardMarkup:
    """
    :param row_w: quantity of items in row
    :param menu_array: has to come in the next format:
                      [[text, url], [text, url]....[text, callback]]
    :return: returns ready markup with all items as urls and last with callback
    """
    markup = types.InlineKeyboardMarkup(row_width=row_w)
    markup.add(
        *[
            types.InlineKeyboardButton(text=f"{item[0]}", url=f"{item[1]}")
            for item in menu_array[0:3]
        ]
    )
    markup.add(
        types.InlineKeyboardButton(
            text=f"{menu_array[-1][0]}", callback_data=f"{menu_array[-1][1]}"
        )
    )
    return markup
