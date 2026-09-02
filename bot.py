import os
import asyncio

from flask import Flask, request
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = os.environ["BOT_TOKEN"]

BAD_GIF_IDS = {
    "AgADRaMAAlftoEg",
    "AgADwr0AAs2BuEg",
    "AgADPAQAAuecRVI",
}

app = Flask(__name__)

telegram_app = Application.builder().token(TOKEN).build()


async def delete_bad_gif(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    if update.message.animation:
        gif = update.message.animation

        if gif.file_unique_id in BAD_GIF_IDS:
            try:
                await update.message.delete()
                print("Запрещённая GIF удалена")
            except Exception as e:
                print("Ошибка удаления:", repr(e))


telegram_app.add_handler(
    MessageHandler(filters.ANIMATION, delete_bad_gif)
)


@app.route("/", methods=["GET"])
def home():
    return "Bot is running!", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)

        update = Update.de_json(data, telegram_app.bot)

        asyncio.run(
            telegram_app.process_update(update)
        )

        return "OK", 200

    except Exception as e:
        print("ERROR:", repr(e))
        return "ERROR", 500


if __name__ == "__main__":
    async def start():
        await telegram_app.initialize()
        await telegram_app.start()

    asyncio.run(start())

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
