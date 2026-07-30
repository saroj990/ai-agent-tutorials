from dotenv import load_dotenv
import os

from telegram import Update
from telegram.ext import (
     ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, I am running")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.to_dict())
    await update.message.reply_text(
            update.message.text
        )

app = (
    ApplicationBuilder()
    .token(BOT_TOKEN)
    .build()
)

app.add_handler(CommandHandler("start", start))
app.add_handler(
    MessageHandler(filters.TEXT, echo)
)

print("Bot is running...")

app.run_polling()