"""Lesson 03c — /bug (etc.) with optional Telegram photo → GitHub issue."""

from __future__ import annotations

import asyncio
import logging
import os
import time

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

TITLE, BODY, PHOTO = range(3)

SHORTCUTS: dict[str, tuple[str, str, str]] = {
    "bug": ("bug", "d73a4a", "Something is broken"),
    "feature": ("enhancement", "a2eeef", "New feature or request"),
    "todo": ("todo", "fbca04", "Tracked task"),
}

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN in .env")

github = GitHubClient()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "GitHub issue bot with photos:\n\n"
        "/newissue /bug /feature /todo\n"
        "After the body, you can send a photo or /skip.\n"
        "/cancel aborts."
    )


async def begin_flow(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    *,
    kind: str,
    labels: list[str] | None,
) -> int:
    context.user_data.clear()
    context.user_data["labels"] = labels or []
    context.user_data["kind"] = kind

    label_note = (
        f"Labels: {', '.join(labels)}" if labels else "No labels"
    )
    await update.message.reply_text(
        f"Starting a **{kind}** issue.\n{label_note}\n\n"
        "Send the **title**.\nOr /cancel to abort.",
        parse_mode="Markdown",
    )
    return TITLE


async def newissue_start(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    return await begin_flow(update, context, kind="newissue", labels=None)


async def bug_start(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    name, color, desc = SHORTCUTS["bug"]
    await asyncio.to_thread(github.ensure_label, name, color, desc)
    return await begin_flow(update, context, kind="bug", labels=[name])


async def feature_start(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    name, color, desc = SHORTCUTS["feature"]
    await asyncio.to_thread(github.ensure_label, name, color, desc)
    return await begin_flow(update, context, kind="feature", labels=[name])


async def todo_start(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    name, color, desc = SHORTCUTS["todo"]
    await asyncio.to_thread(github.ensure_label, name, color, desc)
    return await begin_flow(update, context, kind="todo", labels=[name])


async def receive_title(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    title = (update.message.text or "").strip()
    if not title:
        await update.message.reply_text("Title cannot be empty. Try again.")
        return TITLE

    context.user_data["title"] = title
    await update.message.reply_text(
        "Got it. Now send the **issue body**.\nOr /cancel to abort.",
        parse_mode="Markdown",
    )
    return BODY


async def receive_body(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    context.user_data["body"] = (update.message.text or "").strip()
    await update.message.reply_text(
        "Optional: send a **photo** to attach, or /skip to create without one."
    )
    return PHOTO


async def _create_issue_from_state(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    *,
    photo_bytes: bytes | None,
    photo_name: str | None,
) -> int:
    title = context.user_data.get("title", "Untitled")
    body = context.user_data.get("body", "")
    labels = context.user_data.get("labels") or None
    kind = context.user_data.get("kind", "issue")

    await update.message.reply_text("Creating issue on GitHub…")

    try:
        if photo_bytes and photo_name:
            repo = await asyncio.to_thread(github.get_repo)
            branch = repo.get("default_branch") or "main"
            repo_path = f"tutorial-assets/telegram/{int(time.time())}-{photo_name}"
            uploaded = await asyncio.to_thread(
                github.upload_file,
                repo_path,
                photo_bytes,
                f"Telegram photo for {kind}: {title}",
                branch,
            )
            image_url = uploaded["content"]["download_url"]
            body = (
                f"{body}\n\n"
                f"{github.markdown_image('Telegram photo', image_url)}\n\n"
                f"_Uploaded from Telegram to `{repo_path}`_"
            ).strip()

        issue = await asyncio.to_thread(
            github.create_issue,
            title,
            body,
            labels,
        )
    except Exception:
        logger.exception("Failed to create GitHub issue")
        await update.message.reply_text(
            "Sorry — GitHub rejected the request. "
            "For photos, PAT needs Contents: Read and write."
        )
        context.user_data.clear()
        return ConversationHandler.END

    context.user_data.clear()
    await update.message.reply_text(
        f"Created issue #{issue['number']}\n{issue['html_url']}"
    )
    return ConversationHandler.END


async def receive_photo(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    photo = update.message.photo[-1]  # largest size
    tg_file = await context.bot.get_file(photo.file_id)
    data = bytes(await tg_file.download_as_bytearray())

    return await _create_issue_from_state(
        update,
        context,
        photo_bytes=data,
        photo_name="photo.jpg",
    )


async def skip_photo(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    return await _create_issue_from_state(
        update,
        context,
        photo_bytes=None,
        photo_name=None,
    )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text("Cancelled. Nothing was created.")
    return ConversationHandler.END


def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    issue_conv = ConversationHandler(
        entry_points=[
            CommandHandler("newissue", newissue_start),
            CommandHandler("bug", bug_start),
            CommandHandler("feature", feature_start),
            CommandHandler("todo", todo_start),
        ],
        states={
            TITLE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_title)
            ],
            BODY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_body)
            ],
            PHOTO: [
                MessageHandler(filters.PHOTO, receive_photo),
                CommandHandler("skip", skip_photo),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(issue_conv)

    print("Bot is running... (Module 3 · Lesson 03c)")
    print(f"GitHub target: {github.owner}/{github.repo}")
    app.run_polling()


if __name__ == "__main__":
    main()
