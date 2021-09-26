import discord
import requests
import ast

class DiscordClient(discord.Client):
    def __init__(self):
        super().__init__()

        self.votd = self.get_votd()

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('$votd'):

            await message.channel.send(self.votd)

    def get_votd(self):
        votd_response = requests.get('https://www.biblegateway.com/votd/get/?format=json&version=ESV&callback=BG.votdWriteCallback')
        votd_text = votd_response.text
        votd_string_dict = votd_text[21:-2]
        votd_dict = ast.literal_eval(votd_string_dict)
        votd_verse = votd_dict['votd']['text'][7:-7]
        votd_ref = votd_dict['votd']['display_ref']  
        votd_final = '"' + votd_verse + '" -' + votd_ref

        return votd_final