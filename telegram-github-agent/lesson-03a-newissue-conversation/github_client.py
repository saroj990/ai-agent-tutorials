"""GitHub REST helper reused from Module 2 (create issue)."""

from __future__ import annotations

import os

import httpx

API_BASE = "https://api.github.com"
API_VERSION = "2022-11-28"


class GitHubClient:
    def __init__(
        self,
        token: str | None = None,
        owner: str | None = None,
        repo: str | None = None,
    ) -> None:
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.owner = owner or os.getenv("GITHUB_OWNER")
        self.repo = repo or os.getenv("GITHUB_REPO")

        missing = [
            name
            for name, value in (
                ("GITHUB_TOKEN", self.token),
                ("GITHUB_OWNER", self.owner),
                ("GITHUB_REPO", self.repo),
            )
            if not value
        ]
        if missing:
            raise ValueError(
                "Missing required env vars: " + ", ".join(missing)
            )

        self._headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": API_VERSION,
        }

    def create_issue(
        self,
        title: str,
        body: str = "",
        labels: list[str] | None = None,
        assignees: list[str] | None = None,
    ) -> dict:
        """POST /repos/{owner}/{repo}/issues"""
        url = f"{API_BASE}/repos/{self.owner}/{self.repo}/issues"
        payload: dict = {"title": title, "body": body}
        if labels:
            payload["labels"] = labels
        if assignees:
            payload["assignees"] = assignees

        with httpx.Client(headers=self._headers, timeout=30.0) as client:
            response = client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
