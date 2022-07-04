
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
        duration = None
        if "duration" in response_json:
            duration = response_json["duration"]
           for listed in info.get("formats"):
        if listed.get("acodec") == "none":
            continue
        media_type = "Audio" if "audio" in listed.get("format") else "Video"
        
        if "audio" in listed.get("format"):
            first = str(listed.get("format_id")) + " - Audio"
        else:
            first = listed.get("format")
        
        #format_note = listed.get("format_note", "format")
        format_note = listed.get("ext")
        # SpEcHiDe/AnyDLBot/anydlbot/plugins/youtube_dl_echo.py#L112
        
        if listed.get("filesize"):
            filesize = humanbytes(listed.get("filesize"))
        elif listed.get("filesize_approx"):
            filesize = humanbytes(listed.get("filesize_approx"))
        else:
            filesize = "null"
        
        acodec = listed.get("acodec")
        av_codec = "empty"
        if listed.get("acodec") == "none" or listed.get("vcodec") == "none":
            av_codec = "none"


                cb_string_video = "{}|{}|{}".format(
                    "video", format_id, format_ext)
                cb_string_file = "{}|{}|{}".format(
                    "file", format_id, format_ext)
                if format_string and "audio only" not in format_string:
                    ikeyboard = [
                        InlineKeyboardButton(
                            f"🎬 {format_string}  {format_ext}  {approx_file_size} ",
                            callback_data=(cb_string_video).encode("UTF-8")
                        )
                    ]
                else:
                    # special weird case :\
                    ikeyboard = [
                        InlineKeyboardButton(
                            "🎬 [" +
                            "] ( " +
                            approx_file_size + " )",
                            callback_data=(cb_string_video).encode("UTF-8")
                        )
                    ]
                inline_keyboard.append(ikeyboard)
            if duration is not None:
                cb_string_64 = "{}|{}|{}".format("audio", "64k", "mp3")
                cb_string_128 = "{}|{}|{}".format("audio", "128k", "mp3")
                cb_string = "{}|{}|{}".format("audio", "320k", "mp3")
                inline_keyboard.append([
                    InlineKeyboardButton(
                        "MP3 " + "(" + "64 kbps" + ")",
                        callback_data=cb_string_64.encode("UTF-8")
                    ),
                    InlineKeyboardButton(
                        "MP3 " + "(" + "128 kbps" + ")",
                        callback_data=cb_string_128.encode("UTF-8")
                    )
                ])
                inline_keyboard.append([
                    InlineKeyboardButton(
                        "MP3 " + "(" + "320 kbps" + ")",
                        callback_data=cb_string.encode("UTF-8")
                    )
                ])
        else:
            format_id = response_json["format_id"]
            format_ext = response_json["ext"]
            cb_string_file = "{}|{}|{}".format(
                "file", format_id, format_ext)
            cb_string_video = "{}|{}|{}".format(
                "video", format_id, format_ext)
            inline_keyboard.append([
                InlineKeyboardButton(
                    "🎬",
                    callback_data=(cb_string_video).encode("UTF-8")
                )
            ])
            cb_string_file = "{}={}={}".format(
                "file", format_id, format_ext)
            cb_string_video = "{}={}={}".format(
                "video", format_id, format_ext)
            inline_keyboard.append([
                InlineKeyboardButton(
                    "🎬",
                    callback_data=(cb_string_video).encode("UTF-8")
                )
            ])
        reply_markup = InlineKeyboardMarkup(inline_keyboard)

        await update.reply_text(
            
           
            quote=True,
            text=Translation.FORMAT_SELECTION.format(
                Thumbnail
            ) + "\n" + Translation.SET_CUSTOM_USERNAME_PASSWORD,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    else:
        # fallback for nonnumeric port a.k.a seedbox.io
        inline_keyboard = []
        cb_string_file = "{}={}={}".format(
            "file", "LFO", "NONE")
        cb_string_video = "{}={}={}".format(
            "video", "OFL", "ENON")
        inline_keyboard.append([
            InlineKeyboardButton(
                "SVideo",
                callback_data=(cb_string_video).encode("UTF-8")
            )
        ])
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await update.reply_text(
            
            quote=True,
            text=Translation.FORMAT_SELECTION.format(""),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML,
            reply_to_message_id=update.id
        )

