import logging
import os
import time
import telebot
from datetime import datetime
from google_api import add_data_to_sprsh, create_sheet_template, send_email
from telebot import types
from typing import Any, Optional, Union
from content_maker import *

logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(levelname)s - %(asctime)s -'
           ' %(threadName)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S', level=logging.WARNING
)

with open('bot_token') as tfile:
    token: str = tfile.read()
bot: telebot = telebot.TeleBot(token)


class User:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.phone: Optional[Union[str, int]] = None
        self.email: Optional[str] = None
        self.course: Optional[str] = None

    def __repr__(self) -> str:
        return f"User: {self.name}, {self.phone}, {self.email}, {self.course}"


temp_users: Dict[str, User] = {}
if not os.path.exists("users.csv"):
    with open("users.csv", "w") as file:
        file.write(
            "chat_id, user_id, name, phone, email, course, creation_datetime, "
            "email_status, email_sent_datetime\n"
        )


@bot.message_handler(commands=["start", "help"])
def start(message: types.Message) -> None:
    bot.send_message(
        chat_id=message.chat.id,
        text="Привет! Я T-English–бот.\n"
             "Помогу узнать о наших курсах, "
             "отправить твою заявку, "
             "чтобы записаться на пробное занятие, и дам доступ "
             "к бесплатным материалам!",
        reply_markup=make_menu_buttons(2, main_menu_buttons),
        parse_mode="HTML",
    )


@bot.message_handler(commands=["apply"])
def apply(message: types.Message) -> None:
    bot.send_message(
        chat_id=message.chat.id, text="Как мы можем к тебе обращаться? "
    )

    bot.register_next_step_handler(message, process_name_step)


def process_name_step(message: types.Message) -> None:
    user: User = User(message.text)
    temp_users[message.chat.id] = user

    reply_markup = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True
    )
    contact_keyboard = types.KeyboardButton(
        text=f"{phone_icon} Отправить мой номер телефона", request_contact=True
    )
    reply_markup.add(contact_keyboard)

    bot.send_message(
        chat_id=message.chat.id,
        text=f"{user.name}, укажи твой номер телефона или "
             "поделись им, нажав кнопку ниже:",
        reply_markup=reply_markup,
    )

    bot.register_next_step_handler(message, process_phone_step)


def process_phone_step(message: types.Message) -> None:
    try:
        user: User = temp_users[message.chat.id]
    except KeyError:
        bot.send_message(
            chat_id=message.chat.id, text=f"Извини, что-то пошло не так"
        )
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        start(message)
        return
    try:
        user.phone = message.json["text"]
    except KeyError:
        try:
            user.phone = message.json["contact"]["phone_number"]
        except KeyError:
            user.phone = None
    reply_markup = types.ReplyKeyboardRemove()
    bot.send_message(
        chat_id=message.chat.id,
        text=f"{user.name}, укажи твой email: ",
        reply_markup=reply_markup,
    )
    bot.register_next_step_handler(message, process_email_step)


