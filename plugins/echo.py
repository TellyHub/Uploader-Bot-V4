


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | @Tellybots | @PlanetBots

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
import requests, urllib.parse, filetype, os, time, shutil, tldextract, asyncio, json, math
from PIL import Image
from plugins.config import Config
import time
from plugins.script import Translation
logging.getLogger("pyrogram").setLevel(logging.WARNING)
from pyrogram import filters
from pyrogram import Client, enums
from plugins.functions.forcesub import handle_force_subscribe
from plugins.functions.display_progress import humanbytes
from plugins.functions.help_uploadbot import DownLoadFile
from plugins.functions.display_progress import progress_for_pyrogram, humanbytes, TimeFormatter
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from plugins.functions.ran_text import random_char
from plugins.database.add import add_user_to_database
from pyrogram.types import Thumbnail

@Client.on_message(filters.private & filters.regex(pattern=".*http.*"))
async def echo(bot, update):

            logger.info(update.from_user)
            u = update.text
            youtube_dl_username = None
            youtube_dl_password = None
            file_name = None
            url = None
            if "|" in u:
               ul_part = u.strip(" ")
               ul_parts = ul_part.split("|")
               u = ul_parts[0]
 

            if "|" in update.text:
                file_name = ul_parts[1]

                if url is not None:
                    url = url.strip()
                if file_name is not None:
                    file_name = file_name.strip()
                # https://stackoverflow.com/a/761825/4723940
                if youtube_dl_username is not None:
                    youtube_dl_username = youtube_dl_username.strip()
                if youtube_dl_password is not None:
                    youtube_dl_password = youtube_dl_password.strip()
                logger.info(url)
                logger.info(file_name)
             
 
            if Config.HTTP_PROXY != "":
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
            process = await asyncio.create_subprocess_exec(
                *command_to_exec,
                # stdout must a pipe to be accessible as process.stdout
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            # Wait for the subprocess to finish
            stdout, stderr = await process.communicate()
            e_response = stderr.decode().strip()
            # logger.info(e_response)
            t_response = stdout.decode().strip()
            # logger.info(t_response)
            # https://github.com/rg3/youtube-dl/issues/2630#issuecomment-38635239
            if e_response and "nonnumeric port" not in e_response:
                # logger.warn("Status : FAIL", exc.returncode, exc.output)
                error_message = e_response.replace("please report this issue on https://yt-dl.org/bug . Make sure you are using the latest version; see  https://yt-dl.org/update  on how to update. Be sure to call youtube-dl with the --verbose flag and include its complete output.", "")
                if "This video is only available for registered users." in error_message:
                    error_message += Translation.SET_CUSTOM_USERNAME_PASSWORD
                await bot.send_message(
                    chat_id=update.chat.id,
                    text=Translation.NO_VOID_FORMAT_FOUND.format(str(error_message)),
                    reply_to_message_id=update.message_id,
                    parse_mode="html",
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
                duration = None
                if "duration" in response_json:
                    duration = response_json["duration"]
                if "formats" in response_json:
                    for formats in response_json["formats"]:
                        format_id = formats.get("format_id")
                        format_string = formats.get("format_note")
                        if format_string is None:
                            format_string = formats.get("format")
                        format_ext = formats.get("ext")
                        approx_file_size = ""
                        if "filesize" in formats:
                            approx_file_size = humanbytes(formats["filesize"])
                        cb_string_video = "{}|{}|{}".format(
                            "video", format_id, format_ext)
                        cb_string_file = "{}|{}|{}".format(
                            "file", format_id, format_ext)
                        cb_string_td = "{}|{}|{}".format(
                            "gdrive", format_id, format_ext)
                        if format_string is not None and not "audio only" in format_string:
                            ikeyboard = [
                                pyrogram.InlineKeyboardButton(
                                    "🎞 " + format_string + " video " + approx_file_size + " ",
                                    callback_data=(cb_string_video).encode("UTF-8")
                                ),
                                pyrogram.InlineKeyboardButton(
                                    "📥 GDrive ",
                                    callback_data=(cb_string_td).encode("UTF-8")
                                )
                            ]
                            """if duration is not None:
                                cb_string_video_message = "{}|{}|{}".format(
                                    "vm", format_id, format_ext)
                                ikeyboard.append(
                                    pyrogram.InlineKeyboardButton(
                                        "VM",
                                        callback_data=(
                                            cb_string_video_message).encode("UTF-8")
                                    )
                                )"""
                        else:
                            # special weird case :\
                            ikeyboard = [
                                pyrogram.InlineKeyboardButton(
                                    "🎞 - Video",
                                    callback_data="ferror"
                                ),

                                pyrogram.InlineKeyboardButton(
                                    "📥 - GDrive",
                                    callback_data="ferror"
                                )
                            ]
                        inline_keyboard.append(ikeyboard)

                else:
                    format_id = response_json["format_id"]
                    format_ext = response_json["ext"]
                    cb_string_file = "{}|{}|{}".format(
                        "file", format_id, format_ext)
                    cb_string_video = "{}|{}|{}".format(
                        "video", format_id, format_ext)
                    inline_keyboard.append([
                        pyrogram.InlineKeyboardButton(
                            "SVideo",
                            callback_data=(cb_string_video).encode("UTF-8")
                        )
                    ])
                    cb_string_file = "{}={}={}".format(
                        "file", format_id, format_ext)
                    cb_string_video = "{}={}={}".format(
                        "video", format_id, format_ext)
                    inline_keyboard.append([
                        pyrogram.InlineKeyboardButton(
                            "video",
                            callback_data=(cb_string_video).encode("UTF-8")
                        )
                    ])
                reply_markup = pyrogram.InlineKeyboardMarkup(inline_keyboard)

                await bot.send_message(
                    chat_id=update.chat.id,
                    text=Translation.FORMAT_SELECTION + "\n" + Translation.SET_CUSTOM_USERNAME_PASSWORD,
                    reply_markup=reply_markup,
                    parse_mode="html",
                    reply_to_message_id=update.message_id
                )
            else:
                # fallback for nonnumeric port a.k.a seedbox.io
                inline_keyboard = []
                cb_string_file = "{}={}={}".format(
                    "file", "LFO", "NONE")
                cb_string_video = "{}={}={}".format(
                    "video", "OFL", "ENON")
                inline_keyboard.append([
                    pyrogram.InlineKeyboardButton(
                        "Video",
                        callback_data=(cb_string_video).encode("UTF-8")
                    )
                ])
                reply_markup = pyrogram.InlineKeyboardMarkup(inline_keyboard)
                await bot.send_message(
                    chat_id=update.chat.id,
                    text=Translation.FORMAT_SELECTION.format(""),
                    reply_markup=reply_markup,
                    parse_mode="html",
                    reply_to_message_id=update.message_id
                )


