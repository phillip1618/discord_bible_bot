import re

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

        soup = BeautifulSoup(html, 'html.parser')
        sample_html_text_list = soup.find_all('div')
        #print(sample_html_text_list)
        html_text_list = soup.find_all('div', class_='passage-text')

        for html in html_text_list:
            passage_text_html = html.find_all('p')
            passage_text = ''
            for p in passage_text_html:
                passage_text += p.text
            passage_text_list.append(passage_text)

        return passage_text_list

    def get_verses(self, search_components):
        verses = search_components[0]
        verses_list = verses.split(',')

        formatted_verse_list = []

        for verse in verses_list:

            formatted_verse = ''
            str_index = 0

            if verse[0].isdigit():
                formatted_verse += verse[0] + ' '
                str_index += 1

            while not verse[str_index].isdigit():
                formatted_verse += verse[str_index]
                str_index += 1

            formatted_verse += ' ' + verse[str_index:]
            formatted_verse_list.append(formatted_verse)

        return formatted_verse_list
    
    def format_passage_text(self, passage_text_list, formatted_verse_list):

        n = len(passage_text_list)

        for i in range(n):
            passage_text_list[i] = passage_text_list[i].replace("\xa0", " ")
            passage_text_list[i] = re.sub('\([A-Z]\)', '', passage_text_list[i])
            passage_text_list[i] = re.sub('\[[a-z]\]', '', passage_text_list[i])

            passage_text_list[i] += '-' + formatted_verse_list[i]
        
        return passage_text_list
    
    def get_verse(self):
        return

if __name__ == '__main__':
    BibleVerseo = BibleVerse()
    search_components = BibleVerseo.separate_query('#search Genesis 1:1-9, John 1:1-9!ESV')
    print(search_components)
    url = BibleVerseo.get_url(search_components)
    print(url)

    passage_text_list = BibleVerseo.get_passage_text(url)

    print(passage_text_list)

    formatted_verse_list = BibleVerseo.get_verses(search_components)
    print(formatted_verse_list)

    formatted_passage_text_list = BibleVerseo.format_passage_text(passage_text_list, formatted_verse_list)
    print(formatted_passage_text_list)