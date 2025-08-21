import pytest
from pw_simple_scraper import scrape_context, scrape_href

# 이 파일 전체를 e2e로 표시 (브라우저 실행 필요)
pytestmark = pytest.mark.e2e

def _u(http_server: str, path: str) -> str:
    return f"{http_server}/{path}"

def test_index_list_extraction(http_server):
    res = scrape_context(_u(http_server, "index.html"), "li.item", headless=True, timeout=5)
    assert res.count == 3
    assert res.first() == "First"
    assert all(isinstance(x, str) and x for x in res.result)

def test_links_href_extraction(http_server):
    res = scrape_href(_u(http_server, "links.html"), "a.nav", headless=True, timeout=5)
    assert res.count == 2
    assert set(res.result) == {"/a.html", "/b.html"}

def test_dynamic_wait_visible_after_insert(http_server):
    # dynamic.html 은 일정 시간 후 #late 요소가 생성되어야 함
    res = scrape_context(_u(http_server, "dynamic.html"), "#late", headless=True, timeout=5)
    assert res.count == 1 and res.result[0] == "I came late"

def test_dynamic_list_insert(http_server):
    # dynamic_insert.html 은 li.item 이 지연 삽입됨
    res = scrape_context(_u(http_server, "dynamic_insert.html"), "li.item", headless=True, timeout=5)
    assert res.result == ["One", "Two", "Three"]

def test_dynamic_href_added_later(http_server):
    # 파일명이 dynamic_herf.html 임에 주의 (오타 그대로 사용)
    res = scrape_href(_u(http_server, "dynamic_href.html"), "a.later", headless=True, timeout=5)
    assert res.result == ["/a.html"]

def test_attrs_mixed_href_filter(http_server):
    # 빈 문자열/공백/누락된 href는 제외, javascript:void(0)은 포함
    res = scrape_href(_u(http_server, "attrs_mixed.html"), ".nav", headless=True, timeout=5)
    assert set(res.result) == {"/ok.html", "javascript:void(0)"}

def test_empty_text_is_filtered_and_empty_href_ignored(http_server):
    # 공백 텍스트는 필터링되어 "Not empty"만 남아야 함
    ctx = scrape_context(_u(http_server, "empty.html"), ".has-text", headless=True, timeout=5)
    assert ctx.result == ["Not empty"]
    # href 속성이 비어있는 경우 결과에서 제외
    hrefs = scrape_href(_u(http_server, "empty.html"), "a.maybe-href", headless=True, timeout=5)
    assert hrefs.result == []

def test_encoding_utf8_paragraphs(http_server):
    # 유니코드 텍스트가 잘 추출되는지 확인(정확 공백매칭 대신 부분 문자열 검사)
    res = scrape_context(_u(http_server, "encoding_utf8.html"), "p.ko", headless=True, timeout=5)
    assert res.count == 2
    assert ("안녕하세요" in res.result[0]) and ("세계" in res.result[0])
    assert ("탭" in res.result[1]) and ("혼합" in res.result[1])

def test_longlist_count_and_edges(http_server):
    res = scrape_context(_u(http_server, "longlist.html"), "li.row", headless=True, timeout=5)
    assert res.count == 30
    assert res.first() == "Item 01"
    assert res.result[-1] == "Item 30"

def test_nested_headlines_text_and_links(http_server):
    txt = scrape_context(_u(http_server, "nested.html"), ".card h2 .headline", headless=True, timeout=5)
    assert txt.result == ["Alpha", "Beta"]
    hrefs = scrape_href(_u(http_server, "nested.html"), ".card h2 .headline", headless=True, timeout=5)
    assert hrefs.result == ["/a.html", "/b.html"]

def test_visibility_toggle(http_server):
    res = scrape_context(_u(http_server, "visibility.html"), ".msg", headless=True, timeout=5)
    assert res.result == ["I will appear"]

def test_missing_selector_raises(http_server):
    with pytest.raises(RuntimeError):
        scrape_context(_u(http_server, "index.html"), ".does-not-exist", headless=True, timeout=2)
