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
            
            for verse in bible_search.verses_list:
                await message.channel.send(verse)

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