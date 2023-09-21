# google spreadsheets = 15XZffPS1tUpE6wOO0riA1Z34X1p6rIzyVm2MCtjFTk0
# token = 6490562332:AAGEYO0zk8PWC2jG-cx7YnrgLcxjtdR2ICM


# измени данный код
# необходимо запрашивать у пользователя категорию анекдотов одну из 5

# В предоставленном коде добавь функционал который связывает наш код бота с google sheets и использует таблицу как базу данных с анекдотами

# в данной базе должно у нас есть 2 листа:
# Лист1 и Лист2


# Добавь данный функционал
# 1.
# 5 inline кнопок для выбора категории анекдота:
# # 1 Анекдоты для друзей
# 2 Анекдоты для <3
# 3 Анекдоты для родителей
# 4 Анекдоты 18+
# 5 Анекдоты для 60+
#
# Добавь данный функционал
# 2.
# Лист1 (главная база данных) там находятся Номер анекдота/Категория анекдота/Сам анекдот
# Номер анекдота: это всегда цифра (>0 int)
# Категорий анекдота 5: 1 Анекдоты для друзей 2 Анекдоты для <3 3 Анекдоты для родителей 4 Анекдоты 18+ 5 Анекдоты для 60+
#
# Пример (Лист1):
# Номер 	Категория анекдота	Анекдот
# 1	Анекдот 18+	Взрослый — это тогда, когда идёшь зимой по улице без шапки и понимаешь, что ты сова.
# 2	Анекдот для друзей	Друзья - это те, кто знает все твои секреты, но все равно любят тебя.
# 3	Анекдот для <3	Самое лучшее чувство - это, когда кто-то делает твой мир ярче и счастливее.
# 4	Анекдот 60+	Жизнь после 60 - это новое приключение каждый день.
# 5	Анекдот для родителей	Родители - это те, кто всегда заботился о вашем будущем.
# ...
# Лист1 является прямым потоком дынных для бота в виде анекдотов по категориям!
# Если пользователь просто хочет получить анекдот то он выбирает /joke
# Затем категорию анекдота
# Затем из базы данных (Лист1) в случайном порядке без повторения ему отправляются анекдоты из категории которую он выбрал
# После каждого отправленного анекдота у пользователя снова появляется (inline меню) с выбором категории анекдота
# Если уникальные анекдоты в категории закончились, тогда пользователю выводится сообщение "Новые анекдоты совсем скоро!"
#
# Добавь данный функционал
# 3.
# Лист2 в нем находятся такие данные Никнейм пользователя / Дата и Время добавления анекдота /Id пользователя / Категория анекдота /Добавленный пользователем анекдот
# Когда пользователь хочет добавить анекдот /create ( анекдот попадает в лист номер 2 где хранится в общей таблице)


# Появляется меню из трех кнопок Inline (подключенные к самому анекдоту

# пример:
# Анекдот 1

# Оценка анекдота:
# Отлично | Нормально | Плохо
# где Отлично, Нормально, Плохо это inline кнопки


# после оценки пользователя данная оценка попадает в табличку google sheets list 1


# так же необходимо добавить обработку отправленных анекдотов
# Так если в таблице 2 анекдота в категории  "Анекдоты для <3"  и пользователь 2 раза запросил "Анекдоты для <3" то

# и если пользователь запросил "Анекдоты для <3" но в таблице их больше не т


# @bot.message_handler(commands=["joke"])
# def joke(message):
#     user_id = message.from_user.id
#     markup = types.InlineKeyboardMarkup(row_width=2)

#     categories = ["Анекдоты для друзей", "Анекдоты для <3",
#                   "Анекдоты для родителей", "Анекдоты 18+", "Анекдоты 60+"]

#     for category in categories:
#         callback_data = f"category_{category}"
#         button = types.InlineKeyboardButton(
#             category, callback_data=callback_data)
#         markup.add(button)

#     bot.send_message(user_id, "Выберите категорию анекдота:",
#                      reply_markup=markup)


# @bot.callback_query_handler(func=lambda call: call.data.startswith("category_"))
# def category_selected(call):
#     user_id = call.from_user.id
#     category = call.data.split("_")[1]

#     jokes = worksheet1.get_all_records()

