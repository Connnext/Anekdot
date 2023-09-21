# google spreadsheets = 15XZffPS1tUpE6wOO0riA1Z34X1p6rIzyVm2MCtjFTk0
# token = 6490562332:AAGEYO0zk8PWC2jG-cx7YnrgLcxjtdR2ICM
import telebot
import gspread
import random
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from telebot import types
from dotenv import load_dotenv
import os


CREDENTIALS_FILE = "credentials.json"
SPREADSHEET_NAME = "Anekdots"

load_dotenv()

# TOKEN_BOT = "6490562332:AAGEYO0zk8PWC2jG-cx7YnrgLcxjtdR2ICM"
bot = telebot.TeleBot(os.getenv('TOKEN_BOT'))


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

ratings_data = {}

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


def send_joke_with_category(user_id, joke_id, joke_text, category):
    markup = types.InlineKeyboardMarkup(row_width=3)
    button1 = types.InlineKeyboardButton(
        "Отлично", callback_data=f"rating_{joke_id}_1")
    button2 = types.InlineKeyboardButton(
        "Хорошо", callback_data=f"rating_{joke_id}_2")
    button3 = types.InlineKeyboardButton(
        "Плохо", callback_data=f"rating_{joke_id}_3")
    markup.add(button1, button2, button3)
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
