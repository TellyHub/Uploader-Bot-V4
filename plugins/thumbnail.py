#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
from pyrogram import Client, filters 
from plugins.config import Config 

# the Strings used for this "thing"
from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)




@Client.on_message(filters.photo & filters.private)
def save_photo(bot, update):

    download_location = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
    bot.download_media(
        message=update,
        file_name=download_location
    )
    bot.send_message(
        chat_id=update.from_user.id,
        text=Translation.SAVED_CUSTOM_THUMB_NAIL,
        reply_to_message_id=update.id
    )
