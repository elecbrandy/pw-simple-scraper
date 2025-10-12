import pytest
from playwright.async_api import TimeoutError, expect
from pw_simple_scraper import PlaywrightScraper

pytestmark = pytest.mark.e2e


def _u(http_server: str, path: str) -> str:
    return f"{http_server}/{path}"


@pytest.mark.asyncio
async def test_index_list_extraction(http_server):
    async with PlaywrightScraper(headless=True, timeout=5) as scraper:
        async with scraper.get_page(_u(http_server, "index.html")) as (page, _):
            items_locator = page.locator("li.item")
            assert await items_locator.count() == 3
            assert await items_locator.first.text_content() == "First"

            results = await items_locator.all_text_contents()
            assert all(isinstance(x, str) and x for x in results)


@pytest.mark.asyncio
async def test_links_href_extraction(http_server):
    async with PlaywrightScraper(headless=True, timeout=5) as scraper:
        async with scraper.get_page(_u(http_server, "links.html")) as (page, _):
            locator = page.locator("a.nav")
            hrefs = await locator.evaluate_all(
                "els => els.map(el => el.getAttribute('href'))"
            )
            assert set(hrefs) == {"/a.html", "/b.html"}


@pytest.mark.asyncio
async def test_dynamic_wait_visible_after_insert(http_server):
    async with PlaywrightScraper(headless=True, timeout=5) as scraper:
        async with scraper.get_page(_u(http_server, "dynamic.html")) as (page, _):
            late_element = page.locator("#late")
            await expect(late_element).to_have_count(1)
            assert await late_element.text_content() == "I came late"


@pytest.mark.asyncio
async def test_dynamic_list_insert(http_server):
    async with PlaywrightScraper(headless=True, timeout=5) as scraper:
        async with scraper.get_page(_u(http_server, "dynamic_insert.html")) as (
            page,
            _,
        ):
            items_locator = page.locator("li.item")
            await expect(items_locator).to_have_count(3)

            items = await items_locator.all_text_contents()
            assert items == ["One", "Two", "Three"]


@pytest.mark.asyncio
async def test_dynamic_href_added_later(http_server):
    async with PlaywrightScraper(headless=True, timeout=5) as scraper:
        async with scraper.get_page(_u(http_server, "dynamic_href.html")) as (page, _):
            href = await page.locator("a.later").get_attribute("href")
            assert href == "/a.html"


@pytest.mark.asyncio
async def test_attrs_mixed_href_filter(http_server):
    async with PlaywrightScraper(headless=True, timeout=5) as scraper:
        async with scraper.get_page(_u(http_server, "attrs_mixed.html")) as (page, _):
            locator = page.locator(".nav")
            all_hrefs = await locator.evaluate_all(
                "els => els.map(el => el.getAttribute('href'))"
            )
            # None이 아니거나, 공백이 아닌 href만 필터링
            filtered_hrefs = [href for href in all_hrefs if href and href.strip()]
            assert set(filtered_hrefs) == {"/ok.html", "javascript:void(0)"}


@pytest.mark.asyncio
async def test_empty_text_is_filtered_and_empty_href_ignored(http_server):
    async with PlaywrightScraper(headless=True, timeout=5) as scraper:
        async with scraper.get_page(_u(http_server, "empty.html")) as (page, _):
            # 텍스트 필터링
            all_texts = await page.locator(".has-text").all_text_contents()
            filtered_texts = [t.strip() for t in all_texts if t.strip()]
            assert filtered_texts == ["Not empty"]

            # href 필터링
            hrefs = await page.locator("a.maybe-href").evaluate_all(
                "els => els.map(el => el.getAttribute('href')).filter(Boolean)"
            )
            assert hrefs == []


@pytest.mark.asyncio
async def test_encoding_utf8_paragraphs(http_server):
    async with PlaywrightScraper(headless=True, timeout=5) as scraper:
        async with scraper.get_page(_u(http_server, "encoding_utf8.html")) as (
            page,
            _,
        ):
            results = await page.locator("p.ko").all_text_contents()
            assert len(results) == 2
            assert ("안녕하세요" in results[0]) and ("세계" in results[0])
            assert ("탭" in results[1]) and ("혼합" in results[1])


@pytest.mark.asyncio
async def test_longlist_count_and_edges(http_server):
    async with PlaywrightScraper(headless=True, timeout=5) as scraper:
        async with scraper.get_page(_u(http_server, "longlist.html")) as (page, _):
            locator = page.locator("li.row")
            assert await locator.count() == 30
            assert await locator.first.text_content() == "Item 01"
            assert await locator.last.text_content() == "Item 30"


@pytest.mark.asyncio
async def test_nested_headlines_text_and_links(http_server):
    async with PlaywrightScraper(headless=True, timeout=5) as scraper:
        async with scraper.get_page(_u(http_server, "nested.html")) as (page, _):
            locator = page.locator(".card h2 .headline")
            texts = await locator.all_text_contents()
            assert texts == ["Alpha", "Beta"]

            hrefs = await locator.evaluate_all(
                "els => els.map(el => el.getAttribute('href'))"
            )
            assert hrefs == ["/a.html", "/b.html"]


@pytest.mark.asyncio
async def test_visibility_toggle(http_server):
    async with PlaywrightScraper(headless=True, timeout=5) as scraper:
        async with scraper.get_page(_u(http_server, "visibility.html")) as (page, _):
            text = await page.locator(".msg").text_content()
            assert text == "I will appear"


@pytest.mark.asyncio
async def test_missing_selector_raises(http_server):
    async with PlaywrightScraper(headless=True) as scraper:
        async with scraper.get_page(_u(http_server, "index.html")) as (page, _):
            with pytest.raises(TimeoutError):
                await page.locator(".does-not-exist").wait_for(timeout=2000)

