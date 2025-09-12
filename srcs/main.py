import sys
from pathlib import Path

current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from pw_simple_scraper import scrape_html, scrape_context, scrape_href, ScrapeResult

# test

def main():
    TEST_URL = "https://asml.dkyobobook.co.kr/content/contentList.ink?brcd=&sntnAuthCode=&contentAll=Y&cttsDvsnCode=001&ctgrId=&orderByKey=publDate&selViewCnt=20&pageIndex=1&recordCount=20"
    TEST_CSS_SELECTOR = "#container > div > div.book_resultTxt > div > span > span"
    res = scrape_context(TEST_URL, TEST_CSS_SELECTOR, headless=True, timeout=10)
    print(res.result)

if __name__ == "__main__":
    main()
