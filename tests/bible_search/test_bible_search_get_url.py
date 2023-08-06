import pytest

from scripts.bible_search import BibleSearch


def test_get_url_1():
    query = '#search Matthew 3:20!NIV'
    bible_search = BibleSearch(query)

    url = "https://www.biblegateway.com/passage/?search=Matthew3%3A20&version=NIV"

    assert bible_search.get_url('Matthew3:20', 'NIV') == url


def test_get_url_2():
    query = '#search Matthew 3:20, John 1:15!NLT'
    bible_search = BibleSearch(query)

    url = "https://www.biblegateway.com/passage/?search={reference_string}&version={version}".format(
        reference_string='Matthew3%3A20%2CJohn1%3A15',
        version='NLT'
    )

    assert bible_search.get_url('Matthew3:20,John1:15', 'NLT') == url
