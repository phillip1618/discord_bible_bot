import discord

import requests
import ast
import os

import datetime
import pytz

from time import sleep


class VOTD:
    def __init__(self):
        self.votd = self.get_votd()

    def get_votd(self):
        votd_response = requests.get('https://www.biblegateway.com/votd/get/?format=json&version=ESV&callback=BG.votdWriteCallback')
        votd_response_text = votd_response.text
        votd_json_str = votd_response_text[21:-2]
        votd_json = ast.literal_eval(votd_json_str)
        votd_verse = votd_json['votd']['text'][7:-7]

        if "&#8220" or "&#8221" in votd_verse:
            votd_verse = votd_verse.replace("&#8220;", "'")
            votd_verse = votd_verse.replace("&#8221;", "'")

        votd_reference = votd_json['votd']['display_ref']
        votd_final = '"' + votd_verse + '" -' + votd_reference

        return votd_final

    def votd_daily(self):
        webhook = discord.Webhook.from_url(os.getenv('VOTD_WEBHOOK_URL'), adapter=discord.RequestsWebhookAdapter())
        while True:
            datetime_now = datetime.datetime.now(pytz.timezone('US/Pacific'))
            if datetime_now.hour == 8 and datetime_now.minute == 30:
                self.votd = self.get_votd()
                webhook.send(self.votd)
                sleep(61)
