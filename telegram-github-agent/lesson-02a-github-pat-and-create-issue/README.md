# Module 2 · Lesson 02a — GitHub PAT & Create an Issue

Welcome back. Module 1 taught you how Telegram delivers updates to your
bot. Module 2 steps away from Telegram and teaches the other half of the
stack: **GitHub’s REST API authenticated with a Personal Access Token
(PAT)**.

This lesson is **GitHub-only**. You will not touch the Telegram bot yet.
Module 3 will connect the two.

**Lessons:** [Root overview](../../README.md) · [Tutorial roadmap](../../docs/README.md)

| Module 2 path | Status |
| --- | --- |
| **02a — PAT + create issue** (this lesson) | You are here |
| [02b — Labels + assignees](../lesson-02b-github-labels-and-assignees/README.md) | Next |
| [02c — Issue images](../lesson-02c-github-issue-images/README.md) | Later |

------------------------------------------------------------------------

## What you'll build

A small Python client that:

1. Authenticates to `api.github.com` with a Bearer token
2. Verifies who you are (`GET /user`)
3. Verifies repo access (`GET /repos/{owner}/{repo}`)
4. Creates a real issue (`POST /repos/{owner}/{repo}/issues`)

------------------------------------------------------------------------

## Objective

By the end of this lesson you will:

1. Create a GitHub Personal Access Token with the right permissions
2. Store `GITHUB_TOKEN`, `GITHUB_OWNER`, and `GITHUB_REPO` in the root `.env`
3. Understand the request headers GitHub expects
4. Run a script that opens an issue and prints its URL

------------------------------------------------------------------------

## Prerequisites

- Python 3.10+
- A GitHub account
- A repository you can open issues on (public or private — your own is fine)
- Module 1 complete (venv + `python-dotenv` familiarity helps)

------------------------------------------------------------------------

## How authentication works

``` text
Your script
 │
 ▼
HTTPS POST https://api.github.com/repos/{owner}/{repo}/issues
 │  Headers:
 │    Authorization: Bearer <GITHUB_TOKEN>
 │    Accept: application/vnd.github+json
 │    X-GitHub-Api-Version: 2022-11-28
 │  Body (JSON):
 │    { "title": "...", "body": "..." }
 │
 ▼
GitHub validates the token + permissions
 │
 ▼
Issue created → JSON response with number + html_url
```

The token is a secret credential, same idea as `TELEGRAM_BOT_TOKEN`.
Never commit it. Never paste it into chat or screenshots.

------------------------------------------------------------------------

## Step 1 — Create a Personal Access Token

GitHub supports **fine-grained** and **classic** tokens. Prefer
**fine-grained** for this tutorial.

1. Open GitHub → **Settings** → **Developer settings**.
2. Choose **Personal access tokens** → **Fine-grained tokens**.
3. Click **Generate new token**.
4. Set:
   - **Token name:** e.g. `telegram-github-agent-dev`
   - **Expiration:** short (7–30 days while learning is fine)
   - **Resource owner:** your user (or org, if the repo lives there)
   - **Repository access:** **Only select repositories** → pick your target repo
5. Under **Permissions** → **Repository permissions**, set at least:
   - **Issues** → **Read and write**
   - **Metadata** → **Read-only** (required; usually pre-selected)
6. Generate the token and **copy it once**. GitHub will not show it again.

> **Important:** If the token is ever leaked or committed, revoke it
> immediately and create a new one.

### Classic token alternative

If you use a **classic** PAT instead, enable the `repo` scope (or at
least enough access to manage issues on that repository). Fine-grained
is still preferred.

------------------------------------------------------------------------

## Step 2 — Configure the root `.env`

This project keeps secrets in the **repository root** `.env` (already
gitignored). `load_dotenv()` walks upward from the lesson folder, so the
root file is found automatically.

Add (or create) these variables next to your existing Telegram token:

``` env
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN

GITHUB_TOKEN=github_pat_xxxxxxxx
GITHUB_OWNER=your-github-username
GITHUB_REPO=your-repo-name
```

Notes:

- `GITHUB_OWNER` is the user or org that owns the repo (not always your
  login if the repo is under an organization).
- `GITHUB_REPO` is only the repo name, e.g. `my-test-repo`, **not**
  `owner/my-test-repo`.

You can copy from [`.env.example`](../../.env.example) at the repo root.

------------------------------------------------------------------------

## Step 3 — Project setup

### Structure

``` text
lesson-02a-github-pat-and-create-issue/
│
├── README.md
├── requirements.txt
├── github_client.py      ← thin REST wrapper
└── create_issue.py       ← runnable demo
```

### Install dependencies

From this lesson folder (reuse the project venv if you already have one):

``` bash
# from repo root, if you already use telegram-github-agent/venv:
source ../venv/bin/activate   # adjust if your venv lives elsewhere

# or create a local venv:
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Packages used:

- `httpx` — HTTP client for the GitHub REST API
- `python-dotenv` — load root `.env`

------------------------------------------------------------------------

## Step 4 — Run the demo

``` bash
python create_issue.py
```

Expected output (values will differ):

``` text
Authenticated as: your-username
Target repo: your-username/your-repo-name
Created issue #1
URL: https://github.com/your-username/your-repo-name/issues/1
```

Open the printed URL in the browser to confirm the issue exists.

------------------------------------------------------------------------

## What the code does

| Piece | Role |
| --- | --- |
| `load_dotenv()` | Loads root `.env` (walks parent dirs) |
| `GitHubClient` | Holds token/owner/repo and shared headers |
| `get_authenticated_user()` | `GET /user` — proves the token works |
| `get_repo()` | `GET /repos/{owner}/{repo}` — proves repo access |
| `create_issue(title, body)` | `POST .../issues` — creates the issue |
| `create_issue.py` | Glue script that prints login, repo, and issue URL |

### Request headers (required pattern)

``` python
{
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
```

### Create-issue payload (this lesson)

``` python
{"title": "...", "body": "..."}
```

Labels, assignees, and images are intentionally **not** included yet —
those are Lessons 02b and 02c.

------------------------------------------------------------------------

## Common errors

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `401 Unauthorized` | Bad or revoked token | Regenerate PAT; update `.env` |
| `404 Not Found` on repo | Wrong owner/repo, or token lacks access | Check `GITHUB_OWNER` / `GITHUB_REPO`; widen token repo access |
| `403 Resource not accessible` | Missing Issues write permission | Edit fine-grained token → Issues: Read and write |
| `ValueError: Missing required env vars` | `.env` incomplete or not found | Add vars at **repo root** `.env`; run from lesson folder |
| Issues disabled on repo | Repo settings turn issues off | Enable Issues in repo Settings |

------------------------------------------------------------------------

## Checkpoint

You're done with Lesson 02a when:

- [ ] Fine-grained (or classic) PAT created with Issues write access
- [ ] Root `.env` has `GITHUB_TOKEN`, `GITHUB_OWNER`, `GITHUB_REPO`
- [ ] `python create_issue.py` authenticates and prints your login
- [ ] A new issue appears on GitHub and the script prints its URL
- [ ] You understand that every call is REST + Bearer token (no Telegram)

------------------------------------------------------------------------

## What's next?

**[Lesson 02b](../lesson-02b-github-labels-and-assignees/README.md)** extends the same client to:

- Add **labels** when creating an issue
- Set **assignees**
- Optionally create labels if they do not exist yet

**Lesson 02c** will cover including an **image** (markdown URL and/or
upload patterns).

Then **Module 3** will wire this client into Telegram commands like
`/newissue`.
