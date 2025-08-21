import random
from typing import List, Optional
from playwright.async_api import Browser
from ..utils import UA_POOL, realistic_headers, extract_elements, simulate_human

async def run(
        browser: Browser,
        url: str,
        selector: str,
        attribute: Optional[str],
        timeout: int,
    ) -> List[str]:
        headers = {
            **realistic_headers(),
            "X-Forwarded-For": ".".join(str(random.randint(1, 255)) for _ in range(4)),
            "X-Real-IP": ".".join(str(random.randint(1, 255)) for _ in range(4)),
            "Via": "1.1 proxy-server",
        }
        ctx = await browser.new_context(
            user_agent=random.choice(UA_POOL),
            viewport={"width": 1440, "height": 900},
            extra_http_headers=headers,
        )

        page = await ctx.new_page()
        await page.goto(url, wait_until="load", timeout=timeout)
        await simulate_human(page)
        await page.wait_for_selector(selector, state="attached", timeout=timeout)
        
        result = await extract_elements(page, selector, attribute)
        await ctx.close()
        return result
