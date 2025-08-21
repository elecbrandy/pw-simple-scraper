import random
import asyncio
from typing import List, Optional
from urllib.parse import urlparse, urlunparse
from playwright.async_api import Page

UA_POOL: List[str] = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
]

STEALTH_SCRIPT: str = """
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
Object.defineProperty(navigator, 'languages', { get: () => ['en-US','en'] });
window.chrome = { runtime: {}, loadTimes: () => {}, csi: () => {}, app: {} };
Object.defineProperty(navigator, 'permissions', { get: () => ({ query: () => Promise.resolve({state:'granted'}) })});
"""

def realistic_headers() -> dict:
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

async def simulate_human(page: Page):
    for _ in range(random.randint(2, 5)):
        await page.mouse.move(random.randint(50, 800), random.randint(50, 600))
        await asyncio.sleep(random.uniform(0.1, 0.3))
    for _ in range(random.randint(1, 3)):
        await page.mouse.wheel(0, random.randint(150, 400))
        await asyncio.sleep(random.uniform(0.5, 1.2))
    await asyncio.sleep(random.uniform(0.3, 0.8)) 

async def extract_elements(page: Page, selector: str, attribute: Optional[str]) -> List[str]:
    locator = page.locator(selector)
    elements = await locator.all()
    out: List[str] = []
    for el in elements:
        if attribute:
            value = await el.get_attribute(attribute)
        else:
            value = await el.inner_text()
        if value and value.strip():
            out.append(value.strip())
    return out
