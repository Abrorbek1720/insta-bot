import telebot
import subprocess
import os
import shutil

# BOT TOKEN Railway Variables dan olinadi
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN topilmadi. Railway Variables ni tekshiring")

bot = telebot.TeleBot(TOKEN)

DOWNLOAD_DIR = "downloads"


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Instagram link yuboring (post / reels)\n"
        "📥 Media yuklab beraman"
    )


@bot.message_handler(func=lambda m: True)
def download_instagram(message):
    url = message.text.strip()
    chat_id = message.chat.id

    bot.send_message(chat_id, "⏳ Yuklanmoqda, kuting...")

    # eski fayllarni tozalash
    if os.path.exists(DOWNLOAD_DIR):
        shutil.rmtree(DOWNLOAD_DIR)

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    try:
        # yt-dlp orqali yuklash
        subprocess.run(
            [
                "yt-dlp",
                "-f",
                "mp4/best",
                "-o",
                f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
                url
            ],
            check=True
        )

        files = os.listdir(DOWNLOAD_DIR)

        if not files:
            bot.send_message(chat_id, "❌ Media topilmadi")
            return

        for file in files:
            path = os.path.join(DOWNLOAD_DIR, file)

            try:
                if file.lower().endswith((".mp4", ".mov", ".webm")):
                    bot.send_video(chat_id, open(path, "rb"))
                elif file.lower().endswith((".jpg", ".jpeg", ".png")):
                    bot.send_photo(chat_id, open(path, "rb"))
            except Exception as e:
                bot.send_message(chat_id, f"⚠️ Yuborib bo‘lmadi: {file}")

        shutil.rmtree(DOWNLOAD_DIR)

    except subprocess.CalledProcessError:
        bot.send_message(
            chat_id,
            "❌ Yuklab bo‘lmadi.\n"
            "👉 Link ochiq (public) ekanini tekshiring"
        )
    except Exception as e:
        bot.send_message(chat_id, f"❌ Xatolik: {e}")


bot.polling(none_stop=True)
