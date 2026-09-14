"""Best-effort Redis cache for TaskFlow read models.

Redis accelerates repeat reads but is never the source of truth: PostgreSQL
remains authoritative and every Redis failure falls back to the database.
"""

import json
import logging
from functools import lru_cache
from typing import Any

from redis import Redis
from redis.exceptions import RedisError

from core.config import settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _client() -> Redis | None:
    if not settings.redis_url:
        return None
    return Redis.from_url(
        settings.redis_url,
        decode_responses=True,
        socket_connect_timeout=0.2,
        socket_timeout=0.2,
    )


def get_json(key: str) -> Any | None:
    client = _client()
    if client is None:
        return None
    try:
        value = client.get(key)
        return json.loads(value) if value is not None else None
    except (RedisError, json.JSONDecodeError) as exc:
        logger.warning("Redis cache read failed; using database: %s", exc)
        return None


def set_json(key: str, value: Any) -> None:
    client = _client()
    if client is None:
        return
    try:
        client.setex(key, settings.redis_cache_ttl_seconds, json.dumps(value))
    except RedisError as exc:
        logger.warning("Redis cache write failed; continuing without cache: %s", exc)


def invalidate_pattern(pattern: str) -> None:
    client = _client()
    if client is None:
        return
    try:
        for key in client.scan_iter(match=pattern):
            client.delete(key)
    except RedisError as exc:
        logger.warning("Redis cache invalidation failed; TTL will recover: %s", exc)


def status() -> str:
    client = _client()
    if client is None:
        return "disabled"
    try:
        return "connected" if client.ping() else "unavailable"
    except RedisError:
        return "unavailable"