#     jokes_in_category = [
#         joke for joke in jokes if joke["Категория анекдота"] == category]

#     if jokes_in_category:

#         joke = random.choice(jokes_in_category)
#         bot.send_message(user_id, joke["Сам анекдот"])
#     else:
#         bot.send_message(user_id, "Извините, в этой категории анекдотов нет.")

# В button2 = types.InlineKeyboardButton("Выбор категории анекдотов", callback_data="joke_by_category")
# Необходимо удалять Inline меню после выбора категории анекдота
# Необходимо в рандомном порядке без повторов отправлять анекдоты по выбранным категориям так что бы у пользователя анекдоты не повторялись, в случае окончания колл-ва анекдотов из выбранной категории, отправлять соответствующее сообщение

import telebot
import gspread
import random
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from telebot import types


CREDENTIALS_FILE = "credentials.json"
SPREADSHEET_NAME = "Anekdots"

TOKEN_BOT = "6490562332:AAGEYO0zk8PWC2jG-cx7YnrgLcxjtdR2ICM"
bot = telebot.TeleBot(TOKEN_BOT)


scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)
worksheet1 = client.open(SPREADSHEET_NAME).worksheet("Лист1")
worksheet2 = client.open(SPREADSHEET_NAME).worksheet("Лист2")
worksheet3 = client.open(SPREADSHEET_NAME).worksheet("Лист3")

user_states = {}  # Словарь для отслеживания состояний пользователей

sent_jokes = {}  # Словарь для отслеживания отправленных анекдотов

current_category = None


@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    with open("First.jpg", "rb") as photo:
        bot.send_photo(message.chat.id, photo)

    welcome_message1 = f"✌️ Добро пожаловать, {user_name} ! Ваш ID: {user_id}"
    welcome_message2 = "Бот-анекдот - это лучший источник анекдотов в России. Если ваши анекдоты обычно вызывают тишину и недоумение в компании, а не смех, то этот бот - ваше спасение. У нас есть самые смешные анекдоты, которые поднимут настроение и заставят всех смеяться!\n\nДля выбора анекдота используй /joke\n\nДля создания своего анекдота используй /create"
    bot.send_message(message.chat.id, welcome_message1)
    bot.send_message(message.chat.id, welcome_message2, parse_mode="html")


@bot.message_handler(commands=["joke"])
def joke_command(message):
    send_joke_keyboard(message)


def send_joke_keyboard(message):
    markup = types.InlineKeyboardMarkup(row_width=2)

    button1 = types.InlineKeyboardButton(
        "Поиск анекдота по номеру", callback_data="joke_by_number")
    button2 = types.InlineKeyboardButton(
        "Выбор категории анекдотов", callback_data="joke_by_category")
    back_button = types.InlineKeyboardButton(
        "Назад", callback_data="back_to_menu")

    markup.add(button1, button2, back_button)

    bot.send_message(
        message.chat.id, "Выбери как ты хочешь получить анекдот:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "back_to_menu")
def back_to_menu(call):
    # Возвращение к главному меню
    start(call.message)


@bot.callback_query_handler(func=lambda call: call.data in ["joke_by_number", "joke_by_category"])
def joke_selection(call):
    user_id = call.from_user.id
    if call.data == "joke_by_number":
        user_states[user_id] = 'waiting_for_joke_number'
        markup = types.InlineKeyboardMarkup(row_width=2)
        cancel_button = types.InlineKeyboardButton(
            "Cancel", callback_data="cancel_joke_number")
        markup.add(cancel_button)
        bot.send_message(
            user_id, "Введи номер анекдота:", reply_markup=markup)
    else:
        user_states[user_id] = 'waiting_for_joke_category'
        markup = types.InlineKeyboardMarkup(row_width=2)
        categories = ["Анекдоты для друзей", "Анекдоты для знакомств",
                      "Анекдоты для родителей", "Анекдоты 18+", "Анекдоты 60+"]
        for category in categories:
            button = types.InlineKeyboardButton(
                category, callback_data=f"joke_category_{category}")
            markup.add(button)
        cancel_button = types.InlineKeyboardButton(
            "Cancel", callback_data="cancel_joke_category")
        markup.add(cancel_button)
        bot.send_message(
            user_id, "Выбери категорию анекдота:", reply_markup=markup)
        # Remove inline keyboard after the user has made a selection
    bot.edit_message_reply_markup(
        call.message.chat.id, call.message.message_id, reply_markup=None)


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "waiting_for_joke_number")
def send_joke_by_number(message):
    user_id = message.from_user.id
    try:
        joke_number = int(message.text)+1
        jokes = worksheet1.get_all_values()
        if joke_number > len(jokes) or joke_number - 1 <= 0:
            raise ValueError(
                f"Анекдота с таким номером не существует.\n\nПопробуйте целое число больше 1 и меньше {len(jokes)}")
        joke = jokes[joke_number - 1]
        send_joke_with_category(user_id, joke[0], joke[2], joke[1])
        user_states.pop(user_id, None)
    except ValueError as e:
        bot.send_message(user_id, f"Ошибка: {str(e)}\n\nПопробуйте снова")


