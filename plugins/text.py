from pyrogram.types import Message

from plugins.functions.ikb import ikb
from plugins.config import Config


class Constants:
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



    progress_msg = """
Percentage : {0}%
Done ✅: {1}
Total 🌀: {2}
Speed 🚀: {3}/s
ETA 🕰: {4}
"""
