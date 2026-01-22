import telebot
import subprocess
import os

TOKEN = "6550195732:AAH2RaNVsdkSpjmSyiNPGjuhH6hcAYmh-S0"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Instagram link yuboring 📥"
    )

@bot.message_handler(func=lambda m: True)
def download_instagram(message):
    url = message.text.strip()
    chat_id = message.chat.id

    bot.send_message(chat_id, "⏳ Yuklanmoqda...")

    try:
        subprocess.run(
            ["yt-dlp", "-o", "video.%(ext)s", url],
            check=True
        )

        for file in os.listdir():
            if file.startswith("video."):
                bot.send_video(chat_id, open(file, "rb"))
                os.remove(file)

    except Exception as e:
        bot.send_message(chat_id, "❌ Xatolik yuz berdi")

bot.polling(none_stop=True)
