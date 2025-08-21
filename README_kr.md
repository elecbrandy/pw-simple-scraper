# pw-simple-scraper

> Python, Playwright 기반의 간편, 간단한 웹 스크래퍼

[![PyPI](https://img.shields.io/pypi/v/pw-simple-scraper.svg)](https://pypi.org/project/pw-simple-scraper/)
[![Python](https://img.shields.io/pypi/pyversions/pw-simple-scraper.svg)](https://pypi.org/project/pw-simple-scraper/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#license)

<br>

## 요약

- `pw-simple-scraper` 는 웹페이지에서 원하는 요소를 스크래핑 합니다.
- `URL + CSS` 셀렉터를 주면, 해당 요소들을 찾아서 문자열 리스트로 반환합니다.
- 결과는 `ScrapeResult` 객체에 담겨 반환되고, 그 안의 **`.result` (List[str])** 를 사용하면 됩니다.

<br>
<br>

## 설치 방법

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

## 사용법

``` python
from pw_simple_scraper import scrape_context, scrape_href

# 텍스트 추출
res = scrape_context("https://example.com", "h3")
print(res.result)   # ['h3-type-content1', 'h3-type-content2', ...]
print(res.count)    # n (스크래핑 갯수)

# 링크 추출
links = scrape_href("https://example.com", "a")
print(links.result) # ['https://www.iana.org/domains/example', ...]

# timeout 옵션 부여 (기본값 30초)
scrape_context("https://example.com", "something", timeout=10) # 10초
```

#### 결과는 `ScrapeResult` 객체

```python
@dataclass
class ScrapeResult:
    url: str
    selector: str
    result: List[str]       # 추출된 값 리스트
    count: int              # 값 개수
    fetched_at: datetime    # 실행 시각 (UTC)
```

<br>
<br>

## FAQ

- **설치했는데 브라우저 실행 오류**
    - `python -m playwright install chromium` 으로 브라우저를 꼭 설치해야 합니다. (리눅스 옵션 주의)

- **RuntimeError: All strategies failed 오류**
    - 셀렉터가 존재하지 않거나 로딩이 느릴 수 있습니다. **셀렉터를 다시 한번 확인** 하고, `timeout`을 좀 늘려보세요. 

- **iframe 내부 스크래핑**
    - 추후 지원 예정입니다.

- **xpath 지원**
    - 추후 지원 예정입니다.

- **robot.txt 지원**
    - robot.txt 을 존중여부를 플래그로 지정할 수 있도록 추후 지원 예정입니다.


<br>
<br>
