"""Thin GitHub REST API helper for Module 2 · Lesson 02c."""

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

    def get_authenticated_user(self) -> dict:
        """GET /user — verifies the token works."""
        with httpx.Client(headers=self._headers, timeout=30.0) as client:
            response = client.get(f"{API_BASE}/user")
            response.raise_for_status()
            return response.json()

    def get_repo(self) -> dict:
        """GET /repos/{owner}/{repo} — verifies repo access."""
        url = f"{API_BASE}/repos/{self.owner}/{self.repo}"
        with httpx.Client(headers=self._headers, timeout=30.0) as client:
            response = client.get(url)
            response.raise_for_status()
            return response.json()

    def upload_file(
        self,
        repo_path: str,
        content: bytes,
        message: str,
        branch: str | None = None,
    ) -> dict:
        """
        PUT /repos/{owner}/{repo}/contents/{path}

        Uploads (or updates) a file. Returns the API JSON, including
        content.download_url for use in issue markdown.
        """
        url = (
            f"{API_BASE}/repos/{self.owner}/{self.repo}/contents/{repo_path}"
        )
        payload: dict = {
            "message": message,
            "content": base64.b64encode(content).decode("ascii"),
        }
        if branch:
            payload["branch"] = branch

        with httpx.Client(headers=self._headers, timeout=30.0) as client:
            existing = client.get(url, params={"ref": branch} if branch else None)
            if existing.status_code == 200:
                payload["sha"] = existing.json()["sha"]
            elif existing.status_code != 404:
                existing.raise_for_status()

            response = client.put(url, json=payload)
            if response.is_error:
                detail = response.text
                raise httpx.HTTPStatusError(
                    f"{response.status_code} uploading {repo_path}. "
                    f"GitHub said: {detail}. "
                    "For 403, your PAT usually needs Contents: Read and write "
                    "on this repo (Issues write alone is not enough).",
                    request=response.request,
                    response=response,
                )
            return response.json()

    def upload_local_file(
        self,
        local_path: str | Path,
        repo_path: str,
        message: str | None = None,
        branch: str | None = None,
    ) -> dict:
        """Read a local file and upload it via the Contents API."""
        path = Path(local_path)
        data = path.read_bytes()
        commit_message = message or f"Upload {path.name} for tutorial issue"
        return self.upload_file(repo_path, data, commit_message, branch=branch)

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

    @staticmethod
    def markdown_image(alt: str, url: str) -> str:
        """Build a markdown image snippet for an issue body."""
        return f"![{alt}]({url})"
