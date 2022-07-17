# About

`discord_bible_bot` is a Discord Bot (Bible Bot) that currently lives in the Discord Server of Twitch streamer, phillip1618. The bot's purpose is to send a verse of the day and is to allow users to search for scripture in the Bible.

## Usage

In the "verse-of-the-day" text channel, there is a webhook that has been integrated called "Verse of the Day Bot", which receives a response from the Bible Gateway Verse of the Day API (<https://www.biblegateway.com/usage/votd/custom_votd/>) and sends the verse into the channel.

If users wish to reference the verse of the day, then they would have to type in `#votd` and the Bible Bot will send the verse.

The Bible bot also includes a search feature. The User queries for verses using this format: `#search {list of verses separated by commas}!{version}`. When the version isn't explicitly referenced, the default version becomes ESV (English Standard Version).

## Set-up

A Sentry account must be created, and a Sentry DSN must be obtained. An AWS account must also be created. A `.env` file must be set up with the following values:

```text
PROD='True' or 'False'
TOKEN_PROD=secret-discord-prod-token
TOKEN=secret-discord-dev-token
SENTRY_SDK_INIT=secret-sentry-dsn
SENTRY_PROD='DEV' or 'PROD'
VOTD_WEBHOOK_URL=secret-votd-discord-channel-webhook
```

The Discord Bot has been set up within an AWS EC2 instance (I use 'Amazon Linux 2 AMI') in order for the bot to be run on the cloud. Once the instance and connection to the instance has been set up, here are some further set up instructions:

1. Install python using `sudo yum install python3`
2. Install pip using `sudo yum install pip`
3. Install git using `sudo yum install git`
4. Clone the repo, and a new directory 'discord_bible_bot' will appear
5. Run `cd discord_bible_bot`
6. Install required python packages using `pip install -r requirements.txt`
7. Run the application as a background service using `nohup python3 bible_main.py </dev/null &>/dev/null &`

## Future Implementations

- Give the Bible bot scripture search capabilities
