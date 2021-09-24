import discord

class DiscordClient(discord.Client):
    def __init__(self):
        super().__init__()

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('$bibleverse'):
            await message.channel.send('omg Bible Bot')