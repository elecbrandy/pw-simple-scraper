import asyncio
import importlib
import random
from typing import List, Optional
from .model import ScrapeResult

from playwright.async_api import async_playwright, Browser
from .browser import launch_chromium

# strategies to try in order
_STRATEGY_PATHS = [
	"pw_simple_scraper.strategies.stealth",
	"pw_simple_scraper.strategies.mobile",
	"pw_simple_scraper.strategies.proxy",
]

async def _run_strategies(
		url: str,
		selector: str,
		attribute: Optional[str],
		headless: bool,
		timeout: int,
	) -> List[str]:
	last_err: Optional[Exception] = None
	browser: Optional[Browser] = None

	# Start Playwright
	async with async_playwright() as pw:
		try:
			browser = await launch_chromium(pw, headless=headless, extra_args=[
				"--disable-features=TranslateUI", "--mute-audio"
			])
			# Try each strategy in order
			for i, mod_path in enumerate(_STRATEGY_PATHS):
				strat = importlib.import_module(mod_path)
				try:
					return await strat.run(
						browser, url, selector, attribute, timeout=timeout
					)
				except Exception as e:
					last_err = e
					await asyncio.sleep((i + 1) * 2 + random.uniform(1, 3))
		finally:
			# Ensure the browser is closed
			if browser:
				await browser.close()
	raise RuntimeError(f"All strategies failed: {last_err}")

def _run_sync(
		url: str,
		selector: str,
		attribute: Optional[str],
		headless: bool,
		timeout: int,
	) -> List[str]:
	try:
		# Check if we are already in an event loop
		loop = asyncio.get_running_loop()
		import nest_asyncio; nest_asyncio.apply()
		return loop.run_until_complete(_run_strategies(url, selector, attribute, headless, timeout))
	except RuntimeError:
		# If not, create a new event loop
		return asyncio.run(_run_strategies(url, selector, attribute, headless, timeout))

def _validate_inputs(url: str, selector: str) -> None:
	if not isinstance(url, str):
		raise TypeError("URL must be a string")
	if not url:
		raise ValueError("URL must not be empty")
	if not isinstance(selector, str):
		raise TypeError("Selector must be a string")
	if not selector:
		raise ValueError("Selector must not be empty")
	
def _respect_robots(url: str, respect_robots: bool, robots_user_agent: str) -> None:
	# will be developed in the future
	return

def scrape_context(
	url: str,
	selector: str,
	respect_robots: bool = True,
	user_agent: str = "*",
	headless: bool = True,
	timeout: int = 30,
	) -> ScrapeResult:
	"""Return the text of all elements that match a CSS selector.

	Uses Playwright to open the page, tries a few safe methods,
	and collects each element’s inner text (trimmed).

	Args:
		url: Page URL.
		selector: CSS selector to match.
		respect_robots: Whether to respect robots.txt. (Not implemented yet)
		user_agent: User agent to use for robots.txt check. (Not implemented yet)
		headless: Whether to run the browser in headless mode.
		timeout: Maximum time to wait for the page to load (in seconds).

	Returns:
		ScrapeResult
			* containing the texts, URL, and other metadata.
			* elements with no text content are skipped (only non-empty strings are returned).
	"""
	_validate_inputs(url, selector)
	# _respect_robots(url, respect_robots, user_agent) # Not implemented yet
	data = _run_sync(url, selector, None, headless=headless, timeout=timeout*1000)
	return ScrapeResult(url=url, selector=selector, result=data)


def scrape_href(
	url: str,
	selector: str,
	respect_robots: bool = True,
	user_agent: str = "*",
	headless: bool = True,
	timeout: int = 30,
	) -> ScrapeResult:
	"""Return the href attributes of all elements that match a CSS selector.

	Uses Playwright to open the page, tries a few safe methods,
	and collects each element’s href attribute.

	Args:
		url: Page URL.
		selector: CSS selector to match.
		respect_robots: Whether to respect robots.txt. (Not implemented yet)
		user_agent: User agent to use for robots.txt check. (Not implemented yet)
		headless: Whether to run the browser in headless mode.
		timeout: Maximum time to wait for the page to load (in seconds).

	Returns:
		ScrapeResult
			* containing the non-empty href strings, URL, and other metadata.
			* elements without an href (or with an empty href) are skipped and not included.
	"""
	_validate_inputs(url, selector)
	# _respect_robots(url, respect_robots, user_agent) # Not implemented yet
	data = _run_sync(url, selector, "href", headless=headless, timeout=timeout*1000)
	return ScrapeResult(url=url, selector=selector, result=data)
