# Module 1 · Lesson 1 — Create a Telegram Bot

Welcome to the **Telegram → GitHub AI Agent** tutorial.

This series walks you from a blank Telegram bot to an AI agent that can
create and manage GitHub issues. Each lesson is a small, runnable step —
so you learn the tools by using them, not by reading about them alone.

**Start here for Lesson 1.** For the full roadmap and later modules, see
the [Lessons overview](../docs/README.md).

------------------------------------------------------------------------

## What you'll build in this lesson

Build your first Telegram bot with **@BotFather**, then run a simple
echo bot using long polling.

This lesson covers Module 1 steps 1–5 from the main tutorial:

- Create a Telegram Bot
- Send and receive messages
- Polling vs Webhooks
- Build a simple Echo Bot
- Understand Telegram Updates

------------------------------------------------------------------------

## Objective

By the end of this lesson you will:

1. Have a live Telegram bot created via BotFather
2. Run a local Python app that receives messages
3. Echo replies back to the user
4. Inspect the full Telegram `Update` object

------------------------------------------------------------------------

## Prerequisites

- Python 3.10+
- A Telegram account
- Basic familiarity with the terminal

------------------------------------------------------------------------

## Step 1 — Create a Telegram Bot

1. Open Telegram and search for **@BotFather**.
2. Run `/newbot`.
3. Choose a bot name (display name).
4. Choose a username ending with `bot`.
5. Save the generated bot token securely.
6. Open your bot and press **Start**.

> **Important:** Never commit your bot token to GitHub.

### Behind the scenes

When you press **Start**, Telegram stores the message until your
application retrieves it. At this stage, there is no backend connected
to the bot yet.

------------------------------------------------------------------------

## Step 2 — Project Setup

### Structure

``` text
lesson-01-telegram-bot-creation/
│
├── app.py
├── .env
├── requirements.txt
└── README.md
```

### Install dependencies

From the project root (or this lesson folder), create a virtual
environment and install packages:

``` bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Key packages:

- `python-telegram-bot`
- `python-dotenv`

### Configure the token

Create a `.env` file in this folder:

``` env
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN
```

Make sure `.env` is listed in `.gitignore` so the token is never
committed.

------------------------------------------------------------------------

## Step 3 — Run the Echo Bot

``` bash
python app.py
```

If everything is configured correctly, you'll see:

``` text
Bot is running...
```

Open your bot in Telegram, send a message, and it will echo the text
back.

------------------------------------------------------------------------

## What the Code Does

| Piece | Role |
| --- | --- |
| `load_dotenv()` / `TELEGRAM_BOT_TOKEN` | Loads the bot token from `.env` |
| `start` handler | Replies to `/start` |
| `echo` handler | Prints the update and echoes text messages |
| `CommandHandler("start", ...)` | Routes `/start` |
| `MessageHandler(filters.TEXT, ...)` | Routes plain text messages |
| `app.run_polling()` | Starts long polling |

------------------------------------------------------------------------

## How Long Polling Works

``` text
You
 │
 ▼
Telegram App
 │
 ▼
Telegram Server
 │
 ▼
Your Bot asks:
"Any new messages?"
 │
 ▼
Telegram returns the update
 │
 ▼
Your Python application
 │
 ▼
Processes the message
 │
 ▼
Replies back through Telegram
```

Your application continuously asks Telegram for new updates. This
approach is called **Long Polling** and is ideal for local development
because it doesn't require a public server.

**Webhooks** (covered later) reverse the flow: Telegram pushes updates
to a public HTTPS endpoint. Prefer polling while learning locally.

------------------------------------------------------------------------

## Learn from the Update Object

The echo handler already prints the full update:

``` python
print(update.to_dict())
```

This prints the Telegram update as JSON, including:

- Message ID
- User ID
- Username
- Chat ID
- Timestamp
- Message text
- Chat type
- Language information

Understanding this object is essential because every Telegram
interaction—text, commands, images, files, locations, and
buttons—arrives in this format.

------------------------------------------------------------------------

## Checkpoint

You're done with this lesson when:

- [ ] BotFather created your bot and you saved the token
- [ ] `.env` holds `TELEGRAM_BOT_TOKEN` and is not committed
- [ ] `python app.py` prints `Bot is running...`
- [ ] Sending a message echoes it back in Telegram
- [ ] The terminal shows the update JSON via `update.to_dict()`

------------------------------------------------------------------------

## What's Next?

In the next lesson we'll explore:

- Telegram Handlers
- Commands vs Messages
- Photos and Documents
- Inline Buttons
- Callback Queries

Later modules will replace the echo bot with a `/newissue` command that
creates GitHub issues, then evolve it into an AI-powered engineering
assistant.
