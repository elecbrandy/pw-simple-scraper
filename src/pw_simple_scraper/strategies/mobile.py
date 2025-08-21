import asyncio
from typing import List, Optional
from playwright.async_api import Browser
from ..utils import realistic_headers, extract_elements

MOBILE_UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"

async def run(
        browser: Browser,
        url: str,
        selector: str,
        attribute: Optional[str],
        timeout: int,
    ) -> List[str]:

    # Set up the browser context for mobile emulation
    ctx = await browser.new_context(
        user_agent=MOBILE_UA,
        viewport={"width": 375, "height": 667},
        device_scale_factor=2,
        is_mobile=True,
        has_touch=True,
        extra_http_headers=realistic_headers(),
    )
    
    # Add a mobile-specific script to the context
    page = await ctx.new_page()
    await page.goto(url, wait_until="domcontentloaded", timeout=timeout)
    for _ in range(3):
        await page.evaluate("window.scrollBy(0, 200)")
        await asyncio.sleep(0.8)
    await page.wait_for_selector(selector, state="attached", timeout=timeout)

    result = await extract_elements(page, selector, attribute)
    await ctx.close()
    return result