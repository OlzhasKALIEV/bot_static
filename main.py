import json
import os

import telebot
from dotenv import load_dotenv

from static_func import aggregate_data

load_dotenv()

token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    print(message)
    bot.send_message(message.chat.id, f'Привет {message.chat.first_name}')


@bot.message_handler(content_types=['text'])
def start_message(message):
    try:
        text_bot = message.text
        json_data = json.loads(text_bot)
        data = aggregate_data(json_data['dt_from'], json_data['dt_upto'], json_data['group_type'])
        bot.send_message(message.chat.id, f"{data}")
    except json.JSONDecodeError:
        bot.send_message(message.chat.id,
                         "Неверный формат сообщения. Пожалуйста, используйте следующий формат:\n\n{\n   \"dt_from\": \"YYYY-MM-DDTHH:MM:SS\",\n   \"dt_upto\": \"YYYY-MM-DDTHH:MM:SS\",\n   \"group_type\": \"month/day/hour\"\n}")


if __name__ == '__main__':
    bot.polling()
