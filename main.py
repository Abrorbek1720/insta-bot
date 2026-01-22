import telebot
import subprocess
import os
import shutil

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN topilmadi")

bot = telebot.TeleBot(TOKEN)
DOWNLOAD_DIR = "downloads"


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Instagram link yuboring\n"
        "📥 Rasm / Video / Reels / Carousel yuklab beraman"
    )


@bot.message_handler(func=lambda m: True)
def download_instagram(message):
    url = message.text.strip()
    chat_id = message.chat.id

    bot.send_message(chat_id, "⏳ Yuklanmoqda...")

    if os.path.exists(DOWNLOAD_DIR):
        shutil.rmtree(DOWNLOAD_DIR)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    try:
        subprocess.run(
            [
                "yt-dlp",
                "--no-warnings",
                "--no-playlist",
                "--force-overwrites",
                "-o",
                f"{DOWNLOAD_DIR}/%(id)s.%(ext)s",
                url
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        files = os.listdir(DOWNLOAD_DIR)

        if not files:
            bot.send_message(chat_id, "❌ Media topilmadi (post yopiq yoki rasmli post bo‘lishi mumkin)")
            return

        for file in sorted(files):
            path = os.path.join(DOWNLOAD_DIR, file)

            if file.lower().endswith((".mp4", ".mov", ".webm")):
                with open(path, "rb") as f:
                    bot.send_video(chat_id, f)

            elif file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                with open(path, "rb") as f:
                    bot.send_photo(chat_id, f)

            else:
                with open(path, "rb") as f:
                    bot.send_document(chat_id, f)

            os.remove(path)

        shutil.rmtree(DOWNLOAD_DIR)

    except subprocess.CalledProcessError:
        bot.send_message(
            chat_id,
            "❌ Yuklab bo‘lmadi.\n"
            "👉 Post public ekanini tekshiring"
        )
    except Exception as e:
        bot.send_message(chat_id, f"❌ Xatolik: {e}")


bot.polling(none_stop=True)