# Добавьте глобальную переменную для хранения данных оценок
ratings_data = {}

# В обработчике кнопки отправки анекдота, сохраните номер анекдота и категорию анекдота


def send_joke_with_category(user_id, joke_id, joke_text, category):
    markup = types.InlineKeyboardMarkup(row_width=3)
    button1 = types.InlineKeyboardButton(
        "Отлично", callback_data=f"rating_{joke_id}_1")
    button2 = types.InlineKeyboardButton(
        "Хорошо", callback_data=f"rating_{joke_id}_2")
    button3 = types.InlineKeyboardButton(
        "Плохо", callback_data=f"rating_{joke_id}_3")
    markup.add(button1, button2, button3)

    # Сохраните данные о номере анекдота и категории анекдота в глобальной переменной
    ratings_data[user_id] = {
        'joke_id': joke_id,
        'category': category
    }

    bot.send_message(
        user_id,
        f"Категория: <u>{category}</u>\n\n<i><b>{joke_text}</b></i>\n\nОцените анекдот:",
        reply_markup=markup,
        parse_mode="html"
    )

    bot.send_message(
        user_id,
        "\n\nДля выбора анекдота используй /joke\n\nДля создания своего анекдота используй /create"
    )


# Добавьте обработчик кнопок оценки


@bot.callback_query_handler(func=lambda call: call.data.startswith("rating_"))
def rate_joke(call):
    user_id = call.from_user.id
    data_parts = call.data.split("_")
    rating = data_parts[2]

    # Получите сохраненные данные о номере анекдота и категории анекдота
    user_data = ratings_data.get(user_id)
    if user_data:
        joke_id = user_data['joke_id']   # Increment the joke_id by 1
        category = user_data['category']
        joke_id = int(joke_id)+1
        jokes = worksheet1.get_all_values()
        joke = jokes[int(joke_id) - 1]

        # Отправьте данные оценки в Google Таблицу
        worksheet3.append_row([user_id, joke_id, category, joke[2], rating])

        bot.send_message(
            user_id, f"Спасибо за вашу оценку!❤️")
    else:
        bot.send_message(
            user_id, "Произошла ошибка при оценке анекдота. Пожалуйста, попробуйте снова.")
    bot.edit_message_reply_markup(
        call.message.chat.id, call.message.message_id, reply_markup=None)


@bot.callback_query_handler(func=lambda call: call.data.startswith("joke_category_"))
def send_joke_by_category(call):
    user_id = call.from_user.id
    category = call.data.split("_")[2]
    jokes = worksheet1.get_all_values()
    category_jokes = [joke for joke in jokes if joke[1] == category]

    if user_id in sent_jokes:
        category_jokes = [
            joke for joke in category_jokes if joke not in sent_jokes[user_id]]

    if not category_jokes:
        bot.send_message(
            user_id, "Извините, вы уже прочитали все анекдоты из этой категории.")
        return

    joke = random.choice(category_jokes)
    if user_id in sent_jokes:
        sent_jokes[user_id].append(joke)
    else:
        sent_jokes[user_id] = [joke]

    send_joke_with_category(user_id, joke[0], joke[2], joke[1])
    user_states.pop(user_id, None)

    bot.edit_message_reply_markup(
        call.message.chat.id, call.message.message_id, reply_markup=None)


