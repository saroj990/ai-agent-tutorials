"""Lesson 02c — upload an image, then create an issue that embeds it."""

from pathlib import Path

from dotenv import load_dotenv

from github_client import GitHubClient

load_dotenv()

SAMPLE_IMAGE = Path(__file__).parent / "sample-assets" / "demo.png"
REPO_IMAGE_PATH = "tutorial-assets/lesson-02c-demo.png"


def main() -> None:
    client = GitHubClient()

    user = client.get_authenticated_user()
    print(f"Authenticated as: {user['login']}")

    repo = client.get_repo()
    print(f"Target repo: {repo['full_name']}")
    default_branch = repo.get("default_branch") or "main"

    if not SAMPLE_IMAGE.exists():
        raise FileNotFoundError(f"Missing sample image: {SAMPLE_IMAGE}")

    uploaded = client.upload_local_file(
        local_path=SAMPLE_IMAGE,
        repo_path=REPO_IMAGE_PATH,
        message="Lesson 02c: upload demo image for issue body",
        branch=default_branch,
    )
    image_url = uploaded["content"]["download_url"]
    print(f"Uploaded image: {image_url}")

    body = "\n".join(
        [
            "Created by `create_issue_with_image.py` in Module 2.",
            "",
            "GitHub issues do not take a binary attachment on create.",
            "Instead we upload a file, then embed it with markdown:",
            "",
            client.markdown_image("Lesson 02c demo", image_url),
            "",
            f"Source path in repo: `{REPO_IMAGE_PATH}`",
        ]
    )

    issue = client.create_issue(
        title="Lesson 02c: issue with embedded image",
        body=body,
    )

    print(f"Created issue #{issue['number']}")
    print(f"URL: {issue['html_url']}")


if __name__ == "__main__":
    main()
