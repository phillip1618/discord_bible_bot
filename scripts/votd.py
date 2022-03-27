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

    def replace_unicode_decimals_codes(self, votd_verse):
        replace_bool = True

        while replace_bool:
            if '&#' in votd_verse:
                index = votd_verse.find('&#')
                decimal_code = int(votd_verse[index+2:index+6])
                character = chr(decimal_code)
                votd_verse = votd_verse.replace(votd_verse[index:index+6], character)
            else:
                replace_bool = False

        return votd_verse

    def get_votd(self):
        votd_response = requests.get('https://www.biblegateway.com/votd/get/?format=json&version=ESV&callback=BG.votdWriteCallback')
        votd_response_text = votd_response.text
        votd_json_str = votd_response_text[21:-2]
        votd_json = ast.literal_eval(votd_json_str)
        votd_verse = votd_json['votd']['text'][7:-7]
        votd_verse = self.replace_unicode_decimals_codes(votd_verse)

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


if __name__ == '__main__':
    votd = VOTD()
    print(votd.replace_unicode_decimals_codes('I am a jaguar&#8220 and I like pie &#8224!'))
