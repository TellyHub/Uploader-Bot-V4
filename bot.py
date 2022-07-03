import os
from plugins.config import Config

from pyrogram import Client as sprbt
from pyrogram import filters
from plugins.__init__. import LOGGER 


if __name__ == "__main__" :
    # create download directory, if not exist
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)
    plugins = dict(root="plugins")
    sprbts = sprbt(
        "Uploader Bot",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        workers=100,
        plugins=plugins)
    sprbts.run()
