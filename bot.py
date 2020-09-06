from config import TOKEN, URL
import telebot
import requests
from telebot import types

bot = telebot.TeleBot(TOKEN)


response = requests.get(URL).json()         # json decode

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('USD')
    btn2 = types.KeyboardButton('EUR')
    btn3 = types.KeyboardButton('RUR')
    btn4 = types.KeyboardButton('BTC')
    markup.add(btn1, btn2, btn3, btn4)
    msg = bot.send_message(message.chat.id,
                    "Взнати курс ПриватБанка", reply_markup=markup)
    bot.register_next_step_handler(msg, process_coin_step)

def process_coin_step(message):
    try:
       markup = types.ReplyKeyboardRemove(selective=False)

       for coin in response:
           if (message.text == coin['ccy']):
              bot.send_message(message.chat.id, printCoin(coin['buy'], coin['sale']),
                               reply_markup=markup, parse_mode="Markdown")

    except Exception as e:
       bot.reply_to(message, 'ooops!')

def printCoin(buy, sale):

    return "💰 *Курс купівлі:* " + str(buy) + "\n💰 *Курс продажу:* " + str(sale)


bot.enable_save_next_step_handlers(delay=2)


bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)