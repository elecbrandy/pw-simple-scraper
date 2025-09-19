# pw-simple-scraper

[![PyPI](https://img.shields.io/pypi/v/pw-simple-scraper.svg)](https://pypi.org/project/pw-simple-scraper/)
[![Python](https://img.shields.io/pypi/pyversions/pw-simple-scraper.svg)](https://pypi.org/project/pw-simple-scraper/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#license)

<br>

> **‼️ Forget the hassle of creating browsers or setting headers. Just focus on scraping ‼️**

<br>

## Table of Contents
- [1. Main Features](#1-main-features)
- [2. Installation](#2-installation)
- [3. How to Use](#3-how-to-use)
- [4. Examples](#4-examples)
- [5. Playwright Method Reference](#5-playwright-method-reference)
- [6. FAQ](#faq)

<br>
<br>

## 1. Main Features
- A scraper library built on top of [Playwright](https://playwright.dev).
- Automatically manages the lifecycle of browsers and pages with `async with`.
- Returns Playwright objects, so you can use **all the powerful Playwright features** as they are.
- ⚡️ Fast ⚡️

<br>
<br>

## 2. Installation

``` bash
# 1. Install Playwright
pip install playwright

# 2-1. Install Chromium (macOS / Windows)
python -m playwright install chromium

# 2-2. Install Chromium (Linux)
python -m playwright install --with-deps chromium

# 3. Install pw-simple-scraper
pip install pw-simple-scraper
```

- Since this scraper is based on `Playwright`, you need both the `Playwright` library and the `Chromium` browser.

<br>
<br>

## 3. How to Use

> Not sure how to handle the `Page` object returned by `get_page`? -> [Playwright Method Reference](#5-playwright-method-reference)

<br>

1. `async with PlaywrightScraper() as scraper`  
   Create an instance of the scraper.
2. `async with scraper.get_page("http://www.example.com/") as page:`  
   Get a page context using the `get_page` method.
3. Now you can directly use all the Playwright features on `page`.

<br>

#### 🖥️ Code Example
``` python
import asyncio
from pw_simple_scraper import PlaywrightScraper

async def main():
    # Create scraper instance
    async with PlaywrightScraper() as scraper:
        # Get page context
        async with scraper.get_page("http://www.example.com/") as page:
            # >>>> Use `page` in this block! <<<<

```

<br>
<br>

## 4. Examples

> Not sure how to handle the `Page` object returned by `get_page`? -> [Playwright Method Reference](#5-playwright-method-reference)

### 4-1. Extract title / text / attributes

#### 🖥️ Code Example

``` python
import asyncio
from pw_simple_scraper import PlaywrightScraper

async def main():
    async with PlaywrightScraper() as scraper:
        async with scraper.get_page("https://quotes.toscrape.com/") as page:
            title = await page.title()
            first_quote = await page.locator("span.text").first.text_content()
            quotes = await page.locator("span.text").all_text_contents()
            first_author_link = await page.locator(".quote a").first.get_attribute("href")

            print("Page Title:", title)
            print("First Quote:", first_quote)
            print("Quote List (first 3):", quotes[:3])
            print("First Author Link:", first_author_link)

if __name__ == "__main__":
    asyncio.run(main())
```

#### ⬇️ Example Output

``` bash
Page Title: Quotes to Scrape
First Quote: “The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”
Quote List (first 3): ["The world as we have created it is a process of our thinking...", "It is our choices, Harry, that show what we truly are...", "There are only two ways to live your life..."]
First Author Link: /author/Albert-Einstein
```

### 4-2. Images & links — collect absolute paths

#### 🖥️ Code Example

```python
import asyncio
from urllib.parse import urljoin
from pw_simple_scraper import PlaywrightScraper

async def main():
    async with PlaywrightScraper() as scraper:
        async with scraper.get_page("https://books.toscrape.com/") as page:
            img_urls = await page.locator("article.product_pod img").evaluate_all(
                "els => els.map(el => el.getAttribute('src'))"
            )
            abs_imgs = [urljoin(page.url, u) for u in img_urls if u]

            book_urls = await page.locator("article.product_pod h3 a").evaluate_all(
                "els => els.map(el => el.getAttribute('href'))"
            )
            abs_books = [urljoin(page.url, u) for u in book_urls if u]

            print("Image URLs (5):", abs_imgs[:5])
            print("Book Links (5):", abs_books[:5])

if __name__ == "__main__":
    asyncio.run(main())
```

#### ⬇️ Example Output

``` bash
Image URLs (5): [
  'https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg',
  'https://books.toscrape.com/media/cache/26/0c/260c6ae16bce31c8f8c95daddd9f4a1c.jpg',
  'https://books.toscrape.com/media/cache/3e/ef/3eef99c9d9adef34639f510662022830.jpg',
  'https://books.toscrape.com/media/cache/32/51/3251cf3a3412f53f339e42cac2134093.jpg',
  'https://books.toscrape.com/media/cache/be/a5/bea5697f2534a2f86a3ef27b5a8c12a6.jpg'
]
Book Links (5): [
  'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html',
  'https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html',
  'https://books.toscrape.com/catalogue/soumission_998/index.html',
  'https://books.toscrape.com/catalogue/sharp-objects_997/index.html',
  'https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html'
]
```

### 4-3. Evaluate JSON — convert DOM to JSON

#### 🖥️ Code Example

```python
import asyncio
from pw_simple_scraper import PlaywrightScraper

async def main():
    async with PlaywrightScraper() as scraper:
        async with scraper.get_page("https://books.toscrape.com/") as page:
            cards = page.locator("article.product_pod")
            items = await cards.evaluate_all("""
                els => els.map(el => ({
                    title: el.querySelector("h3 a")?.getAttribute("title"),
                    price: el.querySelector(".price_color")?.innerText.trim(),
                    inStock: !!el.querySelector(".instock.availability"),
                }))
            """)
            print(items[:5])

if __name__ == "__main__":
    asyncio.run(main())
```

#### ⬇️ Example Output

``` bash
[
  {"title": "A Light in the Attic", "price": "£51.77", "inStock": true},
  {"title": "Tipping the Velvet", "price": "£53.74", "inStock": true},
  {"title": "Soumission", "price": "£50.10", "inStock": true},
  {"title": "Sharp Objects", "price": "£47.82", "inStock": true},
  {"title": "Sapiens: A Brief History of Humankind", "price": "£54.23", "inStock": true}
]
```
<br>
<br>

## 5. Playwright Method Reference

- If you’re not sure how to handle the `Page` object returned by `get_page`, check the table below.
- 🚨 **Note**
    - HTML Attribute: `<input value="default">` → always returns `"default"`
    - JS Property: `input.value` → changes to `"user input"` when typed

| Category            | Method                        | Description                                       | Notes / Comparison                         |
| ------------------- | ----------------------------- | ------------------------------------------------- | ------------------------------------------ |
| **Text**            | `all_text_contents()`         | Returns a list of text from **all elements**      | Similar to `all_inner_texts()`             |
|                     | `text_content()`              | Returns visible text of the **first element**     | Similar to `innerText` (not `textContent`) |
|                     | `inner_text()`                | Same as `text_content()`                          | Actual visible text                        |
|                     | `all_inner_texts()`           | List of visible text from all elements            | Similar to `all_text_contents()`           |
| **Attribute**       | `get_attribute('attr')`       | Returns HTML attribute (`href`, `src`, `class`)   | Static, as written in HTML                 |
| **Property**        | `get_property('prop')`        | Returns live DOM property (`value`, `checked`)    | Useful for dynamic state                   |
| **HTML / Value**    | `inner_html()`                | Returns **inner HTML** of element                 | Only inside structure                      |
|                     | `outer_html()`                | Returns element’s full HTML                       | Includes element itself                    |
|                     | `input_value()`               | Returns current value of form elements            | More accurate than `get_attribute('value')`|
|                     | `select_option()`             | Returns `<option>` info from `<select>`           | Shows selected state                       |
| **State (Boolean)** | `is_visible()`                | Is element visible                                | True/False                                 |
|                     | `is_hidden()`                 | Is element hidden                                 | True/False                                 |
|                     | `is_enabled()`                | Is element enabled (clickable)                    | True/False                                 |
|                     | `is_disabled()`               | Is element disabled                               | True/False                                 |
|                     | `is_editable()`               | Is element editable                               | True/False                                 |
|                     | `is_checked()`                | Is checkbox/radio checked                         | True/False                                 |
| **Advanced**        | `evaluate("JS func", arg)`    | Runs JS on first element                          | Flexible extraction                        |
|                     | `evaluate_all("JS func", arg)`| Runs JS on all elements, returns list             | Useful for batch data                      |

<br>
<br>

## 6. FAQ

- **Browser launch error after install**
    - You must install the browser with:  
      `python -m playwright install chromium` (check Linux options carefully)

- **Doesn’t work on some URLs**
    - Please open a GitHub issue so we can check.

<br>
<br>
