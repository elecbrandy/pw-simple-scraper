import random
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional
from playwright.async_api import async_playwright, Playwright, Browser, Page, Response

from .browser import launch_chromium
from .utils import UA_POOL, STEALTH_SCRIPT, realistic_headers

class PlaywrightScraper:
    def __init__(self, headless: bool = True, timeout: int = 30):
        self.headless = headless 
        self.timeout = timeout
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
    
    async def launch(self) -> None:
        """
        Launches the Playwright browser.
        Avoid relaunching if already connected

        Arg:
            None
        
        Return:
            None
        """
        if self.browser and self.browser.is_connected():
            return

        self.playwright = await async_playwright().start()
        self.browser = await launch_chromium(self.playwright, headless=self.headless)

    async def close(self) -> None:
        """
        Closes the browser and stops the Playwright instance.

        Arg:
            None
        Return:
            None
        """
        if self.browser:
            await self.browser.close()
            self.browser = None
        if self.playwright:
            await self.playwright.stop()
            self.playwright = None

    @asynccontextmanager
    async def get_page(self, url: str) -> AsyncGenerator[tuple[Page, Response], None]:
        """
        Provides a Playwright page context for the given URL.
        Creates a new page, navigates to the URL, and ensures cleanup.

        Arg:
            url (str): The URL to navigate to.
        Yields:
            AsyncGenerator[tuple[Page, Response], None]: An async generator yielding the Playwright page and the response.
        """
        if not self.browser or not self.browser.is_connected():
            await self.launch()

        context = await self.browser.new_context(
            user_agent=random.choice(UA_POOL),
            extra_http_headers=realistic_headers(),
            viewport={"width": 1280, "height": 720},
        )

        try:
            await context.add_init_script(STEALTH_SCRIPT)
            page = await context.new_page()
            response = await page.goto(url, wait_until="domcontentloaded", timeout=self.timeout * 1000)
            # await simulate_human(page)
            yield page, response
        finally:
            await context.close()
        
    async def __aenter__(self):
        await self.launch()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
