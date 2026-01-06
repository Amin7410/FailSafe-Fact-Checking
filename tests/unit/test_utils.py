
import pytest
from factcheck.utils.web_util import is_url, extract_hostname, clean_text

def test_is_url():
    assert is_url("https://google.com") is True
    assert is_url("http://localhost:8000") is True
    assert is_url("not a url") is False
    assert is_url("") is False

def test_clean_text():
    raw_text = "  Hello   World! \n "
    assert clean_text(raw_text) == "Hello World!"
    
    # Test removing heavy whitespace
    assert clean_text("A\tB") == "A B"

