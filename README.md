# Telegram → GitHub AI Agent

Build a Telegram bot that grows into an AI agent capable of creating and
managing GitHub issues.

Each lesson is a small, runnable step. Follow them in order — more
lessons will be added as the series continues.

For the full module roadmap, see the
[tutorial overview](docs/README.md).

------------------------------------------------------------------------

## Lessons

### Module 1 — Telegram Bot Fundamentals

| Lesson | Title | Folder |
| --- | --- | --- |
| 1 | [Create a Telegram Bot](telegram-github-agent/lesson-01-telegram-bot-creation/README.md) | [`lesson-01-telegram-bot-creation`](telegram-github-agent/lesson-01-telegram-bot-creation/) |

### Module 2 — GitHub Integration

| Lesson | Title | Folder |
| --- | --- | --- |
| 02a | [GitHub PAT & Create an Issue](telegram-github-agent/lesson-02a-github-pat-and-create-issue/README.md) | [`lesson-02a-github-pat-and-create-issue`](telegram-github-agent/lesson-02a-github-pat-and-create-issue/) |
| 02b | [Labels & Assignees](telegram-github-agent/lesson-02b-github-labels-and-assignees/README.md) | [`lesson-02b-github-labels-and-assignees`](telegram-github-agent/lesson-02b-github-labels-and-assignees/) |
| 02c | [Issue Images](telegram-github-agent/lesson-02c-github-issue-images/README.md) | [`lesson-02c-github-issue-images`](telegram-github-agent/lesson-02c-github-issue-images/) |

### Module 3 — Build the Bot

| Lesson | Title | Folder |
| --- | --- | --- |
| 03a | [`/newissue` + Conversation](telegram-github-agent/lesson-03a-newissue-conversation/README.md) | [`lesson-03a-newissue-conversation`](telegram-github-agent/lesson-03a-newissue-conversation/) |
| 03b | [`/bug`, `/feature`, `/todo`](telegram-github-agent/lesson-03b-issue-shortcuts/README.md) | [`lesson-03b-issue-shortcuts`](telegram-github-agent/lesson-03b-issue-shortcuts/) |
| 03c | [Photos from Telegram](telegram-github-agent/lesson-03c-telegram-photos/README.md) | [`lesson-03c-telegram-photos`](telegram-github-agent/lesson-03c-telegram-photos/) |

### Module 4 — AI Agent

*Coming soon.*

### Module 5 — Production

*Coming soon.*

------------------------------------------------------------------------

## Getting started

1. Open [Lesson 1](telegram-github-agent/lesson-01-telegram-bot-creation/README.md).
2. Create your bot with **@BotFather**.
3. Run the echo bot locally and inspect Telegram updates.
4. Continue through Module 2 (GitHub REST), then Module 3 (bot commands).
5. Latest: [03b shortcuts](telegram-github-agent/lesson-03b-issue-shortcuts/README.md) and [03c photos](telegram-github-agent/lesson-03c-telegram-photos/README.md).

------------------------------------------------------------------------

## Project layout

``` text
Telegram Bot/
├── README.md
├── .env
├── .env.example
├── docs/README.md
└── telegram-github-agent/
    ├── lesson-01-telegram-bot-creation/
    ├── lesson-02a-github-pat-and-create-issue/
    ├── lesson-02b-github-labels-and-assignees/
    ├── lesson-02c-github-issue-images/
    ├── lesson-03a-newissue-conversation/
    ├── lesson-03b-issue-shortcuts/
    └── lesson-03c-telegram-photos/
```
