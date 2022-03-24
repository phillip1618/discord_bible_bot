import re

from urllib.request import urlopen
from bs4 import BeautifulSoup


class BibleSearch:
    def __init__(self, query):
        self.query = query
        self.search_components = self.separate_query(self.query)
        self.passage_dictionary = self.generate_verified_passage_dictionary(self.search_components)

    def separate_query(self, query):
        """
        Separates query into a list of two components:
        1. string of Bible verses references
        2. Desired Bible version
        """
        search = query[7:]
        search = search.replace(" ", "")

        if '!' in search:
            search_components = search.split("!")
        else:
            search_components = [search, 'ESV']

        return search_components

    def get_url(self, verse, version):
        """
        Generate Bible Gateway url to extract data from
        """
        verse = verse.replace(":", "%3A")
        verse = verse.replace(",", "%2C")

        url = "https://www.biblegateway.com/passage/?search={verse}&version={version}".format(
            verse=verse,
            version=version
        )

        return url

    def generate_passage_text(self, html_text):
        """
        Obtain text via webscraping from Bible Gateway html documents
        """
        passage_text = ''

        passage_text_html = html_text.find_all('p')
        for p in passage_text_html:
            passage_text += p.text

        return passage_text

    def format_verse(self, verse):
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

        return formatted_verse

    def format_passage_text(self, passage_text, formatted_verse):
        """
        Obtains new list of properly formatted passages
        """
        formatted_passage_text = passage_text.replace("\xa0", " ")
        formatted_passage_text = re.sub('\([A-Z]\)', '', formatted_passage_text)
        formatted_passage_text = re.sub('\([A-Z][A-Z]\)', '', formatted_passage_text)
        formatted_passage_text = re.sub('\[[a-z]\]', '', formatted_passage_text)
        formatted_passage_text = re.sub('\[[a-z][a-z]\]', '', formatted_passage_text)

        formatted_passage_text += '-' + formatted_verse

        return formatted_passage_text

    def generate_verified_passage_dictionary(self, search_components):
        verses_str = search_components[0]
        version = search_components[1]

        verses_list = verses_str.split(',')

        passage_dictionary = {}

        for verse in verses_list:
            url = self.get_url(
                verse=verse,
                version=version
            )
            page = urlopen(url)
            html = page.read().decode('utf-8')

            soup = BeautifulSoup(html, 'html.parser')
            html_text = soup.find('div', class_='passage-text')

            if html_text:
                formatted_verse = self.format_verse(verse)
                passage = self.generate_passage_text(html_text)
                formatted_passage = self.format_passage_text(passage, formatted_verse)
                passage_dictionary[formatted_verse] = formatted_passage

        return passage_dictionary


if __name__ == '__main__':
    BibleSearchx = BibleSearch('#search Genesis 1:1-9, John 1:1-9!ESV')
    print(BibleSearchx.passage_dictionary)
