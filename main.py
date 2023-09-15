# google spreadsheets = 15XZffPS1tUpE6wOO0riA1Z34X1p6rIzyVm2MCtjFTk0
# token = 6490562332:AAGEYO0zk8PWC2jG-cx7YnrgLcxjtdR2ICM


import telebot
import gspread
import random
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from telebot import types

# Укажите путь к файлу JSON с учетными данными вашего сервисного аккаунта для доступа к Google Sheets
CREDENTIALS_FILE = 'service.json'
SPREADSHEET_NAME = 'Anekdots'

# Инициализация бота
TOKEN_BOT = '6490562332:AAGEYO0zk8PWC2jG-cx7YnrgLcxjtdR2ICM'
bot = telebot.TeleBot(TOKEN_BOT)

# Инициализация Google Sheets API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)
worksheet1 = client.open(SPREADSHEET_NAME).worksheet('Лист1')
worksheet2 = client.open(SPREADSHEET_NAME).worksheet('Лист2')


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Записываем данные пользователя во второй лист Google таблицы
    row = [user_name, current_datetime, user_id, "", ""]
    worksheet2.append_row(row)

    # Отправляем приветственное сообщение
    welcome_message = f"Добро пожаловать, {user_name}! Ваш ID: {user_id}"
    bot.send_message(message.chat.id, welcome_message)

# Добавьте обработку других команд и функциональность бота по мере необходимости


@bot.message_handler(commands=['get_joke'])
def get_joke(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    # Получаем все анекдоты из первого листа Google таблицы
    jokes = worksheet1.get_all_records()

    if jokes:
        random_joke = random.choice(jokes)
        joke_text = random_joke["Сам анекдот"]
        bot.send_message(message.chat.id, joke_text)

        # Опрос пользователя об оценке анекдота
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            "Отлично", callback_data=f"rate_good_{user_id}"))
        markup.add(types.InlineKeyboardButton(
            "Нормально", callback_data=f"rate_ok_{user_id}"))
        markup.add(types.InlineKeyboardButton(
            "Плохо", callback_data=f"rate_bad_{user_id}"))

        bot.send_message(
            message.chat.id, "Пожалуйста, оцените анекдот:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "К сожалению, анекдоты закончились.")


@bot.callback_query_handler(lambda query: query.data.startswith('rate_'))
def rate_joke(query):
    rating = query.data.split('_')[1]
    user_id = query.data.split('_')[2]

    # Записываем оценку пользователя во второй лист Google таблицы
    user_row = worksheet2.find(user_id).row
    if rating == "good":
        worksheet2.update_cell(user_row, 4, "Отлично")
    elif rating == "ok":
        worksheet2.update_cell(user_row, 4, "Нормально")
    elif rating == "bad":
        worksheet2.update_cell(user_row, 4, "Плохо")

    bot.send_message(query.message.chat.id, f"Спасибо за вашу оценку!")


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
