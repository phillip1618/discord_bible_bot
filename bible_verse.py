class BibleVerse:
    def __init__(self):
        self.verse = self.get_verse()

    def format_query(self, query):
        query = query.replace(" ", "")
        query = query.replace(":", "%3A")
        query = query.replace(",", "%2C")

        return query

    def get_html(self, url):
        return

    def get_verse(self):
        return

if __name__ == '__main__':
    x = BibleVerse()
    print(x.format_query("Genesis 1:1-9, John 1:1-9"))