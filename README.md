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
| 02c | Attach / include images | *Coming soon* |

### Module 3 — Build the Bot

*Coming soon.*

### Module 4 — AI Agent

*Coming soon.*

### Module 5 — Production

*Coming soon.*

------------------------------------------------------------------------

## Getting started

1. Open [Lesson 1](telegram-github-agent/lesson-01-telegram-bot-creation/README.md).
2. Create your bot with **@BotFather**.
3. Run the echo bot locally and inspect Telegram updates.
4. Continue to [Lesson 02a](telegram-github-agent/lesson-02a-github-pat-and-create-issue/README.md) for GitHub REST + PAT.
5. Then [Lesson 02b](telegram-github-agent/lesson-02b-github-labels-and-assignees/README.md) for labels and assignees.

------------------------------------------------------------------------

## Project layout

``` text
Telegram Bot/
├── README.md                          ← you are here
├── .env                               ← secrets (not committed)
├── .env.example
├── docs/
│   └── README.md                      ← full tutorial roadmap
└── telegram-github-agent/
    ├── lesson-01-telegram-bot-creation/
    ├── lesson-02a-github-pat-and-create-issue/
    └── lesson-02b-github-labels-and-assignees/
```
