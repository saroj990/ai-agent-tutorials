# Module 2 · Lesson 02c — Issue Images

In [02a](../lesson-02a-github-pat-and-create-issue/README.md) you created
issues. In [02b](../lesson-02b-github-labels-and-assignees/README.md) you
added labels and assignees.

This lesson answers: **how do images get onto a GitHub issue?**

Still **GitHub-only** — Module 3 will use this when a Telegram user sends
a screenshot with `/newissue` or `/bug`.

**Lessons:** [Root overview](../../README.md) · [Tutorial roadmap](../../docs/README.md)

| Module 2 path | Status |
| --- | --- |
| [02a — PAT + create issue](../lesson-02a-github-pat-and-create-issue/README.md) | Done |
| [02b — Labels + assignees](../lesson-02b-github-labels-and-assignees/README.md) | Done |
| **02c — Issue images** (this lesson) | You are here |

------------------------------------------------------------------------

## The key insight

GitHub’s **create issue** API does **not** accept a binary file upload.

``` text
❌ POST /issues  +  multipart image file   →  not supported

✅ 1) Host the image somewhere (this lesson: your repo via Contents API)
✅ 2) Put markdown in the issue body:  ![alt](https://...)
```

So “attach an image” really means **embed an image URL in markdown**.

------------------------------------------------------------------------

## What you'll build

1. Upload `sample-assets/demo.png` to the repo with the **Contents API**
2. Read `content.download_url` from the response
3. Create an issue whose body includes `![...](download_url)`

------------------------------------------------------------------------

## Objective

By the end of this lesson you will:

1. Know why issue create has no binary attachment field
2. Upload a file with `PUT /repos/{owner}/{repo}/contents/{path}`
3. Embed that file in an issue body with markdown
4. Know the PAT permission needed for Contents write

------------------------------------------------------------------------

## Prerequisites

- Lessons 02a and 02b complete (working root `.env`)
- Fine-grained PAT with:
  - **Issues** → Read and write
  - **Contents** → **Read and write** ← new for this lesson

If your token only has Issues access, edit it (or create a new one) and
add Contents write for the same repository.

------------------------------------------------------------------------

## How it works

``` text
Local file: sample-assets/demo.png
 │
 ▼
PUT /repos/{owner}/{repo}/contents/tutorial-assets/lesson-02c-demo.png
 │  body: { message, content: <base64>, sha? }
 │
 ▼
GitHub stores the file on the default branch
 │  response.content.download_url
 ▼
POST /repos/{owner}/{repo}/issues
 │  body markdown includes:
 │  ![Lesson 02c demo](https://raw.githubusercontent.com/...)
 ▼
Issue page renders the image
```

### Alternate (simpler) approach

If the image is already on the public web:

``` markdown
![screenshot](https://example.com/bug.png)
```

No Contents API needed — only a reachable URL. This lesson teaches the
**upload-to-repo** path because that matches a bot receiving a local
Telegram photo later.

------------------------------------------------------------------------

## Step 1 — Update token permissions

1. GitHub → **Settings** → **Developer settings** → **Fine-grained tokens**
2. Edit your tutorial token (or generate a new one)
3. Under repository permissions, set **Contents → Read and write**
4. Keep **Issues → Read and write**
5. Update root `.env` if you generated a new token value

------------------------------------------------------------------------

## Step 2 — Project setup

### Structure

``` text
lesson-02c-github-issue-images/
│
├── README.md
├── requirements.txt
├── github_client.py
├── create_issue_with_image.py
└── sample-assets/
    └── demo.png
```

### Install

``` bash
cd telegram-github-agent/lesson-02c-github-issue-images
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Same root `.env` as before:

``` env
GITHUB_TOKEN=...
GITHUB_OWNER=...
GITHUB_REPO=...
```

------------------------------------------------------------------------

## Step 3 — Run the demo

``` bash
python create_issue_with_image.py
```

Expected output (values will differ):

``` text
Authenticated as: your-username
Target repo: your-username/your-repo-name
Uploaded image: https://raw.githubusercontent.com/.../lesson-02c-demo.png?...
Created issue #17
URL: https://github.com/your-username/your-repo-name/issues/17
```

Open the issue URL — the demo image should render in the body as a
**wide teal banner** (about 480×200). You should also see a commit that
added `tutorial-assets/lesson-02c-demo.png`.

If the image is missing or broken:

- Confirm you opened the **issue** URL, not only the file in the tree
- Hard-refresh the page
- If the repo is **private**, `raw.githubusercontent.com` links sometimes
  fail to render for anonymous image fetches — stay logged into GitHub,
  or use a public sample repo for this lesson

------------------------------------------------------------------------

## What the code does

| Piece | Role |
| --- | --- |
| `upload_file(repo_path, bytes, message)` | Base64 + `PUT .../contents/{path}` |
| `upload_local_file(...)` | Reads disk file, then uploads |
| Existing file `sha` | Sent on update so re-runs do not 409/422 |
| `markdown_image(alt, url)` | Builds `![alt](url)` |
| `create_issue(...)` | Same as 02a/02b; body holds the markdown |

### Contents API payload

``` python
{
    "message": "Lesson 02c: upload demo image for issue body",
    "content": "<base64-encoded-bytes>",
    "branch": "main",   # optional; demo uses repo default_branch
    "sha": "<blob-sha>" # only when updating an existing path
}
```

------------------------------------------------------------------------

## Common errors

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `403` on upload | Token lacks Contents write | Edit PAT → Contents: Read and write |
| `404` on upload | Wrong owner/repo or path | Check `.env` and `REPO_IMAGE_PATH` |
| `409` / validation about `sha` | File exists; update needs sha | Client already fetches sha — pull latest code |
| Image not showing in issue | Private repo + URL auth quirks | Open while logged in; `download_url` from API is preferred |
| Issues disabled | Repo setting | Enable Issues in repo Settings |

------------------------------------------------------------------------

## Checkpoint

You're done with Lesson 02c (and Module 2) when:

- [ ] PAT has Contents + Issues write
- [ ] Script uploads `tutorial-assets/lesson-02c-demo.png`
- [ ] New issue body shows the embedded image
- [ ] You can explain: upload file → get URL → markdown in issue body

------------------------------------------------------------------------

## What's next?

**Module 2 complete.** Continue with
**[Lesson 03a — `/newissue` + conversation](../lesson-03a-newissue-conversation/README.md)**:

- Telegram `ConversationHandler`
- Call `create_issue` from the bot
- Reply with the GitHub issue URL
