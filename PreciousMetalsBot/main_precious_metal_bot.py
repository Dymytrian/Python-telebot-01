import config
import telebot
import requests
from telebot import types

bot = telebot.TeleBot(config.TOKEN)
response = requests.get(config.URL).json()

@bot.message_handler(commands=['start','help'])
def send_welcome(messagee):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('Золото')
    itembtn2 = types.KeyboardButton('Срібло')
    itembtn3 = types.KeyboardButton('Платина')
    itembtn4 = types.KeyboardButton('Паладій')
    markup.add(itembtn1,itembtn2,itembtn3,itembtn4)
    msg = bot.send_message(messagee.chat.id, "Взнати ціну дорогоцінних металів? Обери кнопку нижче"
                                             "", reply_markup=markup)

    bot.register_next_step_handler(msg, process_coin_step)

@bot.message_handler()
def process_coin_step(message):

    markup = types.ReplyKeyboardRemove(selective=False)

    for metal in response:
        if message.text==metal['txt']:
            if ((metal['txt']=='Золото') or (metal['txt']=='Срібло') or (metal['txt']=='Платина') or (metal['txt']=='Паладій')):
                bot.send_message(message.chat.id, MetalPrint(metal['rate']),
                                 reply_markup=markup, parse_mode="Markdown")

def MetalPrint(rate):
    return "Ціна даного дорогоцінного металу: " + str(rate) + " Для подальшої роботи клацніть мишкою сюди => /start"


bot.enable_save_next_step_handlers(delay=2)

if __name__ == '__main__':
    bot.polling()


