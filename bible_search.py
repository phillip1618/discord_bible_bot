import re

from urllib.request import urlopen
from bs4 import BeautifulSoup

class BibleSearch:
    def __init__(self, query):
        self.query = query
        self.verses_list = self.get_verses_list()

    def separate_query(self):
        search = self.query[7:]
        search = search.replace(" ", "")

        if '!' in search:
            search_components = search.split("!")
        else:
            search_components = [search, 'ESV']

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
                formatted_verse += verse[0] + ' ' + verse[1].upper()
                str_index += 2
            else:
                formatted_verse += verse[0].upper()
                str_index += 1

            while not verse[str_index].isdigit():
                formatted_verse += verse[str_index]
                str_index += 1

            formatted_verse += ' ' + verse[str_index:]
            formatted_verse_list.append(formatted_verse)

        self.verse_reference = formatted_verse_list
        return formatted_verse_list
    
    def format_passage_text(self, passage_text_list, formatted_verse_list):

        n = len(passage_text_list)

        for i in range(n):
            passage_text_list[i] = passage_text_list[i].replace("\xa0", " ")
            passage_text_list[i] = re.sub('\([A-Z]\)', '', passage_text_list[i])
            passage_text_list[i] = re.sub('\([A-Z][A-Z]\)', '', passage_text_list[i])
            passage_text_list[i] = re.sub('\[[a-z]\]', '', passage_text_list[i])
            passage_text_list[i] = re.sub('\[[a-z][a-z]\]', '', passage_text_list[i])

            passage_text_list[i] += '-' + formatted_verse_list[i]
        
        return passage_text_list
    
    def get_verses_list(self):
        search_components = self.separate_query()
        url = self.get_url(search_components)
        passage_text_list = self.get_passage_text(url)

        if passage_text_list:
            formatted_verse_list = self.get_verses(search_components)
            verses_list = self.format_passage_text(passage_text_list, formatted_verse_list)
            return verses_list
        else:
            verses_list = []
            return verses_list

if __name__ == '__main__':
    BibleSearchx = BibleSearch('#search Genesis 1:1-9, John 1:1-9!ESV')
    print(BibleSearchx.get_verses_list())