
from plugins.__init__ import *
import requests, urllib.parse, filetype, os, time, shutil, tldextract, asyncio, json, math
from PIL import Image
from plugins.config import Config
import time
from plugins.script import Translation

from pyrogram import filters
from pyrogram import Client, enums
from plugins.functions.forcesub import handle_force_subscribe
from plugins.functions.display_progress import humanbytes
from plugins.functions.help_uploadbot import DownLoadFile
from plugins.functions.display_progress import *
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from plugins.functions.ran_text import random_char
from plugins.database.add import add_user_to_database
from pyrogram.types import Thumbnail

@Client.on_message(filters.private & filters.regex(pattern=".*http.*"))

async def echo(bot, update: Message):


    LOGGER.info(update.from_user)
    url, _, youtube_dl_username, youtube_dl_password = get_link(update)
    if Config.HTTP_PROXY is not None:
        command_to_exec = [
            "yt-dlp",
            "--no-warnings",
            "--youtube-skip-dash-manifest",
            "-j",
            url,
            "--proxy", Config.HTTP_PROXY
        ]
    else:
        command_to_exec = [
            "yt-dlp",
            "--no-warnings",
            "--youtube-skip-dash-manifest",
            "-j",
            url
        ]
    if youtube_dl_username is not None:
        command_to_exec.append("--username")
        command_to_exec.append(youtube_dl_username)
    if youtube_dl_password is not None:
        command_to_exec.append("--password")
        command_to_exec.append(youtube_dl_password)
    # logger.info(command_to_exec)
    t_response, e_response = await run_shell_command(command_to_exec)
    # https://github.com/rg3/youtube-dl/issues/2630#issuecomment-38635239
    if e_response and "nonnumeric port" not in e_response:
        # logger.warn("Status : FAIL", exc.returncode, exc.output)
        error_message = e_response.replace(
            Translation.YTDL_ERROR_MESSAGE,
            ""
        )
        if Translation.ISOAYD_PREMIUM_VIDEOS in error_message:
            error_message += Translation.SET_CUSTOM_USERNAME_PASSWORD
        await update.reply_text(
            text=Translation.NO_VOID_FORMAT_FOUND.format(str(error_message)),
            quote=True,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )
        return False
    if t_response:
        # logger.info(t_response)
        x_reponse = t_response
        if "\n" in x_reponse:
            x_reponse, _ = x_reponse.split("\n")
        response_json = json.loads(x_reponse)
        save_ytdl_json_path = Config.DOWNLOAD_LOCATION + \
            "/" + str(update.from_user.id) + ".json"
        with open(save_ytdl_json_path, "w", encoding="utf8") as outfile:
            json.dump(response_json, outfile, ensure_ascii=False)
        # logger.info(response_json)
        inline_keyboard = []
        if "formats" in response_json:
            for formats in response_json["formats"]:
                format_id = formats["format_id"]
                format_string = formats["format"]
                format_ext = formats["ext"]
                approx_file_size = ""
                if "filesize" in formats:
                    approx_file_size = humanbytes(formats["filesize"])
                cb_string = "{}|{}|{}".format(
                    "video", format_id, format_ext)
                if not "audio only" in format_string:
                    ikeyboard = [
                        pyrogram.types.InlineKeyboardButton(
                            "[" + format_string +
                            "] (" + format_ext + " - " +
                            approx_file_size + ")",
                            callback_data=(cb_string).encode("UTF-8")
                        )
                    ]
                    inline_keyboard.append(ikeyboard)
            cb_string = "{}|{}|{}".format("audio", "5", "mp3")
            inline_keyboard.append([
                pyrogram.InlineKeyboardButton(
                    "MP3 " + "(" + "medium" + ")", callback_data=cb_string.encode("UTF-8"))
            ])
            cb_string = "{}|{}|{}".format("audio", "0", "mp3")
            inline_keyboard.append([
                pyrogram.InlineKeyboardButton(
                    "MP3 " + "(" + "best" + ")", callback_data=cb_string.encode("UTF-8"))
            ])
        else:
            format_id = response_json["format_id"]
            format_ext = response_json["ext"]
            cb_string = "{}|{}|{}".format(
                "file", format_id, format_ext)
            inline_keyboard.append([
                pyrogram.InlineKeyboardButton(
                    "unknown video format", callback_data=cb_string.encode("UTF-8"))
            ])
        reply_markup = pyrogram.InlineKeyboardMarkup(inline_keyboard)
        LOGGER.info(reply_markup)

        


        await update.reply_text(
            
            quote=True,
            text=Translation.FORMAT_SELECTION.format(""),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML,
            reply_to_message_id=update.id
        )


