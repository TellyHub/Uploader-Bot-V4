


import os
import time
import psutil
import shutil
import string
import asyncio

from speedtest import Speedtest
from pyrogram import Client, filters
from asyncio import TimeoutError
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, ForceReply
from plugins.config import Config
from plugins.script import Translation
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from plugins.database.add import add_user_to_database
from plugins.functions.forcesub import handle_force_subscribe
from pyrogram import enums, StopPropagation

@Client.on_message(filters.command(["start"]) & filters.private)
async def start(bot, update):
    if not update.from_user:
        return await update.reply_text("😬 Something went wrong with your profile at telegram or Pyrogram side.")
    await add_user_to_database(bot, update)
    await bot.send_message(
        Config.LOG_CHANNEL,
           f"#NEW_USER: \n\nNew User [{update.from_user.first_name}](tg://user?id={update.from_user.id}) started @{Config.BOT_USERNAME} !!"
    )
    
    if Config.UPDATES_CHANNEL:
      fsub = await handle_force_subscribe(bot, update)
      if fsub == 400:
        return
    await update.reply_text(
        text=Translation.START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=Translation.START_BUTTONS
    )


@Client.on_message(filters.command(["rate"]) & filters.private)
async def rate(bot, update):
            await bot.forward_messages(update.chat.id, "@Super_botz", Config.RATE_MSG_ID)
        
@Client.on_message(filters.private & filters.command("me"))
async def info_handler(bot, update):


    if update.from_user.last_name:
        last_name = update.from_user.last_name
    else:
        last_name = "None"

  
    await update.reply_text(  
        text=Translation.INFO_TEXT.format(update.from_user.first_name, last_name, update.from_user.username, update.from_user.id, update.from_user.mention, update.from_user.dc_id, update.from_user.language_code, update.from_user.status),             
        disable_web_page_preview=True,
        reply_markup=Translation.BUTTONS
    
    )
@Client.on_message(filters.private & filters.command("plan"))
async def upgrade(bot, update):  
    await update.reply_text(  
        text=Translation.UPGRADE_TEXT,             
        disable_web_page_preview=True,
        reply_markup=Translation.BUTTONS
    
    )
@Client.on_message(filters.command(["myspeed"]) & filters.private)
async def speed(bot, update):
    try:
        spg = await update.reply_text("Running Speed Test . . . ")
    except Exception as er:
        print(er, 13)
        spg = await bot.send_message(
            text=f'Running speedtest....',
            chat_id=update.message.chat.id,
            reply_to_message_id=update.id,
            parse_mode=enums.ParseMode.HTML
        )
    
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    path = (result['share'])
    try:
        print('Line 28', test)
    except Exception as ere:
        print(ere, '30')
        pass
    string_speed = f'''
<b>Server</b>
<b>Name:</b> <code>{result['server']['name']}</code>
<b>Country:</b> <code>{result['server']['country']}, {result['server']['cc']}</code>
<b>Sponsor:</b> <code>{result['server']['sponsor']}</code>
    
<a href="{path}"><b>SpeedTest Results</b></a>
<b>Upload:</b> <code>{speed_convert(result['upload'] / 8)}</code>
<b>Download:</b>  <code>{speed_convert(result['download'] / 8)}</code>
<b>Ping:</b> <code>{result['ping']} ms</code>
<b>ISP:</b> <code>{result['client']['isp']}</code>
'''

    await spg.delete()
    try:
        print(path, result)
    except Exception as pri:
        print(pri)
        
    try:
        await update.reply_photo(path, caption=string_speed)
    except Exception as cv:
        print("Error 60 ", cv)
        await update.reply_text(string_speed, disable_web_page_preview=True)
        
def speed_convert(size):
    """Hi human, you can't read bytes?"""
    power = 2 ** 10
    zero = 0
    units = {0: "", 1: "Kb/s", 2: "MB/s", 3: "Gb/s", 4: "Tb/s"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"    
