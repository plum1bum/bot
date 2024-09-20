import telebot
from extensions import Converter, APIException

TOKEN = '7232915438:AAGAbXDPyIrIR7hoKZ-a2WlpcZfbgt9GfNM'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = (
        "Доброго времени суток!\n"
        "Я бот для конвертации валют.\n"
        "Формат команды: <валюта1> <валюта2> <количество>\n"
        "Например: USD EUR 100\n"
        "Доступные валюты: /values"
    )
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def send_values(message):
    text = "Доступные валюты: \nUSD - Доллар\nEUR - Евро\nRUB - Рубль"
    bot.reply_to(message, text)

@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException("Неверное количество параметров.")

        base, quote, amount = values
        amount = float(amount)

        total_amount = Converter.get_price(base.upper(), quote.upper(), amount)
        text = f"{amount} {base.upper()} = {total_amount} {quote.upper()}"
        bot.send_message(message.chat.id, text)

    except APIException as e:
        bot.reply_to(message, f"Ошибка: {str(e)}")
    except ValueError:
        bot.reply_to(message, "Количество должно быть числом.")
    except Exception as e:
        bot.reply_to(message, f"Неизвестная ошибка: {str(e)}")

if __name__ == '__main__':
    bot.polling(none_stop=True)
