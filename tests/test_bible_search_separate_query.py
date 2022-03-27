from scripts.bible_search import BibleSearch


def test_separate_query_1():
    query = '#search Matthew 3!NIV'
    bible_search = BibleSearch(query)
    
    assert bible_search.separate_query(query) == ['Matthew3', 'NIV']