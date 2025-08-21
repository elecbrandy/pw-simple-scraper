import re
import random
from typing import List, Optional
from playwright.async_api import Browser
from ..utils import UA_POOL, STEALTH_SCRIPT, realistic_headers, simulate_human, extract_elements

async def run(
        browser: Browser,
        url: str,
        selector: str,
        attribute: Optional[str],
        timeout: int,
    ) -> List[str]:

    # Set up the browser context with stealth features
    ctx = await browser.new_context(
        user_agent=random.choice(UA_POOL),
        locale="en-US",
        extra_http_headers=realistic_headers(),
        viewport={"width": 1440, "height": 900},
        java_script_enabled=True,
    )

    # Add the stealth script to the context
    await ctx.add_init_script(STEALTH_SCRIPT)
    page = await ctx.new_page()
    _asset_re = re.compile(r".*\.(png|jpe?g|gif|svg|css|woff2?)$", re.IGNORECASE)
    await page.route(_asset_re, lambda r: r.abort())

    # Navigate to the URL and wait for the page to load
    await page.goto(url, wait_until="domcontentloaded", timeout=timeout)
    await simulate_human(page)
    await page.wait_for_selector(selector, state="attached", timeout=timeout)

    result = await extract_elements(page, selector, attribute)
    await ctx.close()
    return result
