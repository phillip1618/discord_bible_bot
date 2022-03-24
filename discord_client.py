import discord
import requests
import ast
import os
import datetime

from time import sleep
from dotenv import load_dotenv
from threading import Thread

from bible_search import BibleSearch

load_dotenv()

class DiscordClient(discord.Client):
    def __init__(self):
        super().__init__()

        self.votd = self.get_votd()

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))
        votd_thread = Thread(target = self.votd_daily, daemon = True)
        votd_thread.start()

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('#votd'):

            await message.channel.send(self.votd)

        if message.content.startswith('#search '):

            bible_search = BibleSearch(message.content)
            
            if bible_search.passage_dictionary:
                verse_ind = 0
                for verse in bible_search.passage_dictionary.values():
                    n = len(verse)

                    if n > 10000:
                        error_message = 'The length of queried passage, {0}, is too long. The passage length limit may not exceed 10000 characters. Please query for a shorter passage.'
                        error_message = error_message.format(bible_search.verse_reference[verse_ind])
                        await message.channel.send(error_message)
                        await message.channel.send('_ _')
                        verse_ind += 1
                        continue

                    iter = n // 2000
                    if iter == 0:
                        await message.channel.send(verse)
                    else:
                        verse_indices_list = self.get_verse_indices_list(verse)

                        iter = len(verse_indices_list)//2

                        for i in range(iter):
                            await message.channel.send(verse[verse_indices_list[2*i]:verse_indices_list[2*i+1]])

                    await message.channel.send('_ _')
                    verse_ind += 1
            else:
                await message.channel.send('Invalid query. Please input appropriate query for Bible verses.')

    def get_votd(self):
        votd_response = requests.get('https://www.biblegateway.com/votd/get/?format=json&version=ESV&callback=BG.votdWriteCallback')
        votd_text = votd_response.text
        votd_string_dict = votd_text[21:-2]
        votd_dict = ast.literal_eval(votd_string_dict)
        votd_verse = votd_dict['votd']['text'][7:-7]

        if "&#8220" or "&#8221" in votd_verse:
            votd_verse = votd_verse.replace("&#8220;", "'")
            votd_verse = votd_verse.replace("&#8221;", "'")

        votd_ref = votd_dict['votd']['display_ref']  
        votd_final = '"' + votd_verse + '" -' + votd_ref

        return votd_final

    def votd_daily(self):
        webhook = discord.Webhook.from_url(os.getenv('VOTD_WEBHOOK_URL'), adapter=discord.RequestsWebhookAdapter())
        while True:
            if datetime.datetime.utcnow().hour == 16 and datetime.datetime.utcnow().minute == 30:
                self.votd = self.get_votd()
                webhook.send(self.votd)
                sleep(61)

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