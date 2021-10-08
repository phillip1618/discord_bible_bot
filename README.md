# About

`discord_bible_bot` is a Discord Bot (Bible Bot) that currently lives in the Discord Server of Twitch streamer, phillip1618. The bot's purpose is to send a verse of the day and is to allow users to search for scripture in the Bible.

## Usage

In the "verse-of-the-day" text channel, there is a webhook that has been integrated called "Verse of the Day Bot", which receives a response from the Bible Gateway Verse of the Day API (https://www.biblegateway.com/usage/votd/custom_votd/) and sends the verse into the channel. 

If users wish to reference the verse of the day, then they would have to type in `#votd` and the Bible Bot will send the verse.

## Set-up

A `.env` file must be set up with the following values:

```
TOKEN=secret-discord-token
SENTRY_SDK_INIT=secret-sentry-dsn
SENTRY_PROD='DEV' or 'PROD'
VOTD_WEBHOOK_URL=secret-votd-discord-channel-webhook
```

The Discord Bot has been set up within an AWS EC2 instance (I use 'Amazon Linux 2 AMI') in order for the bot to be run on the cloud. Once the instance and connection to the instance has been set up, here are some further set up instructions:

1. Install python using `sudo yum install python3`
2. Install pip using `sudo yum install pip`
3. Install git using `sudo yum install git`
4. Clone the repo, and a new directory 'discord_bible_bot' will appear
5. Install required python packages using `pip install -r discord_bible_bot/requirements.txt`
6. Run the application as a background service using `nohup python3 bible_main.py </dev/null &>/dev/null &`

## Future Implementations

- Give the Bible bot scripture search capabilities