# save_results.py
import asyncio
import json
import csv
from urllib.parse import urljoin
from .pw_simple_scraper import PlaywrightScraper


# 결과 저장용 딕셔너리
example_results = {}


# 1. basic
async def example_basic():
    async with PlaywrightScraper() as scraper:
        async with scraper.get_page("https://quotes.toscrape.com/") as page:
            title = await page.title()
            first_quote = await page.locator("span.text").first.text_content()
            quotes = await page.locator("span.text").all_text_contents()
            first_author_link = await page.locator(".quote a").first.get_attribute("href")

            example_results["basic"] = {
                "title": title,
                "first_quote": first_quote,
                "quotes_count": len(quotes),
                "first_author_link": first_author_link,
            }

# 2. images & links
async def example_images_links():
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

            example_results["images_links"] = {
                "images": abs_imgs[:5],
                "book_links": abs_books[:5],
            }


# 3. evaluate JSON
async def example_evaluate():
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
            example_results["evaluate"] = items[:5]


# JSON 저장
def save_json():
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(example_results, f, ensure_ascii=False, indent=2)

async def main():
    await example_basic()
    await example_images_links()
    await example_evaluate()
    save_json()
    print("output.json 저장 완료")


if __name__ == "__main__":
    asyncio.run(main())
