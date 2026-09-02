import os
import asyncio

from flask import Flask, request
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = os.environ["BOT_TOKEN"]

app = Flask(__name__)

telegram_app = Application.builder().token(TOKEN).build()


async def handle_gif(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    if update.message.animation:
        gif = update.message.animation

        await update.message.reply_text(
            f"file_id:\n{gif.file_id}\n\n"
            f"file_unique_id:\n{gif.file_unique_id}"
        )


telegram_app.add_handler(
    MessageHandler(filters.ANIMATION, handle_gif)
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
    import asyncio

    async def start():
        await telegram_app.initialize()
        await telegram_app.start()

    asyncio.run(start())

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
