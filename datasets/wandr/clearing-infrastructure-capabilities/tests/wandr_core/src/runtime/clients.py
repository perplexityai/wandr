"""Client pool factories for eval pipelines."""

import asyncio
import math
import os
from collections.abc import Iterable, Mapping
from itertools import cycle
from typing import Any

from openai import AsyncOpenAI

from src.runtime.browser import BrowserClient
from src.runtime.fetch import FetchClient
from src.runtime.types import StopHook

OPENAI_API_KEY_ENV = "OPENAI_API_KEY"


class ClientPool:
    def __init__(
        self, clients: Iterable[Any], cleanup_hooks: Iterable[StopHook] = ()
    ) -> None:
        self._clients = tuple(clients)
        if not self._clients:
            raise ValueError("ClientPool requires at least one client")
        self._cycle = cycle(self._clients)
        self.cleanup_hooks = tuple(cleanup_hooks)

    def next(self) -> Any:
        return next(self._cycle)


def _check_pool_shape(concurrency: int, client_load: int) -> None:
    if concurrency < 1 or client_load < 1:
        raise ValueError(
            "client pool requires concurrency >= 1 and client_load >= 1; "
            f"got {concurrency=}, {client_load=}"
        )


def _client_load(concurrency: int, client_load: int | None, default: int) -> int:
    effective_client_load = default if client_load is None else client_load
    _check_pool_shape(concurrency, effective_client_load)
    return effective_client_load


def _pool_size(concurrency: int, client_load: int) -> int:
    _check_pool_shape(concurrency, client_load)
    return max(1, math.ceil(concurrency / client_load))


def _pool_loads(concurrency: int, client_load: int) -> tuple[int, ...]:
    _check_pool_shape(concurrency, client_load)
    return tuple(
        min(client_load, concurrency - offset)
        for offset in range(0, concurrency, client_load)
    )


def openai_api_key_values(env: Mapping[str, str] | None = None) -> tuple[str, ...]:
    env = os.environ if env is None else env
    return tuple(
        value
        for name, value in sorted(env.items())
        if (name == OPENAI_API_KEY_ENV or name.startswith(f"{OPENAI_API_KEY_ENV}_"))
        and value
    )


def create_fetch_pool(concurrency: int, client_load: int | None = None) -> ClientPool:
    """Pool of page-fetch clients."""
    effective_client_load = _client_load(concurrency, client_load, concurrency)
    pool_size = _pool_size(concurrency, effective_client_load)
    fetch_clients = [FetchClient.from_env() for _ in range(pool_size)]
    return ClientPool(fetch_clients, [client.close for client in fetch_clients])


def create_openai_pool(
    concurrency: int, client_load: int | None = None, *, max_retries: int = 3
) -> ClientPool:
    """Pool of AsyncOpenAI instances, rotating across OPENAI_API_KEY variables."""
    effective_client_load = _client_load(concurrency, client_load, concurrency)
    api_keys = openai_api_key_values()
    if not api_keys:
        raise RuntimeError("No OPENAI_API_KEY env var found")

    api_key_cycle = cycle(api_keys)
    openai_clients = [
        AsyncOpenAI(api_key=next(api_key_cycle), max_retries=max_retries)
        for _ in range(_pool_size(concurrency, effective_client_load))
    ]
    return ClientPool(openai_clients)


async def create_browser_pool(
    concurrency: int, client_load: int | None = None
) -> ClientPool:
    """Pool of BrowserClient instances across camoufox browser instances.

    client_load = pages per browser (default 1 for fallback isolation).
    _pool_size(concurrency, client_load) browsers are created, each serving
    client_load workers through separate pages.

    This is async because browser startup is async; run_node awaits pool
    factories when needed.
    """
    pages_per_browser = _client_load(concurrency, client_load, 1)

    browser_clients: list[BrowserClient] = []
    try:
        for _ in range(sum(_pool_loads(concurrency, pages_per_browser))):
            client = BrowserClient()
            await client.start()
            browser_clients.append(client)
    except Exception:
        await asyncio.gather(*(client.close() for client in browser_clients))
        raise

    return ClientPool(browser_clients, [client.close for client in browser_clients])
