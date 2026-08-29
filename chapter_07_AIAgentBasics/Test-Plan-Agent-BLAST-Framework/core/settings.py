from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import urlparse

from core.errors import AppError


@dataclass(frozen=True)
class Settings:
    jira_url: str = ""
    jira_email: str = ""
    jira_token: str = ""
    openrouter_api_key: str = ""

    def missing_for_jira(self) -> list[str]:
        values = {
            "Jira URL": self.jira_url,
            "Jira email": self.jira_email,
            "Jira API token": self.jira_token,
        }
        return [name for name, value in values.items() if not value]

    def missing_for_generation(self) -> list[str]:
        missing = self.missing_for_jira()
        if not self.openrouter_api_key:
            missing.append("OpenRouter API key")
        return missing


class SettingsStore:
    def __init__(self, path: Path):
        self.path = path

    def load(self) -> Settings:
        stored: dict = {}
        if self.path.exists():
            try:
                stored = json.loads(self.path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise AppError(
                    "SETTINGS_READ_FAILED",
                    "Local settings could not be read. Remove .tmp/settings.json and save them again.",
                    500,
                ) from exc
        return Settings(
            jira_url=os.getenv("JIRA_BASE_URL", stored.get("jira_url", "")).strip().rstrip("/"),
            jira_email=os.getenv("JIRA_EMAIL", stored.get("jira_email", "")).strip(),
            jira_token=os.getenv("JIRA_API_TOKEN", stored.get("jira_token", "")).strip(),
            openrouter_api_key=os.getenv(
                "OPENROUTER_API_KEY", stored.get("openrouter_api_key", stored.get("groq_api_key", ""))
            ).strip(),
        )

    def public_view(self) -> dict:
        settings = self.load()
        return {
            "jira_url": settings.jira_url,
            "jira_email": settings.jira_email,
            "jira_token_configured": bool(settings.jira_token),
            "openrouter_api_key_configured": bool(settings.openrouter_api_key),
            "environment_overrides": {
                "jira_url": bool(os.getenv("JIRA_BASE_URL")),
                "jira_email": bool(os.getenv("JIRA_EMAIL")),
                "jira_token": bool(os.getenv("JIRA_API_TOKEN")),
                "openrouter_api_key": bool(os.getenv("OPENROUTER_API_KEY")),
            },
        }

    def save(self, payload: dict) -> dict:
        current = self.load()
        jira_url = str(payload.get("jira_url", current.jira_url)).strip().rstrip("/")
        jira_email = str(payload.get("jira_email", current.jira_email)).strip()
        jira_token = str(payload.get("jira_token", "")).strip() or current.jira_token
        openrouter_api_key = str(payload.get("openrouter_api_key", "")).strip() or current.openrouter_api_key

        parsed = urlparse(jira_url)
        if jira_url and (parsed.scheme != "https" or not parsed.netloc):
            raise AppError("INVALID_SETTINGS", "Jira URL must be a valid https:// URL.")
        if jira_email and ("@" not in jira_email or jira_email.startswith("@") or jira_email.endswith("@")):
            raise AppError("INVALID_SETTINGS", "Enter a valid Jira account email address.")

        settings = Settings(jira_url, jira_email, jira_token, openrouter_api_key)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self.path.with_suffix(".tmp")
        try:
            temp_path.write_text(json.dumps(asdict(settings), indent=2), encoding="utf-8")
            try:
                os.chmod(temp_path, 0o600)
            except OSError:
                pass
            temp_path.replace(self.path)
        except OSError as exc:
            raise AppError("SETTINGS_WRITE_FAILED", "Local settings could not be saved.", 500) from exc
        return self.public_view()
