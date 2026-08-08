"""Lesson 02b — create a GitHub issue with labels and an assignee."""

from dotenv import load_dotenv

from github_client import GitHubClient

load_dotenv()


def main() -> None:
    client = GitHubClient()

    user = client.get_authenticated_user()
    login = user["login"]
    print(f"Authenticated as: {login}")

    repo = client.get_repo()
    print(f"Target repo: {repo['full_name']}")

    label = client.ensure_label(
        name="tutorial",
        color="0e8a16",
        description="Created by Module 2 lesson 02b",
    )
    print(f"Label ready: {label['name']}")

    issue = client.create_issue(
        title="Lesson 02b: issue with labels and assignee",
        body=(
            "Created by `create_issue_with_metadata.py`.\n\n"
            "This issue should have the `tutorial` label and an assignee."
        ),
        labels=["tutorial"],
        assignees=[login],
    )

    label_names = [item["name"] for item in issue.get("labels", [])]
    assignee_logins = [item["login"] for item in issue.get("assignees", [])]

    print(f"Created issue #{issue['number']}")
    print(f"Labels: {label_names}")
    print(f"Assignees: {assignee_logins}")
    print(f"URL: {issue['html_url']}")


if __name__ == "__main__":
    main()
