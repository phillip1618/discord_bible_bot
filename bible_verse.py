from urllib.request import urlopen
from bs4 import BeautifulSoup

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

    def get_passage_text(self, url):
        passage_text_list = []
        
        page = urlopen(url)
        html = page.read().decode("utf-8")

        #print(html)
        soup = BeautifulSoup(html, 'html.parser')
        html_text_list = soup.find_all('div', class_='passage-text')
        #print(html_text_list)

        for html in html_text_list:
            chapter_num = html.find('span', class_='chapternum').get_text()
            passage_text = html.find('p').text
            passage_text_list.append(passage_text)

        return passage_text_list

    def format_passage_text(self, passage_text_list):
        return
    
    def get_verse(self):
        return

if __name__ == '__main__':
    x = BibleVerse()
    y = x.separate_query('#search Genesis 1:1-9, John 1:1-9!ESV')
    print(y)
    z = x.get_url(y)
    print(z)

    a = x.get_passage_text(z)

    print(a)