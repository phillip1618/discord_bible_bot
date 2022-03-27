import discord

from dotenv import load_dotenv
from threading import Thread

from bible_search import BibleSearch
from votd import VOTD

load_dotenv()


class DiscordClient(discord.Client):
    def __init__(self):
        super().__init__()
        self.votd = VOTD()

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))
        votd_thread = Thread(target=self.votd.votd_daily, daemon=True)
        votd_thread.start()

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('#votd'):

            await message.channel.send(self.votd.votd)

        if message.content.startswith('#search '):
            bible_search = BibleSearch(message.content)
            bible_messages_dictionary = bible_search.messages_dictionary

            if not bible_messages_dictionary:
                await message.channel.send(
                    'Invalid query. Please input appropriate query for Bible passages.'
                )
                return

            for messages_key in bible_messages_dictionary.keys():
                messages_list = bible_messages_dictionary[messages_key]

                for message_element in messages_list:
                    await message.channel.send(message_element)
