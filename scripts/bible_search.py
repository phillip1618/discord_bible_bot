import re

from urllib.request import urlopen
from bs4 import BeautifulSoup


class BibleSearch:
    def __init__(self, query):
        self.query = query
        self.search_components = self.separate_query(self.query)
        self.passage_dictionary = self.generate_verified_passage_dictionary(self.search_components)
        self.messages_dictionary = self.generate_discord_messages(self.passage_dictionary)

    def verify_query(self, query):
        """
        Verifies if:
        - the query begins with substring '#search '
        - there exists at most one exclamation mark in the query
        """
        if not query.startswith('#search '):
            return False
        
        if query.count('!') > 1:
            return False

        return True
    
    def separate_query(self, query):
        """
        Separates query into a list of two components:
        1. string of Bible verses references
        2. Desired Bible version
        """
        search = query[7:]
        search = search.replace(" ", "")

        if '!' in search:
            separator_index = search.find('!')
            search_components = [search[:separator_index], search[separator_index+1:]]
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

    def get_verse_indices_list(self, verse):
        verse_indices_list = [0]
        counter = 0
        start_ind = 0
        end_ind = 0

        while len(verse[verse_indices_list[counter]:]) > 2000:
            start_ind = verse_indices_list[counter]
            end_ind = start_ind + 1999

            while verse[end_ind] != ' ' and verse[end_ind] != '.':
                end_ind -= 1

            verse_indices_list.append(end_ind + 1)
            verse_indices_list.append(end_ind + 1)
            counter += 2

        verse_indices_list.append(len(verse))

        return verse_indices_list

    def generate_discord_messages(self, passage_dictionary):
        passages = list(passage_dictionary.values())
        references = list(passage_dictionary.keys())
        messages_dictionary = {}

        for i in range(len(passages)):
            n = len(passages[i])

            if n > 10000:
                error_message = 'The length of queried passage, {reference}, is too long. The passage length limit may not exceed 10000 characters. Please query for a shorter passage.'.format(
                    reference=references[i]
                )
                messages_dictionary[references[i]] = [error_message]
            elif n // 2000 == 0:
                messages_dictionary[references[i]] = [passages[i]]
            else:
                messages = []
                passage_indices_list = self.get_verse_indices_list(passages[i])
                iter = len(passage_indices_list) // 2

                for j in range(iter):
                    messages.append(passages[i][passage_indices_list[2*j]:passage_indices_list[2*j+1]])

                messages_dictionary[references[i]] = messages

            if i < len(passages) - 1:
                blank_key = "blank{index}".format(index=i)
                messages_dictionary[blank_key] = ['_ _']

        return messages_dictionary


if __name__ == '__main__':
    BibleSearchx = BibleSearch('#search Matthew 3')
    passage_dictionary = BibleSearchx.passage_dictionary
    discord_messages_dictionary = BibleSearchx.generate_discord_messages(passage_dictionary)