###############
###############
###############
###############
###############
###############


@bot.message_handler(commands=["create"])
def create_keyboard(message):
    user_id = message.from_user.id
    markup = types.InlineKeyboardMarkup(row_width=2)
    categories = ["Анекдоты для друзей", "Анекдоты для знакомств",
                  "Анекдоты для родителей", "Анекдоты 18+", "Анекдоты 60+"]

    for category in categories:
        callback_data = f"create_{category}"
        button = types.InlineKeyboardButton(
            category, callback_data=callback_data)
        markup.add(button)

    cancel_button = types.InlineKeyboardButton(
        "Отмена", callback_data="cancel")
    markup.add(cancel_button)

    bot.send_message(
        message.chat.id, "Выберите категорию для вашего анекдота:", reply_markup=markup)
    # Устанавливаем состояние ожидания выбора категории
    user_states[user_id] = 'waiting_for_category'


@bot.callback_query_handler(func=lambda call: call.data.startswith("create_"))
def category_create_selected(call):
    global current_category
    user_id = call.from_user.id
    current_category = call.data.split("_")[1]
    markup = types.InlineKeyboardMarkup()
    cancel_button = types.InlineKeyboardButton(
        "Отмена", callback_data="cancel_input")
    markup.add(cancel_button)
    # Устанавливаем состояние ожидания ввода анекдота
    user_states[user_id] = 'waiting_for_joke'
    bot.send_message(
        user_id, f"Вы выбрали категорию: {current_category}.\n\nТеперь введите ваш анекдот:", reply_markup=markup)
    # Удаление кнопок из предыдущего сообщения
    bot.edit_message_reply_markup(
        call.message.chat.id, call.message.message_id, reply_markup=None)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id

    if call.data == "cancel_joke_number":
        bot.send_message(
            user_id, "Выбор номера отменен.\n\nДля выбора анекдота используй /joke\n\nДля создания своего анекдота используй /create")
        bot.answer_callback_query(call.id, "Вы отменили выбор номера.")
        user_states.pop(user_id, None)
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id, reply_markup=None)

    elif call.data == "cancel_joke_category":
        bot.send_message(
            user_id, "Выбор категории отменен.\n\nДля выбора анекдота используй /joke\n\nДля создания своего анекдота используй /create")
        bot.answer_callback_query(call.id, "Вы отменили выбор категории.")
        user_states.pop(user_id, None)
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id, reply_markup=None)

    elif call.data == "cancel":
        if user_states.get(user_id) == 'waiting_for_category':
            bot.answer_callback_query(call.id, "Вы отменили выбор категории.")
        elif user_states.get(user_id) == 'waiting_for_joke':
            bot.answer_callback_query(call.id, "Вы отменили ввод анекдота.")
        user_states.pop(user_id, None)

        bot.send_message(
            call.message.chat.id, "Выбор категории отменен.\n\nДля выбора анекдота используй /joke\n\nДля создания своего анекдота используй /create")
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id)

    elif call.data == "cancel_input":
        bot.answer_callback_query(call.id, "Вы отменили ввод анекдота.")
        user_states.pop(user_id, None)

        bot.send_message(
            call.message.chat.id, "Ввод анекдота отменен.\n\nДля выбора анекдота используй /joke\n\nДля создания своего анекдота используй /create")
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id)

    elif call.data.startswith("create_"):
        category_create_selected(call)
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id)


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == 'waiting_for_joke')
def save_joke(message):
    global current_category
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    joke_text = message.text
    row = [user_name, current_datetime, user_id, current_category, joke_text]
    worksheet2.append_row(row)
    with open("Merci.jpg", "rb") as photo:
        bot.send_photo(message.chat.id, photo)
    bot.send_message(
        user_id, "Анекдот успешно добавлен!\n\nДля выбора анекдота используй /joke\n\nДля создания своего анекдота используй /create")
    user_states.pop(user_id, None)  # Удаляем состояние пользователя


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    message_text = 'Извините, я вас не понимаю :('
    bot.reply_to(message, message_text)


if __name__ == "__main__":
    bot.polling(none_stop=True)


# import telebot
# from telebot import types
# import random
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# # Здесь вставьте путь к вашему файлу сервисного аккаунта JSON
# SERVICE_ACCOUNT_JSON = 'service.json'

