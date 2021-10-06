from urllib.request import urlopen

class BibleVerse:
    def __init__(self):
        self.verse = self.get_verse()

    def separate_query(self, query):
        search = query[7:]
        search = search.replace(" ", "")
        search_components = search.split("!")

        return search_components

    
    def get_url(self, search_components):

        verses = search_components[0]
        version = search_components[1]

        verses = verses.replace(":", "%3A")
        verses = verses.replace(",", "%2C")

        url = "https://www.biblegateway.com/passage/?search=" + verses + "&version=" + version

        return url

    def get_html(self, url):
        return

    def get_verse(self):
        return

if __name__ == '__main__':
    x = BibleVerse()
    y = x.separate_query('#search Genesis 1:1-9, John 1:1-9!ESV')
    print(y)
    z = x.get_url(y)
    print(z)