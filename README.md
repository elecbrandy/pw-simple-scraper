# pw-simple-scraper

> A lightweight, easy-to-use web scraper built with Python and Playwright

[![PyPI](https://img.shields.io/pypi/v/pw-simple-scraper.svg)](https://pypi.org/project/pw-simple-scraper/)
[![Python](https://img.shields.io/pypi/pyversions/pw-simple-scraper.svg)](https://pypi.org/project/pw-simple-scraper/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#license)

[한국어 보러가기](./README_kr.md)

<br>

## Overview

* `pw-simple-scraper` scrapes desired elements from a web page.
* Provide a `URL + CSS` selector, and it will return the matching elements as a list of strings.
* The result is wrapped in a `ScrapeResult` object. You can access the extracted values via **`.result` (List\[str])**.

<br>
<br>

## Installation

```bash
# 1. Install Playwright
pip install playwright

# 2-1. Install Chromium (macOS / Windows)
python -m playwright install chromium

# 2-2. Install Chromium (Linux)
python -m playwright install --with-deps chromium

# 3. Install pw-simple-scraper
pip install pw-simple-scraper
```

* Since this scraper is built on top of `Playwright`, both the `Playwright` library and the `Chromium` browser are required.

<br>
<br>

## Usage

```python
from pw-simple_scraper import scrape_context, scrape_href

# Extract text
res = scrape_context("https://example.com", "h3")
print(res.result)   # ['h3-type-content1', 'h3-type-content2', ...]
print(res.count)    # n (number of scraped elements)

# Extract links
links = scrape_href("https://example.com", "a")
print(links.result) # ['https://www.iana.org/domains/example', ...]

# Apply timeout option (default: 30 seconds)
scrape_context("https://example.com", "something", timeout=10) # 10 seconds
```

#### Result is a `ScrapeResult` object

```python
@dataclass
class ScrapeResult:
    url: str
    selector: str
    result: List[str]       # Extracted values
    count: int              # Number of values
    fetched_at: datetime    # Execution timestamp (UTC)
```

<br>
<br>

## FAQ

- **Installed but browser fails to launch**
    - You must install the browser with `python -m playwright install chromium` (Be mindful of the Linux `--with-deps` option.)

- **RuntimeError: All strategies failed**
    - This may happen if the selector doesn’t exist or the page loads slowly. **Double-check your selector** and try increasing the `timeout`.

- **Scraping inside iframe**
    - Planned for future support.

- **xpath support**
    - Planned for future support.

- **robot.txt support**
    - Will be added as a configurable option in the future.

<br>
<br>
