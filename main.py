import telebot
import subprocess
import os
import shutil

# Railway Variables dan token olinadi
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN topilmadi. Railway Variables ni tekshiring")

bot = telebot.TeleBot(TOKEN)
DOWNLOAD_DIR = "downloads"


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Instagram link yuboring\n"
        "📥 Post / Reels / Rasm / Carousel yuklab beraman"
    )


@bot.message_handler(func=lambda m: True)
def download_instagram(message):
    url = message.text.strip()
    chat_id = message.chat.id

    bot.send_message(chat_id, "⏳ Yuklanmoqda, iltimos kuting...")

    # eski fayllarni tozalash
    if os.path.exists(DOWNLOAD_DIR):
        shutil.rmtree(DOWNLOAD_DIR)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    try:
        # Video bo‘lsa video, rasm bo‘lsa rasm yuklaydi
        subprocess.run(
            [
                "yt-dlp",
                "-o",
                f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
                url
            ],
            check=True
        )

        files = sorted(os.listdir(DOWNLOAD_DIR))

        if not files:
            bot.send_message(chat_id, "❌ Media topilmadi")
            return

        for file in files:
            path = os.path.join(DOWNLOAD_DIR, file)

            try:
                # Video formatlar
                if file.lower().endswith((".mp4", ".mov", ".webm")):
                    with open(path, "rb") as f:
                        bot.send_video(chat_id, f)

                # Rasm formatlar (ENG MUHIM QISM)
                elif file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    with open(path, "rb") as f:
                        bot.send_photo(chat_id, f)

                # Boshqa fayllar (zaxira)
                else:
                    with open(path, "rb") as f:
                        bot.send_document(chat_id, f)

            except Exception:
                bot.send_message(chat_id, f"⚠️ Yuborib bo‘lmadi: {file}")

            os.remove(path)

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