def process_email_step(message: types.Message) -> None:
    try:
        user = temp_users[message.chat.id]
    except KeyError:
        bot.send_message(
            chat_id=message.chat.id, text=f"Извини, что-то пошло не так"
        )
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        start(message)
        return

    user.email = message.text

    bot.send_message(
        chat_id=message.chat.id,
        text=f"Выбери интересующий тебя курс:",
        reply_markup=make_menu_buttons(2, courses_buttons_choose),
    )
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call: Any) -> None:
    if call.data == "main_menu":
        start(call.message)

    if call.data == "courses":
        bot.send_message(
            chat_id=call.message.chat.id,
            text=f"Выбери интересующий тебя курс:",
            reply_markup=make_menu_buttons(2, courses_buttons),
        )

    if call.data == "resources":
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Выбери интересующий тебя ресурс: ",
            reply_markup=make_resources_buttons(3, resources_buttons),
        )

    if call.data == "leave_application":
        try:
            del temp_users[call.message.chat.id]
        except KeyError:
            pass
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        apply(call.message)

    if call.data in COURSES.keys():
        bot.send_message(
            chat_id=call.message.chat.id,
            text=COURSES[call.data],
            reply_markup=make_menu_buttons(2, one_course_buttons),
        )

    if call.data[0:-3] in COURSES.keys() or call.data == "Не уверен|ch":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=balloon_icon)

        try:
            user: User = temp_users[call.message.chat.id]
        except KeyError:
            bot.send_message(
                chat_id=call.message.chat.id,
                text=f"Извини, что-то пошло не так"
            )
            bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
            start(call.message)
            return

        user.course = call.data.split("|")[0]
        bot.send_message(
            chat_id=call.message.chat.id,
            text=f"Это твои данные?\n"
                 f"Имя: {user.name},\n"
                 f"Телефон: {user.phone},\n"
                 f"Email: {user.email},\n"
                 f"Курс: {user.course}",
            reply_markup=make_menu_buttons(2, finish_buttons),
        )
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)

    if call.data == "apply_no":
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=None,
        )

        bot.send_message(
            chat_id=call.message.chat.id,
            text="Пожалуйста, заполни заявку еще раз:"
        )
        try:
            del temp_users[call.message.chat.id]
        except KeyError:
            bot.send_message(
                chat_id=call.message.chat.id,
                text="Извини, сначала надо заполнить заявку!",
                reply_markup=make_menu_buttons(
                    1, home_apply_buttons,
                ),
            )
            return
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        apply(call.message)

    if call.data == "apply_yes":
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=None,
        )
        try:
            user_to_write: Dict[str, str] = {
                "Telegram_id": f"@{call.message.chat.username}",
                "Имя пользователя": f"{temp_users[call.message.chat.id].name}",
                "Телефон": f"{temp_users[call.message.chat.id].phone}",
                "email": f"{temp_users[call.message.chat.id].email}",
                "Желаемый курс": f"{temp_users[call.message.chat.id].course}",
                "Время создания заявки":
                    f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}',
            }
            bot.send_message(
                chat_id=call.message.chat.id,
                text="Спасибо, твоя заявка принята!\n"
                     "В ближайшее время мы свяжемся с тобой!",
                reply_markup=make_menu_buttons(
                    1, single_home_button
                ),
            )
            if not os.path.exists("google_api/sprsh_link.txt"):
                current_sheet: Optional[
                    Dict[str, str]
                ] = create_sheet_template()
                logging.warning('Created new spreadsheet')
            else:
                with open("google_api/sprsh_link.txt", "r") as s_file:
                    data: List[str] = s_file.readlines()[-1].split(" | ")
                    current_sheet = {
                        "spreadsheet_id": data[0], "sheet_name": data[1]
                    }

            if add_data_to_sprsh(user_to_write, current_sheet):
                logging.info('data successfully written to spreadsheet')
            else:
                current_sheet = create_sheet_template()
                if add_data_to_sprsh(user_to_write, current_sheet):
                    logging.info("data successfully written to spreadsheet")
                else:
                    logging.error("failed to write data to spreadsheets")

            with open("users.csv", "a") as f:
                f.write(
                    f"{call.message.chat.id}, "
                    f'{", ".join([item for item in user_to_write.values()])}'
                )
            with open("google_api/sprsh_link.txt", "r") as s_file:
                sprsh_link: str = s_file.readlines()[-1].split(" | ")[-1]

            if send_email(
                    "Новая заявка от бота!",
                    "\n".join(
                        [f"{item}  |  {value}" for
                         item, value in user_to_write.items()]
                    ) + f"\nФайл заявок - {sprsh_link}"
            ):
                with open("users.csv", "a") as f:
                    f.write(
                        ", email sent successfully! , "
                        f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n'
                    )
            else:
                logging.warning('could not send email')
                with open("users.csv", "a") as f:
                    f.write(
                        ", !COULD NOT SEND EMAIL!, "
                        f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n'
                    )
            bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
            del temp_users[call.message.chat.id]
        except KeyError:
            bot.send_message(
                chat_id=call.message.chat.id,
                text="Извини, сначала надо заполнить заявку!",
                reply_markup=make_menu_buttons(
                    1, home_apply_buttons
                ),
            )
            return


while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=0)
    except Exception as e:
        logging.error(f'Error "{e}" in main app', exc_info=True)
        time.sleep(2)
        continue
