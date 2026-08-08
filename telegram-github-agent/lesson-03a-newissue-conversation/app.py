"""Lesson 03a — /newissue with conversation state → GitHub issue."""

from __future__ import annotations

import asyncio
import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from github_client import GitHubClient

load_dotenv()

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TITLE, BODY = range(2)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN in .env")

github = GitHubClient()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hi! I can open GitHub issues from Telegram.\n\n"
        "Try /newissue to create one.\n"
        "Use /cancel to abort a flow in progress."
    )


async def newissue_start(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    context.user_data.clear()
    await update.message.reply_text(
        "Creating a new GitHub issue.\n\n"
        "Send the **title** (one message).\n"
        "Or /cancel to abort.",
        parse_mode="Markdown",
    )
    return TITLE


async def receive_title(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    title = (update.message.text or "").strip()
    if not title:
        await update.message.reply_text("Title cannot be empty. Try again.")
        return TITLE

    context.user_data["title"] = title
    await update.message.reply_text(
        "Got it. Now send the **issue body** (description).\n"
        "Or /cancel to abort.",
        parse_mode="Markdown",
    )
    return BODY


async def receive_body(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    body = (update.message.text or "").strip()
    title = context.user_data.get("title", "Untitled")

    await update.message.reply_text("Creating issue on GitHub…")

    try:
        issue = await asyncio.to_thread(
            github.create_issue,
            title,
            body,
        )
    except Exception:
        logger.exception("Failed to create GitHub issue")
        await update.message.reply_text(
            "Sorry — GitHub rejected the request. "
            "Check GITHUB_TOKEN / OWNER / REPO in your .env."
        )
        context.user_data.clear()
        return ConversationHandler.END

    context.user_data.clear()
    await update.message.reply_text(
        f"Created issue #{issue['number']}\n{issue['html_url']}"
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text("Cancelled. Nothing was created.")
    return ConversationHandler.END


def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    newissue_conv = ConversationHandler(
        entry_points=[CommandHandler("newissue", newissue_start)],
        states={
            TITLE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_title)
            ],
            BODY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_body)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(newissue_conv)

    print("Bot is running... (Module 3 · Lesson 03a)")
    print(f"GitHub target: {github.owner}/{github.repo}")
    app.run_polling()


if __name__ == "__main__":
    main()
