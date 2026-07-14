"""Compute node: concurrent workers calling a component over a queue."""

import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import Any, NamedTuple

from src.runtime.clients import ClientPool
from src.runtime.progress import ProgressBar
from src.runtime.types import (
    Component,
    Record,
)
from src.runtime.utils import call_maybe_async, quiet_cleanup, stop_quietly

type ClientPoolFactory = Callable[[int, int | None], ClientPool | Awaitable[ClientPool]]


class Node(NamedTuple):
    name: str
    component: Component
    concurrency: int = 1
    client_load: int | None = None
    client_pool_factory: ClientPoolFactory | None = None


def _validate_node_shape(
    *,
    concurrency: int,
    client_load: int | None,
    client_pool_factory: ClientPoolFactory | None,
) -> None:
    if concurrency < 1:
        raise ValueError("node() requires concurrency >= 1")
    if client_load is not None and client_load < 1:
        raise ValueError("node() requires client_load >= 1")
    if client_load is not None and client_pool_factory is None:
        raise ValueError("node() requires client_pool_factory when client_load is set")


def node(
    name: str,
    component: Component,
    *,
    concurrency: int = 1,
    client_load: int | None = None,
    client_pool_factory: ClientPoolFactory | None = None,
) -> Node:
    _validate_node_shape(
        concurrency=concurrency,
        client_load=client_load,
        client_pool_factory=client_pool_factory,
    )
    return Node(
        name=name,
        component=component,
        concurrency=concurrency,
        client_load=client_load,
        client_pool_factory=client_pool_factory,
    )


async def run_node(
    node_spec: Node,
    input_queue: asyncio.Queue[Record | None],
    output_queue: asyncio.Queue[Record | None],
    n_inputs: int = 1,
    progress: ProgressBar | None = None,
) -> None:
    if n_inputs < 1:
        raise ValueError("run_node() requires n_inputs >= 1")
    component = node_spec.component
    client_pool_factory = node_spec.client_pool_factory
    work_queue: asyncio.Queue[tuple[Record, Any] | None] = asyncio.Queue()
    pool: ClientPool | None = None
    logger = logging.getLogger(f"node.{node_spec.name}")

    async def stop_workers() -> None:
        for _ in range(node_spec.concurrency):
            await work_queue.put(None)

    async def start_pool() -> None:
        nonlocal pool
        if client_pool_factory is None:
            return
        pool = await call_maybe_async(
            client_pool_factory,
            node_spec.concurrency,
            node_spec.client_load,
        )

    async def cleanup() -> None:
        await stop_quietly(component, logger, label="component")
        if pool is not None:
            for hook in pool.cleanup_hooks:
                await quiet_cleanup(logger, "client", hook())

    async def enqueue_work() -> None:
        sentinels_remaining = n_inputs
        while True:
            record = await input_queue.get()
            try:
                if record is None:
                    sentinels_remaining -= 1
                    if sentinels_remaining <= 0:
                        await stop_workers()
                        return
                    continue
                client = pool.next() if pool is not None else None
                await work_queue.put((record, client))
            finally:
                input_queue.task_done()

    async def run_worker() -> None:
        while True:
            item = await work_queue.get()
            try:
                if item is None:
                    return
                record, client = item
                record_update = await component(client, record)
                if record_update is None:
                    if progress is not None:
                        await progress.fail()
                    continue
                await output_queue.put(record | record_update)
                if progress is not None:
                    await progress.ok()
            finally:
                work_queue.task_done()

    try:
        await start_pool()
        async with asyncio.TaskGroup() as task_group:
            task_group.create_task(enqueue_work())
            for _ in range(node_spec.concurrency):
                task_group.create_task(run_worker())
    finally:
        await cleanup()
        await output_queue.put(None)
