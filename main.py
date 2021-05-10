from telebot import TeleBot
from cfg import TOKEN
from telebot import types
import crypto

bot = TeleBot(TOKEN)

commands = {
    'start': 'Start using this bot',
    'help': 'Useful information about this bot',
}


def get_crypto(crypto_dict, rub, name, currency='доллар'):
    names_dict = {'биткоин': 'BTC', 'bitcoin': 'BTC', 'эфир': 'ETH', 'эфириум': 'ETH'}
    try:
        cur_name = names_dict[name.lower()]
    except KeyError:
        cur_name = name.lower()
    value = crypto_dict[cur_name.upper() + '/USD']
    if currency.lower() == 'доллар':
        return round(value)
    elif currency.lower() == 'рубль':
        return round(value * rub)


# ОСНОВА -------------------------------------------------------------------------
state_was = True


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item_rub = types.KeyboardButton('Рубль')
    item_dol = types.KeyboardButton('Доллар')
    markup.add(item_dol, item_rub)
    send = bot.send_message(message.chat.id,
                            """Приветствую, {0.first_name}!\nЯ помогу тебе узнать <b> курс криптовалют</b>\nВ какой валюте ты хочешь узнавать курс?""".format(
                                message.from_user,
                                bot.get_me()),
                            parse_mode='HTML', reply_markup=markup)

    bot.register_next_step_handler(send, get_course)


state = None


@bot.message_handler(content_type=['text'])
def get_course(message):
    global state
    global state_was
    if message.text == 'в рублях':
        state = 'рубль'
    elif message.text == 'в долларах':
        state = 'доллар'
    if state == None:
        state = message.text
    if state_was:
        state_was = False
        text_for = 'Хорошо!\nВыбери, какую криптовалюту хочешь узнать'
    else:
        text_for = 'Жду от тебя валюту...'

    markup = types.ReplyKeyboardMarkup(row_width=2)
    item_btc = types.KeyboardButton('BTC')
    item_eth = types.KeyboardButton('ETH')
    item_neo = types.KeyboardButton('NEO')
    item_xrp = types.KeyboardButton('XRP')
    item_eos = types.KeyboardButton('EOS')
    item_omg = types.KeyboardButton('OMG')
    if state.lower() == 'доллар':
        item_stop = types.KeyboardButton('в рублях')
    else:
        item_stop = types.KeyboardButton('в долларах')
    markup.add(item_btc, item_eth, item_eos, item_neo, item_xrp, item_omg, item_stop)

    send = bot.send_message(message.from_user.id, text_for,
                            reply_markup=markup)

    bot.register_next_step_handler(send, say_value)


@bot.message_handler(content_type=['text'])
def say_value(message):
    global state
    if message.text == 'в рублях' or message.text == 'в долларах':
        get_course(message)

    else:
        print(message.text)
        rub = crypto.rub()
        dict = crypto.get_crypto_dict('https://www.rbc.ru/crypto/')
        x = get_crypto(dict, rub, message.text, state)
        print(dict, rub, message.text, state, sep=',   ')
        if state.lower() == 'доллар':
            word = '$'
        else:
            word = '₽'

        bot.send_message(message.chat.id, f'Цена валюты в данный момент - {x} {word}')

        get_course(message)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
