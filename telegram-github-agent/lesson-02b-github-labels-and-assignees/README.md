# Module 2 · Lesson 02b — Labels & Assignees

In [Lesson 02a](../lesson-02a-github-pat-and-create-issue/README.md) you
authenticated with a PAT and created a bare issue (`title` + `body`).

This lesson adds **metadata** on create:

- **Labels** — tags like `bug` or `tutorial` for triage
- **Assignees** — GitHub users responsible for the issue

Still **GitHub-only** — Telegram wiring comes in Module 3.

**Lessons:** [Root overview](../../README.md) · [Tutorial roadmap](../../docs/README.md)

| Module 2 path | Status |
| --- | --- |
| [02a — PAT + create issue](../lesson-02a-github-pat-and-create-issue/README.md) | Done |
| **02b — Labels + assignees** (this lesson) | You are here |
| [02c — Issue images](../lesson-02c-github-issue-images/README.md) | Next |

------------------------------------------------------------------------

## What you'll build

Extend the GitHub client so `POST /repos/{owner}/{repo}/issues` can
include `labels` and `assignees`. Optionally **ensure** a label exists
before using it.

------------------------------------------------------------------------

## Objective

By the end of this lesson you will:

1. Understand labels vs assignees on a GitHub issue
2. Create an issue with both in a single REST call
3. Create a missing label via the Labels API when needed
4. See common `422` failures (unknown label / invalid assignee)

------------------------------------------------------------------------

## Prerequisites

- Lesson 02a complete (working `GITHUB_TOKEN`, `GITHUB_OWNER`, `GITHUB_REPO`)
- Same root `.env` as 02a
- You can be assigned on the target repo (true for your own repos)

------------------------------------------------------------------------

## Concepts

| Field | What it is | API shape |
| --- | --- | --- |
| `labels` | List of label **names** that already exist (or you create first) | `["bug", "tutorial"]` |
| `assignees` | List of GitHub **usernames** | `["saroj990"]` |

### On-create payload

``` json
{
  "title": "Lesson 02b: issue with labels and assignee",
  "body": "...",
  "labels": ["tutorial"],
  "assignees": ["your-username"]
}
```

That is still one request: `POST /repos/{owner}/{repo}/issues`.

### Why `ensure_label`?

If you pass a label name that does not exist on the repo, GitHub often
rejects the issue create with **422 Unprocessable Entity**.

So this lesson:

1. `GET /repos/{owner}/{repo}/labels/{name}`
2. If **404**, `POST /repos/{owner}/{repo}/labels` to create it
3. Then create the issue with that label name

------------------------------------------------------------------------

## Step 1 — Permissions check

Your fine-grained PAT from 02a needs:

- **Issues** → **Read and write** (create issues, apply labels, create labels)

If label creation fails with **403**, either:

- Widen the token permission, or
- Create the `tutorial` label once in the GitHub UI (Issues → Labels),
  then re-run the script (it will find the existing label)

Assignees do not need a separate token permission, but the user must be
assignable on that repo.

------------------------------------------------------------------------

## Step 2 — Project setup

### Structure

``` text
lesson-02b-github-labels-and-assignees/
│
├── README.md
├── requirements.txt
├── github_client.py                 ← extended client
└── create_issue_with_metadata.py    ← runnable demo
```

### Install

``` bash
cd telegram-github-agent/lesson-02b-github-labels-and-assignees
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Root `.env` (same as 02a) is enough — no new secrets required:

``` env
GITHUB_TOKEN=...
GITHUB_OWNER=...
GITHUB_REPO=...
```

------------------------------------------------------------------------

## Step 3 — Run the demo

``` bash
python create_issue_with_metadata.py
```

Expected output (values will differ):

``` text
Authenticated as: your-username
Target repo: your-username/your-repo-name
Label ready: tutorial
Created issue #16
Labels: ['tutorial']
Assignees: ['your-username']
URL: https://github.com/your-username/your-repo-name/issues/16
```

Open the URL and confirm the label chip and assignee avatar are present.

------------------------------------------------------------------------

## What the code does

| Piece | Role |
| --- | --- |
| `ensure_label(name, color, description)` | GET label; create on 404 |
| `create_issue(..., labels=..., assignees=...)` | POST issue with optional metadata |
| Demo script | Uses your login as assignee; ensures `tutorial` label |

### Extended `create_issue` payload building

``` python
payload = {"title": title, "body": body}
if labels:
    payload["labels"] = labels
if assignees:
    payload["assignees"] = assignees
```

Empty lists are omitted so 02a-style bare creates still work.

------------------------------------------------------------------------

## Alternate approach (not required here)

You can also set metadata **after** create:

``` text
POST /repos/{owner}/{repo}/issues/{number}/labels
POST /repos/{owner}/{repo}/issues/{number}/assignees
```

Useful when labels/assignees are chosen later in a multi-step bot flow
(Module 3). For 02b, **on-create** keeps the lesson small.

------------------------------------------------------------------------

## Common errors

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `422` on create | Label name does not exist | Use `ensure_label` or create the label in the UI |
| `422` on assignees | User cannot be assigned | Assign yourself on your own repo; check username spelling |
| `403` creating label | Token lacks permission | Issues: Read and write, or create label manually |
| `404` on repo | Wrong owner/repo (same as 02a) | Fix `GITHUB_OWNER` / `GITHUB_REPO` |

------------------------------------------------------------------------

## Checkpoint

You're done with Lesson 02b when:

- [ ] Script prints `Label ready: tutorial`
- [ ] New issue shows the `tutorial` label on GitHub
- [ ] You appear as assignee on that issue
- [ ] You understand labels/assignees are just extra JSON fields on the same REST create call

------------------------------------------------------------------------

## What's next?

**[Lesson 02c](../lesson-02c-github-issue-images/README.md)** covers
including an **image** on an issue (upload via Contents API + markdown).

Then **Module 3** wires this client into Telegram commands like
`/newissue`.
