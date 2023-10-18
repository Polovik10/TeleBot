import telebot
from config import keys, TOKEN
from extensions import ConvertionException, ExchangeRates


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Чтобы узнать цену валюты, отправьте сообщение в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты> /nУвидеть список всех доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
       text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

        
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров.')
            
        base, quote, amount = values
        amount_float = float(amount)  # noqa: F841
        total_base = ExchangeRates.convert(values)
        total_base = round((amount_float * total_base), 2)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {total_base}'
        print(text)
        bot.send_message(message.chat.id, text)

if __name__ == "__main__":
    bot.polling()