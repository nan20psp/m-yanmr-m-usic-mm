import asyncio
from pyrogram import Client, errors, filters
from pyrogram.enums import ChatMemberStatus, ParseMode

import config
from ..logging import LOGGER

class pisces(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot...")
        super().__init__(
            name="maythusharmusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        # --- (၁) AUTO-LEAVE REDUNDANT BOTS (Main/Clone မခွဲဘဲ တစ်ကောင်ပဲ လက်ခံခြင်း) ---
        # Group ထဲကို Member အသစ်ဝင်လာတိုင်း စစ်ဆေးမည့် Handler ဖြစ်သည်
        @self.on_message(filters.group & filters.new_chat_members)
        async def auto_leave_handler(client, message):
            for member in message.new_chat_members:
                if member.is_bot:
                    try:
                        from maythusharmusic.utils.database import is_clone_bot
                        
                        # ဝင်လာသူသည် Main Bot သို့မဟုတ် Clone Bot ဟုတ်မဟုတ် စစ်ဆေးသည်
                        if member.id == config.BOT_ID or await is_clone_bot(member.id):
                            
                            # အကယ်၍ ဝင်လာသော Bot သည် ကိုယ့် ID မဟုတ်ပါက (တခြားတစ်ကောင် ဝင်လာခြင်း)
                            if member.id != client.me.id:
                                await message.reply_text(
                                    f"🤖 **Conflict Detected:** @{member.username} ဝင်လာသောကြောင့် "
                                    f"ကျွန်တော် @{client.me.username} သည် ဤ Group မှ ထွက်ခွာပါမည်။"
                                )
                                # အဟောင်းရှိနေသော Bot က အလိုအလျောက် ထွက်ခွာသွားခြင်း
                                await client.leave_chat(message.chat.id)
                                break 
                    except Exception as e:
                        LOGGER(__name__).error(f"Auto-Leave Error: {e}")

        # --- (၂) GLOBAL BOT CONFLICT HANDLER (သီချင်းဖွင့်ရာတွင် တစ်ကောင်တည်းသာ အလုပ်လုပ်ရန်) ---
        # Text Commands များကိုသာ စစ်ထုတ်ပြီး group=-1 ဖြင့် လမ်းဖြတ်စစ်ဆေးသည်
        @self.on_message(filters.group & ~filters.service, group=-1)
        async def bot_conflict_handler(client, message):
            if not message.text:
                return 

            # Command ဖြစ်မှသာ စစ်ဆေးမည် (Fixed Syntax)
            if message.text.startswith(("/", "")):
                try:
                    from maythusharmusic.utils.database import is_active_bot_auto
                    
                    # ဒီ Group မှာ ငါက Active Bot ဟုတ်-မဟုတ် စစ်ဆေးသည်
                    # client, chat_id, bot_id (၃) ခုလုံးကို ပို့ပေးရပါမည်
                    if not await is_active_bot_auto(client, message.chat.id, client.me.id):
                        # ငါက Active မဟုတ်ရင် ဒီ Message ကို Plugin တွေဆီ ဆက်မလွှတ်တော့ပါ
                        message.stop_propagation()
                except Exception as e:
                    LOGGER(__name__).error(f"Conflict Handler Error: {e}")

        # --- Startup Log Messages ---
        try:
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b><u>\n\nɪᴅ : <code>{self.id}</code>\nɴᴀᴍᴇ : {self.name}\nᴜsᴇʀɴᴀᴍᴇ : @{self.username}",
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error("Log group access failed. Check your config.LOGGER_ID.")
        except Exception as ex:
            LOGGER(__name__).error(f"Startup error: {ex}")

        LOGGER(__name__).info(f"Music Bot Started as {self.name}")

    async def stop(self):
        await super().stop()

    # --- (၃) CLEAN MODE & MESSAGE OVERRIDES ---
    # စာပို့တိုင်း Clean Mode ထဲ အလိုအလျောက်ထည့်မည့် Function ဖြစ်သည်
    async def add_to_clean(self, chat_id, message_id):
        try:
            if chat_id != config.LOGGER_ID:
                from maythusharmusic.utils.database import add_clean_message
                await add_clean_message(chat_id, message_id)
        except:
            pass

    async def send_message(self, chat_id, text, *args, **kwargs):
        message = await super().send_message(chat_id, text, *args, **kwargs)
        await self.add_to_clean(chat_id, message.id)
        return message

    async def send_photo(self, chat_id, photo, *args, **kwargs):
        message = await super().send_photo(chat_id, photo, *args, **kwargs)
        await self.add_to_clean(chat_id, message.id)
        return message

    async def send_video(self, chat_id, video, *args, **kwargs):
        message = await super().send_video(chat_id, video, *args, **kwargs)
        await self.add_to_clean(chat_id, message.id)
        return message
