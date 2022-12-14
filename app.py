import extensions
from extensions import APIException, CryptoConverter
import telebot
from config import TOKEN, keys

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    start_t = 'Хаюшки!\n' \
              'Чтобы продолжить работу введите команду /help'
    bot.reply_to(message, start_t)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    help_t = 'Чтобы начать работу, введите комманду боту в следующем формате:' \
    '\n<имя валюты> \n<в какую валюту перевести> \n<кол-во переводимой валюты>' \
    '\nУвидеть список доступных валют: /values'
    bot.reply_to(message,help_t)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    values_t = 'Доступные валюты:'
    for key in keys.keys():
        values_t = '\n'.join((values_t, key, ))
    bot.reply_to(message, values_t)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Вы ввели слишком много параметров.')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount, keys)
    except APIException as e:
        bot.reply_to(message, f'{e}')
    except Exception as e:
        bot.reply_to(message, f'Что-то пошло не так(((\n{e}')
    else:
        conv_t = f'Цена {amount} {quote} в переводе на {base} составляет {total_base}'
        bot.send_message(message.chat.id, conv_t)



bot.polling(none_stop=True)