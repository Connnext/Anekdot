# google spreadsheets = 15XZffPS1tUpE6wOO0riA1Z34X1p6rIzyVm2MCtjFTk0
# token = 6490562332:AAGEYO0zk8PWC2jG-cx7YnrgLcxjtdR2ICM


import telebot

TOKEN_BOT = '6490562332:AAGEYO0zk8PWC2jG-cx7YnrgLcxjtdR2ICM'


bot = telebot.TeleBot(TOKEN_BOT)


@bot.message_handler(commands=['start'])
def start(message):
    # Открываем фото
    Welcome_Photo = open('First.jpg', 'rb')

    # Отправляем фото
    bot.send_photo(message.chat.id, Welcome_Photo)

    # Закрываем файл после использования
    Welcome_Photo.close()

    # Отправляем приветственное сообщение
    welcome_message1 = "Добро пожаловать в Бот-Анекдот!"
    welcome_message2 = "Бот-анекдот - это лучший источник анекдотов в России. Если ваши анекдоты обычно вызывают тишину и недоумение в компании, а не смех, то этот бот - ваше спасение. У нас есть самые смешные анекдоты, которые поднимут настроение и заставят всех смеяться!\n\nДля выбора анекдота используй /joke"
    bot.send_message(message.chat.id, welcome_message1)
    bot.send_message(message.chat.id, welcome_message2, parse_mode='html')


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Замените 'Ваш собственный текст' на ваш текст
    custom_text = 'Извините, я вас не понимаю :('

    # Отправьте ваш собственный текст вместо message.text
    bot.reply_to(message, custom_text)


bot.infinity_polling()

# @bot.message_handler(commands=['joke'])
# def start(message):
#     message_to_user = f'Hello <b><u>{message.from_user.first_name}</u></b>'
#     bot.send_message(message.chat.id, message_to_user, parse_mode='html')


# @bot.message_handler(commands=['create'])
# def start(message):
#     message_to_user = f'Hello <b><u>{message.from_user.first_name}</u></b>'
#     bot.send_message(message.chat.id, message_to_user, parse_mode='html')


# @bot.message_handler(commands=['description'])
# def start(message):
#     message_to_user = f'Hello <b><u>{message.from_user.first_name}</u></b>'
#     bot.send_message(message.chat.id, message_to_user, parse_mode='html')


bot.polling(none_stop=True)
