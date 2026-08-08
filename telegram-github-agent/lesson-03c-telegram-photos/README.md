# Module 3 · Lesson 03c — Photos from Telegram

Combines [03b shortcuts](../lesson-03b-issue-shortcuts/README.md) with
[02c image upload](../lesson-02c-github-issue-images/README.md): after
title + body, optionally send a **Telegram photo**, upload it to the
repo, and embed it in the issue body.

**Lessons:** [Root overview](../../README.md) · [Tutorial roadmap](../../docs/README.md)

| Module 3 path | Status |
| --- | --- |
| [03a — `/newissue` + conversation](../lesson-03a-newissue-conversation/README.md) | Done |
| [03b — shortcuts + labels](../lesson-03b-issue-shortcuts/README.md) | Done |
| **03c — Telegram photos** (this lesson) | You are here |

------------------------------------------------------------------------

## What you'll build

``` text
/bug → title → body → photo (or /skip) → GitHub issue (+ image markdown)
```

Commands: `/newissue`, `/bug`, `/feature`, `/todo`, `/skip`, `/cancel`.

------------------------------------------------------------------------

## Objective

1. Add a third conversation state: `PHOTO`
2. Download the largest Telegram photo size
3. Upload bytes via Contents API
4. Append `![...](download_url)` to the issue body

------------------------------------------------------------------------

## Prerequisites

- 03b concepts (shortcuts + labels)
- PAT with **Issues** + **Contents** Read and write
- Root `.env` configured

------------------------------------------------------------------------

## Flow

| State | User sends | Bot does |
| --- | --- | --- |
| entry | `/bug` etc. | ensure label, ask title |
| `TITLE` | text | store title, ask body |
| `BODY` | text | store body, ask photo or `/skip` |
| `PHOTO` | photo | download → upload → create issue |
| `PHOTO` | `/skip` | create issue without image |

------------------------------------------------------------------------

## Setup & run

``` bash
cd telegram-github-agent/lesson-03c-telegram-photos
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Only **one** bot process should poll this token.

Test:

1. `/bug`
2. Title + body
3. Send a photo (or `/skip`)
4. Open the issue URL — photo should appear when Contents upload works

------------------------------------------------------------------------

## Notes

- Telegram compresses chat photos; for originals you’d handle
  `filters.Document.IMAGE` later.
- Private repos may not render `raw.githubusercontent.com` images for
  all viewers (same caveat as Lesson 02c).
- Re-running uploads use unique paths under `tutorial-assets/telegram/`.

------------------------------------------------------------------------

## Checkpoint

- [ ] Photo step appears after body
- [ ] `/skip` still creates the issue
- [ ] Photo creates a commit + embedded image on the issue
- [ ] Shortcuts still apply labels

------------------------------------------------------------------------

## What's next?

**Module 3 complete.** Next is **Module 4 — AI Agent** (Ollama, tool
calling, memory, smarter follow-ups).