# # Установите область видимости и права доступа для вашего сервисного аккаунта
# SCOPES = ['https://spreadsheets.google.com/feeds',
#           'https://www.googleapis.com/auth/drive']

# # Подключаемся к Google Sheets
# credentials = ServiceAccountCredentials.from_json_keyfile_name(
#     SERVICE_ACCOUNT_JSON, SCOPES)
# gc = gspread.authorize(credentials)

# # Открываем таблицу по её URL
# SPREADSHEET_URL = 'https://docs.google.com/spreadsheets/d/15XZffPS1tUpE6wOO0riA1Z34X1p6rIzyVm2MCtjFTk0/edit?hl=fr#gid=0'
# worksheet = gc.open_by_url(SPREADSHEET_URL).sheet1

# TOKEN_BOT = '6490562332:AAGEYO0zk8PWC2jG-cx7YnrgLcxjtdR2ICM'

# bot = telebot.TeleBot(TOKEN_BOT)

# # Словарь с категориями и анекдотами
# jokes = {
#     "Анекдоты для друзей": ["Анекдот 1 для друзей", "Анекдот 2 для друзей", "Анекдот 3 для друзей"],
#     "Анекдоты для <3": ["Анекдот 1 для <3", "Анекдот 2 для <3", "Анекдот 3 для <3"],
#     "Анекдоты для родителей": ["Анекдот 1 для родителей", "Анекдот 2 для родителей", "Анекдот 3 для родителей"],
#     "Анекдоты 18+": ["Анекдот 1 18+", "Анекдот 2 18+", "Анекдот 3 18+"],
#     "Анекдоты для 60+": ["Анекдот 1 для 60+", "Анекдот 2 для 60+", "Анекдот 3 для 60+"]
# }

# # Словарь для хранения пользовательских анекдотов
# user_jokes = {}

# # Словарь для хранения уже отправленных анекдотов
# sent_jokes = {}

# # Словарь для хранения оценок анекдотов пользователей
# joke_ratings = {}

# # Состояния пользователей (для управления добавлением анекдотов)
# user_states = {}

# # Константы для состояний
# STATE_SELECT_CATEGORY = "select_category"
# STATE_ENTER_JOKE = "enter_joke"
# STATE_RATE_JOKE = "rate_joke"


# @bot.message_handler(commands=['start'])
# def start(message):
#     # Отправляем фото
#     with open('First.jpg', 'rb') as photo:
#         bot.send_photo(message.chat.id, photo)

#     # Отправляем приветственное сообщение
#     welcome_message1 = "Добро пожаловать в Бот-Анекдот!"
#     welcome_message2 = "Бот-анекдот - это лучший источник анекдотов в России. Если ваши анекдоты обычно вызывают тишину и недоумение в компании, а не смех, то этот бот - ваше спасение. У нас есть самые смешные анекдоты, которые поднимут настроение и заставят всех смеяться!\n\nДля выбора анекдота используй /joke\n\nДля создания своего анекдота используй /create"
#     bot.send_message(message.chat.id, welcome_message1)
#     bot.send_message(message.chat.id, welcome_message2, parse_mode='html')


# @bot.message_handler(commands=['joke'])
# def send_joke(message):
#     markup = types.InlineKeyboardMarkup(row_width=2)

#     # Создаем кнопки категорий анекдотов
#     for category in jokes.keys():
#         callback_data = f"category_{category}"
#         button = types.InlineKeyboardButton(
#             text=category, callback_data=callback_data)
#         markup.add(button)

#     bot.send_message(
#         message.chat.id, "Выберите категорию анекдотов:", reply_markup=markup)


# @bot.message_handler(commands=['create'])
# def create_joke(message):
#     user_id = message.from_user.id
#     user_states[user_id] = STATE_SELECT_CATEGORY

#     markup = types.InlineKeyboardMarkup(row_width=1)
#     for category in jokes.keys():
#         button = types.InlineKeyboardButton(category, callback_data=category)
#         markup.add(button)

#     bot.send_message(
#         message.chat.id, "Выберите категорию для создания анекдота:", reply_markup=markup)


