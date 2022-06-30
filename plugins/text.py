from pyrogram.types import Message

from plugins.functions.ikb import ikb
from plugins.config import Config


class Text:
    @staticmethod
    async def join_channel_msg(m: Message):
        join_channel = Config.UPDATE_CHANNEL.replace("@", "")
        return await m.reply_text(
            "You have reached your limit of usage."
            "\nPlease wait for some time before using this bot again."
            f"\nIf you want to increase the usage limit, join {Config.UPDATE_CHANNEL}",
            reply_markup=ikb(
                [[("Join Channel", f"https://t.me/{join_channel}", "url")]],
            ),
        )

    @staticmethod
    def ban_kb(user_id: int):
        return (
            ikb(
                [[("Ban User", f"ban_{user_id}")]],
            )
            if user_id != Config.OWNER_ID
            else None
        )

    start_kb = [
        [
            ("How to use", "help_callback.start"),
            ("Help & Support", f"https://t.me/{Vars.SUPPORT_GROUP}", "url"),
        ],
    ]




    start_msg = """
👋 Hᴇʏ {} ♡

I ᴀᴍ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴏsᴛ ᴘᴏᴡᴇʀғᴜʟ ᴜʀʟ ᴜᴘʟᴏᴀᴅᴇʀ ʙᴏᴛ

Usᴇ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴛᴏ ᴋɴᴏᴡ ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ

ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : [Tᴇʟʟʏʙᴏᴛs](t.me//tellybots)
"""


    help_msg = """
ʟɪɴᴋ ᴛᴏ ᴍᴇᴅɪᴀ ᴏʀ ғɪʟᴇ

➠ sᴇɴᴅ ᴀ ʟɪɴᴋ ғᴏʀ ᴜᴘʟᴏᴀᴅ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ ғɪʟᴇ ᴏʀ ᴍᴇᴅɪᴀ.

sᴇᴛ ᴛʜᴜᴍʙɴᴀɪʟ

➠ sᴇɴᴅ ᴀ ᴘʜᴏᴛᴏ ᴛᴏ ᴍᴀᴋᴇ ɪᴛ ᴀs ᴘᴇʀᴍᴀɴᴇɴᴛ ᴛʜᴜᴍʙɴᴀɪʟ.

ᴅᴇʟᴇᴛɪɴɢ ᴛʜᴜᴍʙɴᴀɪʟ

➠ sᴇɴᴅ /delthumb ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴛʜᴜᴍʙɴᴀɪʟ.

sᴇᴛᴛɪɴɢs

➠ ᴄᴏɴғɪɢᴜʀᴇ ᴍʏ sᴇᴛᴛɪɴɢs ᴛᴏ ᴄʜᴀɴɢᴇ ᴜᴘʟᴏᴀᴅ ᴍᴏᴅᴇ

sʜᴏᴡ ᴛʜᴜᴍʙɴᴀɪʟ

➠ sᴇɴᴅ /showthumb ᴛᴏ ᴠɪᴇᴡ ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ.

ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : [Tᴇʟʟʏʙᴏᴛs](https://telegram.me/TellyBots)
 
"""
    about_msg = """
**Mʏ ɴᴀᴍᴇ** : [ᴜᴘʟᴏᴀᴅᴇʀ ʙᴏᴛ](http://t.me/TellyUploaderRobot)

**Cʜᴀɴɴᴇʟ** : [Tᴇʟʟʏʙᴏᴛs](https://t.me/TellyBots)

**Vᴇʀꜱɪᴏɴ** : [2.0 ʙᴇᴛᴀ](https://t.me/TellyUploaderRobot)

**Sᴏᴜʀᴄᴇ** : [ᴄʟɪᴄᴋ ʜᴇʀᴇ](https://t.me/tellybots_digital)

**Sᴇʀᴠᴇʀ** : [ʜᴇʀᴏᴋᴜ](https://heroku.com/)

**Lᴀɴɢᴜᴀɢᴇ :** [Pʏᴛʜᴏɴ 3.10.2](https://www.python.org/)

**Fʀᴀᴍᴇᴡᴏʀᴋ :** [ᴘʏʀᴏɢᴀᴍ 2.0.30](https://docs.pyrogram.org/)

**Dᴇᴠᴇʟᴏᴘᴇʀ :** [Tᴇʟʟʏʙᴏᴛs](https://t.me/tellybots)

**ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ :** [NᴀʏsᴀBᴏᴛs](https://t.me/NaysaBots)

"""


    PROGRESS = """
🔰 Sᴘᴇᴇᴅ : {3}/s\n\n
🌀 Dᴏɴᴇ : {1}\n\n
🎥 Tᴏᴛᴀʟ sɪᴢᴇ  : {2}\n\n
⏳ Tɪᴍᴇ ʟᴇғᴛ : {4}\n\n
"""
    INFO_TEXT = """
 💫 Telegram Info

 🤹 First Name : <b>{}</b>

 🚴‍♂️ Second Name : <b>{}</b>

 🧑🏻‍🎓 Username : <b>@{}</b>

 🆔 Telegram Id : <code>{}</code>

 📇 Profile Link : <b>{}</b>

 📡 Dc : <b>{}</b>

 📑 Language : <b>{}</b>

 👲 Status : <b>{}</b>
"""

    st_bt = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🗜️ sᴇᴛᴛɪɴɢs', callback_data='OpenSettings')
        ],[
        InlineKeyboardButton('❔ ʜᴇʟᴘ', callback_data='help'),
        InlineKeyboardButton('👨‍🚒 ᴀʙᴏᴜᴛ', callback_data='about')
        ],[
        InlineKeyboardButton('♨️ ᴄʟᴏsᴇ', callback_data='close')
        ]]
    )
    hp_bt = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🏡 ʜᴏᴍᴇ', callback_data='home'),
        InlineKeyboardButton('👨‍🚒 ᴀʙᴏᴜᴛ', callback_data='about')
        ],[
        InlineKeyboardButton('♨️ ᴄʟᴏsᴇ', callback_data='close')
        ]]
    )
    ab_bt = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🏡 ʜᴏᴍᴇ', callback_data='home'),
        InlineKeyboardButton('❔ ʜᴇʟᴘ', callback_data='help')
        ],[
        InlineKeyboardButton('♨️ ᴄʟᴏsᴇ', callback_data='close')
        ]]
    )
    BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('♨️ ᴄʟᴏsᴇ', callback_data='close')
        ]]
    )


