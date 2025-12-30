import telebot
import os

TOKEN = os.getenv("TOKEN")
ADMIN_ID = 5121402243

bot = telebot.TeleBot(TOKEN)
user_data = {}

questions = [
    "ник, дисплей ник",
    "Количество килов",
    "готов ли ты вставить в ник приписку?",
    "сколько будет актива (с твоей стороны)",
    "VIP или нет? (Геймпасс)",
    "юз в тг?"
]

@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {'answers': [], 'step': 0}
    bot.send_message(message.chat.id, questions[0])

@bot.message_handler(func=lambda message: True)
def handle(message):
    chat_id = message.chat.id

    if chat_id not in user_data:
        bot.send_message(chat_id, "Напиши /start")
        return

    data = user_data[chat_id]
    step = data['step']

    data['answers'].append(message.text)
    step += 1

    if step < len(questions):
        data['step'] = step
        bot.send_message(chat_id, questions[step])
    else:
        text = (
            "📥 НОВАЯ ЗАЯВКА\n\n"
            f"ник, дисплей ник - {data['answers'][0]}\n"
            f"Количество килов - {data['answers'][1]}\n"
            f"готов ли ты вставить в ник приписку? - {data['answers'][2]}\n"
            f"сколько будет актива (с твоей стороны) - {data['answers'][3]}\n"
            f"VIP или нет? (Геймпасс) - {data['answers'][4]}\n"
            f"юз в тг? - {data['answers'][5]}"
        )

        bot.send_message(chat_id, "✅ Заявка отправлена.")
        bot.send_message(ADMIN_ID, text)
        user_data.pop(chat_id)

bot.polling(none_stop=True)
