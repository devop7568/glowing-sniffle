from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Settings:
    token: str
    guild_id: int | None
    database_path: str


def load_settings() -> Settings:
    token = os.getenv("DISCORD_TOKEN", "")
    guild_id_raw = os.getenv("DISCORD_GUILD_ID")
    guild_id = int(guild_id_raw) if guild_id_raw else None
    database_path = os.getenv("DATABASE_PATH", "pulseguard.db")
    return Settings(token=token, guild_id=guild_id, database_path=database_path)
