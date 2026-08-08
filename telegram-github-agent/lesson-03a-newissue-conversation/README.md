# Module 3 · Lesson 03a — `/newissue` + Conversation State

Module 1 taught Telegram. Module 2 taught the GitHub REST API.

This lesson **connects them**: a Telegram command walks you through
title → body, then creates a real GitHub issue and replies with the URL.

**Lessons:** [Root overview](../../README.md) · [Tutorial roadmap](../../docs/README.md)

| Module 3 path | Status |
| --- | --- |
| **03a — `/newissue` + conversation** (this lesson) | You are here |
| [03b — shortcuts + labels](../lesson-03b-issue-shortcuts/README.md) | Next |
| [03c — Telegram photos](../lesson-03c-telegram-photos/README.md) | Next |

------------------------------------------------------------------------

## What you'll build

``` text
You (Telegram)          Bot                     GitHub
     │                   │                        │
     │  /newissue        │                        │
     │──────────────────►│                        │
     │  "Send title"     │                        │
     │◄──────────────────│                        │
     │  My bug title     │                        │
     │──────────────────►│  store title           │
     │  "Send body"      │                        │
     │◄──────────────────│                        │
     │  Steps to repro… │                        │
     │──────────────────►│  POST /issues ────────►│
     │  issue URL        │◄───────────────────────│
     │◄──────────────────│                        │
```

------------------------------------------------------------------------

## Objective

By the end of this lesson you will:

1. Use Telegram `ConversationHandler` for multi-step flows
2. Store temporary answers in `context.user_data`
3. Call your Module 2 `GitHubClient.create_issue` from a bot handler
4. Create an issue from chat with `/newissue`

------------------------------------------------------------------------

## Prerequisites

- Lesson 1 bot token working (`TELEGRAM_BOT_TOKEN`)
- Module 2 `.env` vars working (`GITHUB_TOKEN`, `GITHUB_OWNER`, `GITHUB_REPO`)
- Same root `.env` as before

------------------------------------------------------------------------

## Concepts

### Conversation state

A normal handler is one-shot: message in → reply out.

`/newissue` needs **two** user messages (title, then body). Telegram’s
`ConversationHandler` tracks which step each chat is on:

| State | Meaning |
| --- | --- |
| `TITLE` | Waiting for the issue title |
| `BODY` | Waiting for the issue body |
| `END` | Flow finished or cancelled |

### `context.user_data`

Per-user dict for the current process. We store `title` here between
steps. Cleared on success, cancel, or error.

> Note: in-memory only. Restarting the bot loses in-progress flows.
> Fine for local learning; Module 5 can add persistence later.

------------------------------------------------------------------------

## Step 1 — Env check

Root `.env` should include:

``` env
TELEGRAM_BOT_TOKEN=...
GITHUB_TOKEN=...
GITHUB_OWNER=...
GITHUB_REPO=...
```

------------------------------------------------------------------------

## Step 2 — Project setup

### Structure

``` text
lesson-03a-newissue-conversation/
│
├── README.md
├── requirements.txt
├── github_client.py    ← create_issue from Module 2
└── app.py              ← Telegram bot + ConversationHandler
```

### Install

``` bash
cd telegram-github-agent/lesson-03a-newissue-conversation
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

------------------------------------------------------------------------

## Step 3 — Run the bot

``` bash
python app.py
```

Expected:

``` text
Bot is running... (Module 3 · Lesson 03a)
GitHub target: your-username/your-repo-name
```

In Telegram:

1. Open your bot → `/start`
2. Send `/newissue`
3. Send a title, e.g. `Login button broken on mobile`
4. Send a body, e.g. `Tapping Login does nothing on iOS.`
5. Bot replies with `Created issue #N` and a GitHub URL

Abort anytime with `/cancel`.

------------------------------------------------------------------------

## What the code does

| Piece | Role |
| --- | --- |
| `/start` | Short help |
| `/newissue` | Enters conversation → ask for title |
| `receive_title` | Saves title → ask for body |
| `receive_body` | Calls GitHub → reply with URL → end |
| `/cancel` | Clears state and exits |
| `asyncio.to_thread(...)` | Runs sync `httpx` create off the event loop |

### Handler graph

``` python
ConversationHandler(
    entry_points=[CommandHandler("newissue", newissue_start)],
    states={
        TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_title)],
        BODY:  [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_body)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
```

------------------------------------------------------------------------

## Common errors

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Bot never replies | Wrong/missing `TELEGRAM_BOT_TOKEN` | Check root `.env`; restart bot |
| “GitHub rejected the request” | Bad PAT / owner / repo | Re-test with Lesson 02a script |
| Another `/newissue` ignored mid-flow | Still in conversation | Finish body or send `/cancel` |
| Conflict / getUpdates error | Two bots polling same token | Stop the other `app.py` |

------------------------------------------------------------------------

## Checkpoint

You're done with Lesson 03a when:

- [ ] `python app.py` shows the GitHub target repo
- [ ] `/newissue` asks for title, then body
- [ ] A real issue appears on GitHub
- [ ] Bot replies with the issue URL
- [ ] `/cancel` aborts cleanly

------------------------------------------------------------------------

## What's next?

**[Lesson 03b](../lesson-03b-issue-shortcuts/README.md)** adds shortcut
commands with auto-labels (`/bug`, `/feature`, `/todo`).

**[Lesson 03c](../lesson-03c-telegram-photos/README.md)** accepts a
**photo** from Telegram and embeds it on the issue.
