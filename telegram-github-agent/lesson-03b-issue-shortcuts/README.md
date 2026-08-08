# Module 3 · Lesson 03b — `/bug`, `/feature`, `/todo`

Builds on [03a](../lesson-03a-newissue-conversation/README.md): same
title → body conversation, but shortcut commands attach **labels**
automatically (and create the label if missing).

**Lessons:** [Root overview](../../README.md) · [Tutorial roadmap](../../docs/README.md)

| Module 3 path | Status |
| --- | --- |
| [03a — `/newissue` + conversation](../lesson-03a-newissue-conversation/README.md) | Done |
| **03b — shortcuts + labels** (this lesson) | You are here |
| [03c — Telegram photos](../lesson-03c-telegram-photos/README.md) | Parallel / next |

------------------------------------------------------------------------

## What you'll build

| Command | Label applied |
| --- | --- |
| `/newissue` | *(none)* |
| `/bug` | `bug` |
| `/feature` | `enhancement` |
| `/todo` | `todo` |

Flow is still: command → title → body → GitHub issue URL.

------------------------------------------------------------------------

## Objective

1. Reuse one `ConversationHandler` with **multiple entry points**
2. Store chosen labels in `context.user_data`
3. Call `ensure_label` then `create_issue(..., labels=[...])`

------------------------------------------------------------------------

## Prerequisites

- Lesson 03a working
- Root `.env` with Telegram + GitHub vars
- Issues: Read and write on the PAT

------------------------------------------------------------------------

## Concepts

### Multiple entry points

``` python
ConversationHandler(
    entry_points=[
        CommandHandler("newissue", newissue_start),
        CommandHandler("bug", bug_start),
        CommandHandler("feature", feature_start),
        CommandHandler("todo", todo_start),
    ],
    states={ TITLE: [...], BODY: [...] },
    fallbacks=[CommandHandler("cancel", cancel)],
)
```

Each entry point sets `context.user_data["labels"]`, then asks for the
title. Title/body handlers stay shared.

------------------------------------------------------------------------

## Setup & run

``` bash
cd telegram-github-agent/lesson-03b-issue-shortcuts
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Stop any other bot using the same token first.

In Telegram try `/bug`, send title + body, confirm the issue has the
`bug` label.

------------------------------------------------------------------------

## Checkpoint

- [ ] `/bug` creates an issue labeled `bug`
- [ ] `/feature` uses `enhancement`
- [ ] `/todo` uses `todo`
- [ ] `/newissue` still works without labels
- [ ] `/cancel` aborts

------------------------------------------------------------------------

## What's next?

[Lesson 03c](../lesson-03c-telegram-photos/README.md) adds an optional
**photo** step after the body (Module 2 Contents upload + markdown).