# @bot.callback_query_handler(lambda query: query.data in jokes.keys())
# def save_user_joke_category(query):
#     user_id = query.from_user.id
#     category = query.data
#     user_states[user_id] = STATE_ENTER_JOKE
#     user_states[f"{user_id}_category"] = category
#     bot.send_message(query.message.chat.id,
#                      f"Введите анекдот для категории '{category}':")


# @bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == STATE_ENTER_JOKE)
# def save_user_joke_text(message):
#     user_id = message.from_user.id
#     category = user_states.get(f"{user_id}_category")
#     user_joke = message.text

#     # Добавляем анекдот в таблицу Google Sheets
#     worksheet.append_table(
#         [str(len(worksheet.get_all_values()) + 1), category, user_joke, ''])

#     bot.send_message(
#         message.chat.id, "Анекдот успешно добавлен в базу данных!")
#     user_states.pop(user_id)
#     user_states.pop(f"{user_id}_category")


# @bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == STATE_RATE_JOKE)
# def rate_joke(message):
#     user_id = message.from_user.id
#     joke_id = user_states.get(f"{user_id}_joke_id")
#     rating = message.text

#     if rating.lower() in ['отлично', 'нормально', 'плохо']:
#         joke_ratings[joke_id] = rating.lower()
#         bot.send_message(
#             message.chat.id, "Спасибо за вашу оценку анекдоту!")
#         user_states.pop(user_id)
#         user_states.pop(f"{user_id}_joke_id")
#     else:
#         bot.send_message(
#             message.chat.id, "Пожалуйста, выберите оценку из предложенных вариантов (Отлично, Нормально, Плохо):")


# @bot.callback_query_handler(lambda query: query.data.startswith('category_'))
# def handle_category_callback(query):
#     user_id = query.from_user.id
#     category = query.data.split('_')[1]

#     # Проверяем, есть ли уже отправленные анекдоты для данной категории
#     if category in sent_jokes and user_id in sent_jokes[category]:
#         sent_jokes_for_category = sent_jokes[category][user_id]
#     else:
#         sent_jokes_for_category = []

#     # Выбираем случайный анекдот из выбранной категории, который еще не был отправлен пользователю
#     jokes_for_category = worksheet.find(category).row

#     if jokes_for_category:
#         # Находим первый анекдот в выбранной категории, который не был отправлен
#         for row in jokes_for_category[1:]:
#             if row[0] not in sent_jokes_for_category:
#                 joke = row[2]
#                 joke_id = row[0]
#                 sent_jokes_for_category.append(joke_id)
#                 sent_jokes[category][user_id] = sent_jokes_for_category
#                 bot.send_message(query.message.chat.id, joke)
#                 user_states[user_id] = STATE_RATE_JOKE
#                 user_states[f"{user_id}_joke_id"] = joke_id
#                 markup = types.ReplyKeyboardMarkup(
#                     one_time_keyboard=True, resize_keyboard=True)
#                 markup.add('Отлично', 'Нормально', 'Плохо')
#                 bot.send_message(
#                     query.message.chat.id, "Оцените анекдот:", reply_markup=markup)
#                 break
#         else:
#             bot.send_message(query.message.chat.id,
#                              "Свежие анекдоты уже скоро!")
#     else:
#         bot.send_message(query.message.chat.id, "Свежие анекдоты уже скоро!")


# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     # Замените 'Ваш собственный текст' на ваш текст
#     custom_text = 'Извините, я вас не понимаю :('

#     # Отправьте ваш собственный текст вместо message.text
#     bot.reply_to(message, custom_text)


# bot.polling(none_stop=True)


# import telebot
# from telebot import types
# import random

# TOKEN_BOT = '6490562332:AAGEYO0zk8PWC2jG-cx7YnrgLcxjtdR2ICM'

# bot = telebot.TeleBot(TOKEN_BOT)

# # Словарь с категориями и анекдотами
# jokes = {
#     "Анекдоты для друзей": ["Анекдот 1 для друзей", "Анекдот 2 для друзей", "Анекдот 3 для друзей"],
#     "Анекдоты для <3": ["Анекдот 1 для <3", "Анекдот 2 для <3", "Анекдот 3 для <3"],
#     "Анекдоты для родителей": ["Анекдот 1 для родителей", "Анекдот 2 для родителей", "Анекдот 3 для родителей"],
#     "Анекдоты 18+": ["Анекдот 1 18+", "Анекдот 2 18+", "Анекдот 3 18+"],
#     "Анекдоты для 60+": ["Анекдот 1 для 60+", "Анекдот 2 для 60+", "Анекдот 3 для 60+"]
# }

