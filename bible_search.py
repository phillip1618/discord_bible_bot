import re

from urllib.request import urlopen
from bs4 import BeautifulSoup

class BibleSearch:
    def __init__(self, query):
        self.query = query
        self.verses_list = self.get_verses_list()

    #separates query into a list of two components:
    #1. string of Bible verses references
    #2. Desired Bible version 
    def separate_query(self):
        search = self.query[7:]
        search = search.replace(" ", "")

        if '!' in search:
            search_components = search.split("!")
        else:
            search_components = [search, 'ESV']

        return search_components

    
    #obtain Bible Gateway url to extract data from
    def get_url(self, search_components):

        verses = search_components[0]
        version = search_components[1]

        verses = verses.replace(":", "%3A")
        verses = verses.replace(",", "%2C")

        url = "https://www.biblegateway.com/passage/?search=" + verses + "&version=" + version

        return url

    #obtain text via webscraping from Bible Gateway html documents
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

    #obtain list of verse references to passages
    def get_verses(self, search_components):
        verses = search_components[0]
        version = search_components[1]

        verses_list = verses.split(',')

        formatted_verse_list = []

        verified_verses = []

        for verse in verses_list:
            url = "https://www.biblegateway.com/passage/?search=" + verse + "&version=" + version
            page = urlopen(url)
            html = page.read().decode("utf-8")

            soup = BeautifulSoup(html, 'html.parser')
            html_text = soup.find('div', class_='passage-text')

            if html_text:
                verified_verses.append(verse)
            
        for verse in verified_verses:
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

                if str_index == len(verse):
                    break

            if str_index < len(verse):
                formatted_verse += ' ' + verse[str_index:]
            
            formatted_verse_list.append(formatted_verse)

        self.verse_reference = formatted_verse_list
        return formatted_verse_list
    
    #obtains new list of properly formatted passages
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
    
    #utilizes all written helper functions to output list of passages (need to refactor later)
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