"""Browser client implementation for verifier fallback retrieval."""

import logging
from typing import Any

from camoufox.async_api import AsyncCamoufox

from src.runtime.utils import quiet_cleanup


logger = logging.getLogger(__name__)


class BrowserClient:
    """One reusable browser page, with browser recreation on crash."""

    def __init__(self) -> None:
        self._context: Any | None = None
        self._browser: Any | None = None
        self._page: Any | None = None
        self._page_options_key: tuple[tuple[str, Any], ...] = ()

    async def start(self) -> None:
        self._context = AsyncCamoufox(
            headless=True,
            block_images=True,
            block_webrtc=True,
            i_know_what_im_doing=True,
        )
        self._browser = await self._context.__aenter__()

    async def page(self, **page_options: Any) -> Any:
        if self._browser is None:
            await self.start()
        options_key = tuple(sorted(page_options.items()))
        if self._page is not None and self._page_options_key != options_key:
            await self.reset_page()
        if self._page is None:
            self._page = await self._browser.new_page(**page_options)
            self._page_options_key = options_key
        return self._page

    async def reset_page(self) -> None:
        if self._page is not None:
            await quiet_cleanup(logger, "browser_page", self._page.close())
            self._page = None
            self._page_options_key = ()

    async def reset_browser(self) -> None:
        await self.close()
        await self.start()

    async def close(self) -> None:
        await self.reset_page()
        if self._context is not None:
            await _close_browser_context(self._context, label="browser_pool")
            self._context = None
            self._browser = None


async def _close_browser_context(browser_context: Any, *, label: str) -> None:
    await quiet_cleanup(logger, label, browser_context.__aexit__(None, None, None))
