import re
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

import random
import asyncio
from typing import List, Optional
from playwright.async_api import Page

# ... (파일의 다른 부분은 그대로 둡니다) ...

async def extract_elements(page: Page, selector: str, attribute: Optional[str]) -> List[str]:
    locator = page.locator(selector)
    
    results: List[str] = []
    if attribute == "html":
        results = await locator.evaluate_all("els => els.map(el => el.outerHTML)")
    elif attribute:
        results = await locator.evaluate_all(f"(els, attr) => els.map(el => el.getAttribute(attr))", attribute)
    else:
        results = await locator.all_text_contents()

    # 결과를 정리해서 반환 (비어있거나 공백만 있는 값 제외)
    return [item.strip() for item in results if item and item.strip()]

async def wait_for_target(
    page: Page,
    selector: str,
    attribute: str | None,
    timeout: int
) -> None:
    loc = page.locator(selector)
    if attribute is None:
        # non-empty 텍스트가 나올 때까지
        await loc.filter(has_text=re.compile(r"\S")).first.wait_for(
            state="visible",
            timeout=timeout
        )
    else:
        # 요소가 DOM 에 붙기만 하면 됨
        await loc.first.wait_for(state="attached", timeout=timeout)