# # Словарь для хранения пользовательских анекдотов
# user_jokes = {}

# # Словарь для хранения уже отправленных анекдотов
# sent_jokes = {}

# # Состояния пользователей (для управления добавлением анекдотов)
# user_states = {}

# # Константы для состояний
# STATE_SELECT_CATEGORY = "select_category"
# STATE_ENTER_JOKE = "enter_joke"


# @bot.message_handler(commands=['start'])
# def start(message):
#     # Отправляем фото
#     with open('First.jpg', 'rb') as photo:
#         bot.send_photo(message.chat.id, photo)

#     # Отправляем приветственное сообщение
#     welcome_message1 = "Добро пожаловать в Бот-Анекдот!"
#     welcome_message2 = "Бот-анекдот - это лучший источник анекдотов в России. Если ваши анекдоты обычно вызывают тишину и недоумение в компании, а не смех, то этот бот - ваше спасение. У нас есть самые смешные анекдоты, которые поднимут настроение и заставят всех смеяться!\n\nДля выбора анекдота используй /joke\n\nДля создания своего анекдота используй /create"
#     bot.send_message(message.chat.id, welcome_message1)
#     bot.send_message(message.chat.id, welcome_message2, parse_mode='html')


# @bot.message_handler(commands=['joke'])
# def send_joke(message):
#     markup = types.InlineKeyboardMarkup(row_width=2)

#     # Создаем кнопки категорий анекдотов
#     for category in jokes.keys():
#         callback_data = f"category_{category}"
#         button = types.InlineKeyboardButton(
#             text=category, callback_data=callback_data)
#         markup.add(button)

#     bot.send_message(
#         message.chat.id, "Выберите категорию анекдотов:", reply_markup=markup)


# @bot.message_handler(commands=['create'])
# def create_joke(message):
#     user_id = message.from_user.id
#     user_states[user_id] = STATE_SELECT_CATEGORY

#     markup = types.InlineKeyboardMarkup(row_width=1)
#     for category in jokes.keys():
#         button = types.InlineKeyboardButton(category, callback_data=category)
#         markup.add(button)

#     bot.send_message(
#         message.chat.id, "Выберите категорию для создания анекдота:", reply_markup=markup)


# @bot.callback_query_handler(lambda query: query.data in jokes.keys())
# def save_user_joke_category(query):
#     user_id = query.from_user.id
#     category = query.data
#     user_states[user_id] = STATE_ENTER_JOKE
#     user_states[f"{user_id}_category"] = category
#     bot.send_message(query.message.chat.id,
#                      f"Введите анекдот для категории '{category}':")


# @bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == STATE_ENTER_JOKE)
# def save_user_joke_text(message):
#     user_id = message.from_user.id
#     category = user_states.get(f"{user_id}_category")
#     user_joke = message.text

#     if category in jokes:
#         jokes[category].append(user_joke)
#     else:
#         jokes[category] = [user_joke]

#     bot.send_message(
#         message.chat.id, "Анекдот успешно добавлен в базу данных!")
#     user_states.pop(user_id)
#     user_states.pop(f"{user_id}_category")


# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     # Замените 'Ваш собственный текст' на ваш текст
#     custom_text = 'Извините, я вас не понимаю :('

#     # Отправьте ваш собственный текст вместо message.text
#     bot.reply_to(message, custom_text)


# bot.polling(none_stop=True)

# @bot.message_handler(commands=['create'])
# def start(message):
#     message_to_user = f'Hello <b><u>{message.from_user.first_name}</u></b>'
#     bot.send_message(message.chat.id, message_to_user, parse_mode='html')


# @bot.message_handler(commands=['description'])
# def start(message):
#     message_to_user = f'Hello <b><u>{message.from_user.first_name}</u></b>'
#     bot.send_message(message.chat.id, message_to_user, parse_mode='html')
