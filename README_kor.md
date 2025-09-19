# pw-simple-scraper

[![PyPI](https://img.shields.io/pypi/v/pw-simple-scraper.svg)](https://pypi.org/project/pw-simple-scraper/)
[![Python](https://img.shields.io/pypi/pyversions/pw-simple-scraper.svg)](https://pypi.org/project/pw-simple-scraper/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#license)

<br>

> **‼️ 브라우저 생성, 헤더 설정 같은 반복 작업은 잊고, 스크래핑에만 집중하기 ‼️**

<br>

## 목차
- [1. 주요기능](#1-주요기능)
- [2. 설치방법](#2-설치방법)
- [3. 사용방법](#3-사용방법)
- [4. 사용예시](#4-사용예시)
- [5. Playwright 관련 메서드 정리](#5-playwright-관련-메서드-정리)
- [6. FAQ](#FAQ)

<br>
<br>

## 1. 주요기능
- [Playwright](https://playwright.dev) 을 기반으로 한 스크래퍼 라이브러리 입니다.
- `async with` 구문을 통해 브라우저와 페이지의 생명 주기를 자동으로 관리합니다.
- Playwright 객체를 반환하기 때문에, _**Playwright이 제공하는 강력한 모든 기능을 그대로 사용**_ 할 수 있습니다!
- ⚡️빠름⚡️

<br>
<br>

## 2. 설치방법


``` bash
# 1. Playwright 설치
pip install playwright

# 2-1. Chromium 설치 (macOS / Windows)
python -m playwright install chromium

# 2-2. Chromium 설치 (Linux)
python -m playwright install --with-deps chromium

# 3. pw-simple-scraper 설치
pip install pw-simple-scraper
```

- 이 스크래퍼는 `Playwright` 기반으로 작동하기 때문에, `Playwright` 라이브러리와 `Chromium` 브라우저가 필요합니다.

<br>
<br>

## 3. 사용방법

> `get_page`의 결과로 반환된 `Page` 타입의 객체를 어떻게 다뤄야할지 모르겠다면? -> [Playwright 관련 메서드 정리](#5-playwright-관련-메서드-정리)

<br>

1. `async with PlaywrightScraper() as scraper`
    - 스크래퍼 인스턴스를 만들어줍시다.
2. `async with scraper.get_page("http://www.example.com/") as page:`
    - get_page 메소드를 통해 페이지 컨텍스트를 가져옵시다.
3. 이제 `page` 요소에 Playwright의 다양한 기능을 직접 사용할 수 있습니다.

<br>

#### 🖥️ 코드 예시
``` python
import asyncio
from pw_simple_scraper import PlaywrightScraper

async def main():
    # 스크레퍼 인스턴스 생성
    async with PlaywrightScraper() as scraper:
        # get_page()를 통해 페이지 컨텍스트를 얻음
        async with scraper.get_page("http://www.example.com/") as page:
            # >>>> 이 블록에서 page를 조작하면 됩니다! <<<<

```

<br>
<br>

## 4. 사용예시

> `get_page`의 결과로 반환된 `Page` 타입의 객체를 어떻게 다뤄야할지 모르겠다면? -> [Playwright 관련 메서드 정리](#5-playwright-관련-메서드-정리)

### 4-1. 제목/텍스트/속성 추출

#### 🖥️ 코드 예시

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

            print("페이지 제목:", title)
            print("첫 번째 명언:", first_quote)
            print("명언 리스트 (앞 3개):", quotes[:3])
            print("첫 번째 저자 링크:", first_author_link)

if __name__ == "__main__":
    asyncio.run(main())
```

#### ⬇️ 결과 예시

``` bash
페이지 제목: Quotes to Scrape
첫 번째 명언: “The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”
명언 리스트 (앞 3개): ["The world as we have created it is a process of our thinking...", "It is our choices, Harry, that show what we truly are...", "There are only two ways to live your life..."]
첫 번째 저자 링크: /author/Albert-Einstein
```

### 4-2. images & links — 이미지/상세 링크 절대경로로 수집

#### 🖥️ 코드 예시

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

            print("이미지 URL 5개:", abs_imgs[:5])
            print("책 링크 5개:", abs_books[:5])

if __name__ == "__main__":
    asyncio.run(main())
```

#### ⬇️ 결과 예시

``` bash
이미지 URL 5개: [
  'https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg',
  'https://books.toscrape.com/media/cache/26/0c/260c6ae16bce31c8f8c95daddd9f4a1c.jpg',
  'https://books.toscrape.com/media/cache/3e/ef/3eef99c9d9adef34639f510662022830.jpg',
  'https://books.toscrape.com/media/cache/32/51/3251cf3a3412f53f339e42cac2134093.jpg',
  'https://books.toscrape.com/media/cache/be/a5/bea5697f2534a2f86a3ef27b5a8c12a6.jpg'
]
책 링크 5개: [
  'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html',
  'https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html',
  'https://books.toscrape.com/catalogue/soumission_998/index.html',
  'https://books.toscrape.com/catalogue/sharp-objects_997/index.html',
  'https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html'
]
```

---

### 4-3. evaluate JSON — DOM을 JSON 객체로 변환

#### 🖥️ 코드 예시

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

#### ⬇️ 결과 예시

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

## 5. Playwright 관련 메서드 정리

- `get_page`의 결과로 반환된 `Page` 타입의 객체를 어떻게 다뤄야할지 모르겠다면, 아래 표를 살펴봅시다.
- 🚨 **주의**
    - HTML 속성(Attribute): `<input value="초기값">` → 항상 `"초기값"` 반환
    - JS 프로퍼티(Property): `input.value` → 사용자가 입력하면 `"사용자 입력값"`으로 바뀜

| 카테고리               | 메서드                         | 설명                                               | 특징/비교                                  |
| ------------------ | --------------------------- | ------------------------------------------------ | -------------------------------------- |
| **텍스트(Text)**      | `all_text_contents()`       | 선택된 **모든 요소**의 텍스트를 리스트로 반환                      | `all_inner_texts()`와 유사 (보이는 텍스트만)     |
|                    | `text_content()`            | 선택된 **첫 번째 요소**의 보이는 텍스트 반환                      | `innerText`와 유사, `textContent`와는 차이 있음 |
|                    | `inner_text()`              | `text_content()`와 동일하게 보이는 텍스트 반환                | 사용자가 실제로 보는 값                          |
|                    | `all_inner_texts()`         | 모든 요소의 보이는 텍스트 리스트 반환                            | `all_text_contents()`와 유사              |
| **속성(Attribute)**  | `get_attribute('속성명')`      | HTML 속성값 반환 (`href`, `src`, `class` 등)           | HTML에 작성된 값 그대로 가져옴                    |
| **프로퍼티(Property)** | `get_property('프로퍼티명')`     | DOM 객체의 실시간 값 반환 (`value`, `checked` 등)          | 동적인 상태 확인 시 유용                         |
| **HTML / 값**       | `inner_html()`              | 요소의 **내부 HTML** 반환                               | 태그 내부 구조                               |
|                    | `outer_html()`              | 요소 자체 포함한 HTML 반환                                | 요소 전체                                  |
|                    | `input_value()`             | `<input>`, `<textarea>`, `<select>`의 **현재 값** 반환 | `get_attribute('value')`보다 정확          |
|                    | `select_option()`           | `<select>`에서 선택된 `<option>` 정보 반환                | 현재 선택 상태 확인                            |
| **상태(Boolean)**    | `is_visible()`              | 요소가 화면에 보이는지 여부                                  | True/False                             |
|                    | `is_hidden()`               | 요소가 숨겨져 있는지 여부                                   | True/False                             |
|                    | `is_enabled()`              | 요소가 활성화(클릭 가능) 상태인지                              | True/False                             |
|                    | `is_disabled()`             | 요소가 비활성화 상태인지                                    | True/False                             |
|                    | `is_editable()`             | 요소가 편집 가능한 상태인지                                  | True/False                             |
|                    | `is_checked()`              | 체크박스/라디오가 선택되었는지                                 | True/False                             |
| **고급 추출**          | `evaluate("JS 함수", 인자)`     | 첫 번째 요소에 대해 JS 코드 실행 결과 반환                       | 복잡한 정보 추출 가능                           |
|                    | `evaluate_all("JS 함수", 인자)` | 모든 요소에 대해 JS 실행 결과 리스트 반환                        | 다수 요소 처리에 유용                           |


<br>
<br>

## 6. FAQ

- **설치했는데 브라우저 실행 오류**
    - `python -m playwright install chromium` 으로 브라우저를 꼭 설치해야 합니다. (리눅스 옵션 주의)

- **특정 url에서 작동하지 않아요**
    - 깃 이슈로 남겨주시면 확인하겠습니다.

<br>
<br>
