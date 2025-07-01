import telebot
import requests

# Токен бота Telegram
BOT_TOKEN = 'вставить токен телеграм бота'
# Токен OpenWeatherMap API
OWM_API_KEY = 'вставить API ключ тут'


OWM_URL = "https://api.openweathermap.org/data/2.5/weather"
user_states = {}

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Напиши название города, чтобы узнать погоду.")

def send_weather(chat_id, city):
    try:
        params = {
            'q': city,
            'appid': OWM_API_KEY,
            'units': 'metric',
            'lang': 'ru'
        }
        res = requests.get(OWM_URL, params=params)
        data = res.json()

        if res.status_code != 200:
            bot.send_message(chat_id, f"⚠️ Город не найден: {city}")
            return

        temp = data['main']['temp']
        feels = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        desc = data['weather'][0]['description'].capitalize()

        reply = (f"🌍 Погода в {city}:\n"
                 f"{desc}\n"
                 f"🌡 Температура: {temp}°C (ощущается как {feels}°C)\n"
                 f"💧 Влажность: {humidity}%\n"
                 f"💨 Ветер: {wind} м/с")

        bot.send_message(chat_id, reply)
    except Exception as e:
        bot.send_message(chat_id, f"Произошла ошибка: {e}")

# === [РАСШИРЕННЫЙ БЛОК ДЛЯ РЕЖИМА "/погода"] ===
# Раскомментировать для включения обработки команды "/погода"
#  Закомментируйте или удалите блок "guess_city_weather", чтобы избежать конфликтов
#@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith('/погода'))
#def handle_weather(message):
#    text = message.text.lower()
#    args = text.split(maxsplit=1)
#        if len(args) == 2:
#            city = args[1].strip().strip("<>").strip()
#            send_weather(message.chat.id, city)
#        else:
#            user_states[message.chat.id] = 'awaiting_city'
#            bot.send_message(message.chat.id, "Какой город тебя интересует?")
#        return

    # если пользователь уже в режиме ожидания города
#    if user_states.get(message.chat.id) == 'awaiting_city':
#        city = message.text.strip().strip("<>").strip()
#        send_weather(message.chat.id, city)
#        user_states.pop(message.chat.id, None)
#        return
#=========================
    
    # === [БЛОК ПО УМОЛЧАНИЮ] ===
# Обрабатывает любые текстовые сообщения как ввод города
# ОТКЛЮЧИТЬ этот блок, если активируете расширенный режим через "/погода"
@bot.message_handler(func=lambda m: True)
def guess_city_weather(message):
    text = message.text.strip()

    # Игнорируем команды
    if text.startswith('/'):
        return

    # Можно добавить фильтр по длине, чтобы не реагировать на короткие слова (например, меньше 2 символов)
    if len(text) < 2:
        return
    city = text
    send_weather(message.chat.id, city)
#=================================

       
    
# Запуск бота
bot.infinity_polling()