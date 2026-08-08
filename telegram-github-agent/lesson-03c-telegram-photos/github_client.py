"""GitHub REST helper for Module 3 · Lesson 03c (issues + image upload)."""

from __future__ import annotations

import base64
import os
from pathlib import Path

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

    def get_repo(self) -> dict:
        url = f"{API_BASE}/repos/{self.owner}/{self.repo}"
        with httpx.Client(headers=self._headers, timeout=30.0) as client:
            response = client.get(url)
            response.raise_for_status()
            return response.json()

    def ensure_label(
        self,
        name: str,
        color: str = "d73a4a",
        description: str = "",
    ) -> dict:
        url = f"{API_BASE}/repos/{self.owner}/{self.repo}/labels/{name}"
        with httpx.Client(headers=self._headers, timeout=30.0) as client:
            response = client.get(url)
            if response.status_code == 200:
                return response.json()
            if response.status_code != 404:
                response.raise_for_status()

            create_url = f"{API_BASE}/repos/{self.owner}/{self.repo}/labels"
            payload = {
                "name": name,
                "color": color,
                "description": description,
            }
            created = client.post(create_url, json=payload)
            created.raise_for_status()
            return created.json()

    def upload_file(
        self,
        repo_path: str,
        content: bytes,
        message: str,
        branch: str | None = None,
    ) -> dict:
        url = (
            f"{API_BASE}/repos/{self.owner}/{self.repo}/contents/{repo_path}"
        )
        payload: dict = {
            "message": message,
            "content": base64.b64encode(content).decode("ascii"),
        }
        if branch:
            payload["branch"] = branch

        with httpx.Client(headers=self._headers, timeout=60.0) as client:
            existing = client.get(
                url, params={"ref": branch} if branch else None
            )
            if existing.status_code == 200:
                payload["sha"] = existing.json()["sha"]
            elif existing.status_code != 404:
                existing.raise_for_status()

            response = client.put(url, json=payload)
            if response.is_error:
                raise httpx.HTTPStatusError(
                    f"{response.status_code} uploading {repo_path}. "
                    f"GitHub said: {response.text}. "
                    "PAT needs Contents: Read and write.",
                    request=response.request,
                    response=response,
                )
            return response.json()

    def create_issue(
        self,
        title: str,
        body: str = "",
        labels: list[str] | None = None,
        assignees: list[str] | None = None,
    ) -> dict:
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

    @staticmethod
    def markdown_image(alt: str, url: str) -> str:
        return f"![{alt}]({url})"
