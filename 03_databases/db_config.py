"""Shared .env configuration helpers for database demo scripts."""

from __future__ import annotations

import os
from pathlib import Path


ENV_PATH = Path(__file__).with_name(".env")


def load_env_file(path: Path = ENV_PATH) -> None:
    """Load KEY=VALUE pairs from .env into os.environ (without overriding existing env vars)."""
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value


def get_postgres_config() -> dict[str, str | int]:
    load_env_file()
    return {
        "host": os.environ.get("POSTGRES_HOST", "localhost"),
        "port": int(os.environ.get("POSTGRES_PORT", "5432")),
        "dbname": os.environ.get("POSTGRES_DB", "postgres"),
        "user": os.environ.get("POSTGRES_USER", "postgres"),
        "password": os.environ.get("POSTGRES_PASSWORD", "postgres"),
    }


def get_mysql_config() -> dict[str, str | int]:
    load_env_file()
    return {
        "host": os.environ.get("MYSQL_HOST", "localhost"),
        "port": int(os.environ.get("MYSQL_PORT", "3306")),
        "user": os.environ.get("MYSQL_USER", "root"),
        "password": os.environ.get("MYSQL_PASSWORD", "root"),
        "database": os.environ.get("MYSQL_DATABASE", "demo_db"),
    }


def get_snowflake_config() -> dict[str, str]:
    load_env_file()
    return {
        "account": os.environ.get("SNOWFLAKE_ACCOUNT", ""),
        "user": os.environ.get("SNOWFLAKE_USER", ""),
        "password": os.environ.get("SNOWFLAKE_PASSWORD", ""),
        "warehouse": os.environ.get("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
        "database": os.environ.get("SNOWFLAKE_DATABASE", ""),
        "schema": os.environ.get("SNOWFLAKE_SCHEMA", "PUBLIC"),
    }


def require_config(config: dict[str, str], required_keys: tuple[str, ...], env_prefix: str) -> None:
    """Fail fast when required config values are missing."""
    missing = [key for key in required_keys if not str(config.get(key, "")).strip()]
    if not missing:
        return

    print("\nMissing required configuration:")
    for key in missing:
        print(f"  - {env_prefix}_{key.upper()}")

    print("\nCreate or update 03_databases/.env, then run again.")
    raise SystemExit(1)
