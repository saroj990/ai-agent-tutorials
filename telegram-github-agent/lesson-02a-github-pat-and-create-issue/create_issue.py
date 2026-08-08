"""Lesson 02a — verify PAT, then create a GitHub issue via REST."""

from dotenv import load_dotenv

from github_client import GitHubClient

load_dotenv()


def main() -> None:
    client = GitHubClient()

    user = client.get_authenticated_user()
    print(f"Authenticated as: {user['login']}")

    repo = client.get_repo()
    print(f"Target repo: {repo['full_name']}")

    issue = client.create_issue(
        title="Lesson 02a: hello from the tutorial",
        body=(
            "Created by `create_issue.py` in Module 2.\n\n"
            "This confirms the GitHub Personal Access Token and REST "
            "API wiring work."
        ),
    )

    print(f"Created issue #{issue['number']}")
    print(f"URL: {issue['html_url']}")


if __name__ == "__main__":
    main()
