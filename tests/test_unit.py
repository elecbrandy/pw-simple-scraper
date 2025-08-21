import pytest
from pw_simple_scraper.core import scrape_context
from pw_simple_scraper.model import ScrapeResult
from pw_simple_scraper import utils

def test_validation_errors():
    with pytest.raises(TypeError):
        scrape_context(123, "a")
    with pytest.raises(ValueError):
        scrape_context("", "a")
    with pytest.raises(TypeError):
        scrape_context("http://x", 123)
    with pytest.raises(ValueError):
        scrape_context("http://x", "")

def test_model_to_dict():
    s = ScrapeResult(url="u", selector="s", result=["a","b","c"])
    d = s.to_dict()
    assert d["count"] == 3 and d["url"] == "u" and d["selector"] == "s"

def test_utils_headers_and_uapool():
    headers = utils.realistic_headers()
    assert "Accept" in headers and "Accept-Language" in headers
    assert isinstance(utils.UA_POOL, list) and len(utils.UA_POOL) >= 3
