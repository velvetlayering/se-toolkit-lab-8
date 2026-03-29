"""Load environment-backed settings for the Telegram bot."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    bot_token: str
    gateway_base_url: str
    lms_api_key: str

    @staticmethod
    def load() -> "Settings":
        missing = [
            name
            for name in ("BOT_TOKEN", "GATEWAY_BASE_URL", "LMS_API_KEY")
            if not os.getenv(name)
        ]
        if missing:
            missing_list = ", ".join(missing)
            raise RuntimeError(
                f"Missing required environment variables: {missing_list}"
            )
        return Settings(
            bot_token=os.environ["BOT_TOKEN"],
            gateway_base_url=os.environ["GATEWAY_BASE_URL"],
            lms_api_key=os.environ["LMS_API_KEY"],
        )


settings = Settings.load()
