import pytest

from scripts.bible_search import BibleSearch


@pytest.mark.parametrize('verse, version, expected_url', [
    ('Matthew3:20', 'NIV', 'https://www.biblegateway.com/passage/?search=Matthew3%3A20&version=NIV'),
    ('Matthew3:20,John1:15', 'NLT', 'https://www.biblegateway.com/passage/?search=Matthew3%3A20%2CJohn1%3A15&version=NLT')
])

def test_get_url(verse, version, expected_url):
    query = "Genesis 1"
    bible_search = BibleSearch(query)
    
    assert bible_search.get_url(verse, version) == expected_url
