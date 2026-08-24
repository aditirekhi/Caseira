from time import monotonic

from redis.asyncio import Redis

from config import redis_settings

_token_blacklist: Redis | None = None
_BLACKLIST_STATUS_CACHE: dict[str, tuple[bool, float]] = {}
_BLACKLIST_CACHE_TTL_SECONDS = 10.0
_REDIS_FAILURE_COOLDOWN_SECONDS = 30.0
_redis_unavailable_until = 0.0

if redis_settings.REDIS_HOST and redis_settings.REDIS_PORT > 0:
    _token_blacklist = Redis(
        host=redis_settings.REDIS_HOST,
        port=redis_settings.REDIS_PORT,
        db=0,
        socket_connect_timeout=0.1,
        socket_timeout=0.1,
        retry_on_timeout=False,
    )


async def add_token_to_blacklist(token: str):
    global _redis_unavailable_until

    if _token_blacklist is None:
        return

    _BLACKLIST_STATUS_CACHE[token] = (True, monotonic() + _BLACKLIST_CACHE_TTL_SECONDS)

    if monotonic() < _redis_unavailable_until:
        return

    try:
        await _token_blacklist.set(token, "blacklist")
    except Exception:
        _redis_unavailable_until = monotonic() + _REDIS_FAILURE_COOLDOWN_SECONDS
        return


async def is_token_blacklisted(token: str) -> bool:
    global _redis_unavailable_until

    if _token_blacklist is None:
        return False

    now = monotonic()
    cached_status = _BLACKLIST_STATUS_CACHE.get(token)
    if cached_status is not None:
        is_blacklisted, expires_at = cached_status
        if expires_at > now:
            return is_blacklisted

        _BLACKLIST_STATUS_CACHE.pop(token, None)

    if now < _redis_unavailable_until:
        return False

    try:
        blacklisted = bool(await _token_blacklist.exists(token))
        _BLACKLIST_STATUS_CACHE[token] = (
            blacklisted,
            monotonic() + _BLACKLIST_CACHE_TTL_SECONDS,
        )
        return blacklisted
    except Exception:
        _redis_unavailable_until = monotonic() + _REDIS_FAILURE_COOLDOWN_SECONDS
        return False
