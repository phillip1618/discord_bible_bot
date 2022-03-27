import os
import sentry_sdk

from dotenv import load_dotenv
from discord_client import DiscordClient

load_dotenv()

if (os.getenv('SENTRY_PROD') == 'PROD'):
    sentry_sdk.init(os.getenv('SENTRY_SDK_INIT'), traces_sample_rate=1.0)

client = DiscordClient()

prod_bool = os.getenv('PROD')
if prod_bool == 'True':
    client.run(os.getenv('TOKEN_PROD'))
else:
    client.run(os.getenv('TOKEN_DEV'))
