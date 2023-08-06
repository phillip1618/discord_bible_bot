import pytest

from scripts.bible_search import BibleSearch


@pytest.mark.parametrize('query, expected_result', [
    ('#search Matthew 3!NIV', ['Matthew3', 'NIV']),
    ('#search Matthew 3', ['Matthew3', 'ESV']),
    ('#search Matthew 3NIV', ['Matthew3NIV', 'ESV']),
    ('$search Matthew 3:15!!NIV', ['Matthew3:15', '!NIV'])
])


def test_separate_query(query, expected_result):
    bible_search = BibleSearch(query)

    assert bible_search.separate_query(query) == expected_result
