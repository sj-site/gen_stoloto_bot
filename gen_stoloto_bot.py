import telebot
import numpy as np
from randomgen import PCG64, MT19937, JSF, DSFMT

# Замените 'YOUR_TOKEN_HERE' на токен, полученный от BotFather
bot = telebot.TeleBot('7896749291:AAHJ74_oH01_C1fHA0OjISXeb718Dzir7l0')

# Глобальные переменные для хранения настроек пользователя
user_settings = {}

# Функция для генерации случайных чисел
def generate_numbers(algo, lottery_type):
    rng = np.random.Generator(globals()[algo]())
    if lottery_type == '2 из 26':
        return sorted(rng.integers(1, 27, size=2).tolist())
    elif lottery_type == '5 из 50 и 2 из 10':
        return sorted(rng.integers(1, 51, size=5).tolist()), sorted(rng.integers(1, 11, size=2).tolist())
    elif lottery_type == '4 из 20':
        return sorted(rng.integers(1, 21, size=4).tolist())

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Выбрать алгоритм', 'Выбрать тип лотереи')
    markup.row('Сгенерировать')
    bot.send_message(message.chat.id, "Добро пожаловать в лотерею! Выберите опцию:", reply_markup=markup)

# Обработчик текста
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == 'Выбрать алгоритм':
        send_algo_options(message)
    elif message.text == 'Выбрать тип лотереи':
        send_lottery_options(message)
    elif message.text == 'Сгенерировать':
        generate_and_send_numbers(message)
    elif message.text in ['WELL', 'PCG', 'Mersenne Twister', 'CSPRNG']:
        algo_map = {
            'WELL': 'JSF',
            'PCG': 'PCG64',
            'Mersenne Twister': 'MT19937',
            'CSPRNG': 'DSFMT'
        }
        if message.chat.id not in user_settings:
            user_settings[message.chat.id] = {}
        user_settings[message.chat.id]['algo'] = algo_map[message.text]
        bot.send_message(message.chat.id, f"Алгоритм выбран: {message.text}")
        send_welcome(message)  # Возвращение к основным кнопкам
    elif message.text in ['2 из 26', '5 из 50 и 2 из 10', '4 из 20']:
        if message.chat.id not in user_settings:
            user_settings[message.chat.id] = {}
        user_settings[message.chat.id]['lottery_type'] = message.text
        bot.send_message(message.chat.id, f"Тип лотереи выбран: {message.text}")
        send_welcome(message)  # Возвращение к основным кнопкам

# Функция для отправки опций алгоритмов
def send_algo_options(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('WELL', 'PCG', 'Mersenne Twister', 'CSPRNG')
    markup.row('Назад')
    bot.send_message(message.chat.id, "Выберите алгоритм:", reply_markup=markup)

# Функция для отправки опций типов лотереи
def send_lottery_options(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('2 из 26', '5 из 50 и 2 из 10', '4 из 20')
    markup.row('Назад')
    bot.send_message(message.chat.id, "Выберите тип лотереи:", reply_markup=markup)

# Функция для генерации и отправки чисел
def generate_and_send_numbers(message):
    if message.chat.id in user_settings and 'algo' in user_settings[message.chat.id] and 'lottery_type' in user_settings[message.chat.id]:
        numbers = generate_numbers(user_settings[message.chat.id]['algo'], user_settings[message.chat.id]['lottery_type'])
        bot.send_message(message.chat.id, f"Сгенерированные числа: {numbers}")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, выберите алгоритм и тип лотереи.")

# Запускаем бота
bot.polling()