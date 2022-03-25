import discord
import requests
import datetime
import ast
import os
import datetime

from time import sleep

class VOTD:
    def __init__(self):
        self.votd = self.get_votd()

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
