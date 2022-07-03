
# (c) Shrimadhav U K | @Tellybots



import asyncio
import json
import math
import os
import shutil
import time
from datetime import datetime, timedelta
from pyrogram import enums 
from plugins.config import Config
from plugins.script import Translation
from plugins.thumbnail import *
from plugins.__init__ import *
from pyrogram.types import InputMediaPhoto
from plugins.functions.display_progress import *
from plugins.database.database import db
from PIL import Image





async def youtube_dl_call_back(bot, update):
    cb_data = update.data
    # youtube_dl extractors
    tg_send_type, youtube_dl_format, youtube_dl_ext = cb_data.split("|")
    
    save_ytdl_json_path = DOWNLOAD_LOCATION + \
        "/" + str(update.from_user.id) + ".json"
    try:
        with open(save_ytdl_json_path, "r", encoding="utf8") as f:
            response_json = json.load(f)
    except FileNotFoundError:
        await update.message.delete()
        return False

    youtube_dl_url, \
        custom_file_name, \
        youtube_dl_username, \
        youtube_dl_password = get_link(
            update.message.reply_to_message
        )
    if not custom_file_name:
        custom_file_name = str(response_json.get("title")) + \
            "_" + youtube_dl_format + "." + youtube_dl_ext
    await update.message.edit_caption(
        caption=Translation.DOWNLOAD_START,

        parse_mode=enums.ParseMode.HTML
    )
    description = Translation.CUSTOM_CAPTION_UL_FILE
    if "fulltitle" in response_json:
        description = response_json["fulltitle"][0:1021]
        # escape Markdown and special characters
    tmp_directory_for_each_user = os.path.join(
        DOWNLOAD_LOCATION,
        str(update.from_user.id)
    )
    if not os.path.isdir(tmp_directory_for_each_user):
        os.makedirs(tmp_directory_for_each_user)
    download_directory = os.path.join(
        tmp_directory_for_each_user,
        custom_file_name
    )
    command_to_exec = []
    if tg_send_type == "audio":
        command_to_exec = [
            "yt-dlp",
            "-c",
            "--max-filesize", str(TG_MAX_FILE_SIZE),
            "--prefer-ffmpeg",
            "--extract-audio",
            "--audio-format", youtube_dl_ext,
            "--audio-quality", youtube_dl_format,
            youtube_dl_url,
            "-o", download_directory
        ]
    else:
        minus_f_format = youtube_dl_format
        if "youtu" in youtube_dl_url:
            minus_f_format = youtube_dl_format + "+bestaudio"
        command_to_exec = [
            "yt-dlp",
            "-c",
            "--max-filesize", str(TG_MAX_FILE_SIZE),
            "--embed-subs",
            "-f", minus_f_format,
            "--hls-prefer-ffmpeg", youtube_dl_url,
            "-o", download_directory
        ]
    if HTTP_PROXY is not None:
        command_to_exec.append("--proxy")
        command_to_exec.append(HTTP_PROXY)
    if youtube_dl_username is not None:
        command_to_exec.append("--username")
        command_to_exec.append(youtube_dl_username)
    if youtube_dl_password is not None:
        command_to_exec.append("--password")
        command_to_exec.append(youtube_dl_password)
    command_to_exec.append("--no-warnings")
    # command_to_exec.append("--quiet")
    command_to_exec.append("--restrict-filenames")
    LOGGER.info(command_to_exec)
    start = datetime.now()
    t_response, e_response = await run_shell_command(command_to_exec)
    LOGGER.info(e_response)
    LOGGER.info(t_response)
    if e_response and Translation.YTDL_ERROR_MESSAGE in e_response:
        error_message = e_response.replace(
            Translation.YTDL_ERROR_MESSAGE,
            ""
        )
        await update.message.edit_caption(
            caption=error_message,

            parse_mode=enums.ParseMode.HTML
        )
        return False
    if t_response:
        # LOGGER.info(t_response)
        os.remove(save_ytdl_json_path)
        end_one = datetime.now()
        time_taken_for_download = (end_one - start).seconds
        file_size = TG_MAX_FILE_SIZE + 1
        download_directory_dirname = os.path.dirname(download_directory)
        download_directory_contents = os.listdir(download_directory_dirname)
        for download_directory_c in download_directory_contents:
            current_file_name = os.path.join(
                download_directory_dirname,
                download_directory_c
            )
            file_size = os.stat(current_file_name).st_size

            if file_size > TG_MAX_FILE_SIZE:
                await update.message.edit_caption(
                    caption=Translation.RCHD_TG_API_LIMIT.format(
                        time_taken_for_download,
                        humanbytes(file_size)
                    )
                    
                )

            else:
                is_w_f = False
                '''images = await generate_screen_shots(
                    current_file_name,
                    tmp_directory_for_each_user,
                    is_w_f,
                    "",
                    300,
                    9
                )
                '''LOGGER.info(images)
                await update.message.edit_caption(
                    caption=Translation.UPLOAD_START,

        
                    parse_mode=enums.ParseMode.HTML
                )
                start_time = time.time()
                if (await db.get_upload_as_doc(update.from_user.id)) is False:
                    thumbnail = await Gthumb01(bot, update)
                    await update.message.reply_document(
                    #chat_id=update.message.chat.id,
                        document=download_directory,
                        thumb=thumbnail,
                        caption=description,
                        parse_mode=enums.ParseMode.HTML,
                    #reply_to_message_id=update.id,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            Translation.UPLOAD_START,
                            update.message,
                            start_time
                        )
                    )
                else:
                     width, height, duration = await Mdata01(download_directory)
                     thumb_image_path = await Gthumb02(bot, update, duration, download_directory)
                     await update.message.reply_video(
                    #chat_id=update.message.chat.id,
                        video=download_directory,
                        caption=description,
                        duration=duration,
                        width=width,
                        height=height,
                        supports_streaming=True,
                        parse_mode=enums.ParseMode.HTML,
                        thumb=thumb_image_path,
                    #reply_to_message_id=update.id,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            Translation.UPLOAD_START,
                            update.message,
                            start_time
                        )
                    )
                if tg_send_type == "audio":
                    duration = await Mdata03(download_directory)
                    thumbnail = await Gthumb01(bot, update)
                    await update.message.reply_audio(
                    #chat_id=update.message.chat.id,
                        audio=download_directory,
                        caption=description,
                        parse_mode=enums.ParseMode.HTML,
                        duration=duration,
                        thumb=thumbnail,
                    #reply_to_message_id=update.id,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            Translation.UPLOAD_START,
                            update.message,
                            start_time
                        )
                    )
                elif tg_send_type == "vm":
                    width, duration = await Mdata02(download_directory)
                    thumbnail = await Gthumb02(bot, update, duration, download_directory)
                    await update.message.reply_video_note(
                    #chat_id=update.message.chat.id,
                        video_note=download_directory,
                        duration=duration,
                        length=width,
                        thumb=thumbnail,
                    #reply_to_message_id=update.id,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            Translation.UPLOAD_START,
                            update.message,
                            start_time
                        )
                    )
            
                
                else:
                    LOGGER.info("Did this happen? :\\")
                end_two = datetime.now()
                time_taken_for_upload = (end_two - end_one).seconds
                #
                media_album_p = []
                if images is not None:
                    i = 0
                    caption = "© @AnyDLBot"
                    for image in images:
                        if os.path.exists(image):
                            if i == 0:
                                media_album_p.append(
                                    InputMediaPhoto(
                                        media=image,
                                        caption=caption,
                                        parse_mode=enums.ParseMode.HTML
                                    )
                                )
                            else:
                                media_album_p.append(
                                    InputMediaPhoto(
                                        media=image
                                    )
                                )
                            i = i + 1
                await update.message.reply_media_group(
                    media=media_album_p,
                    parse_mode=enums.ParseMode.HTML,
                    disable_notification=True
                )
            #
            shutil.rmtree(
                tmp_directory_for_each_user,
                ignore_errors=True
            )
            os.remove(thumb_image_path)

            await update.message.delete()

