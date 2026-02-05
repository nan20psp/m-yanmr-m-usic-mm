from pyrogram import Client
import re
import asyncio
from os import getenv
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()
import config
from dotenv import load_dotenv
from strings.__init__ import LOGGERS
from ..logging import LOGGER
# Database function များအား Import လုပ်ခြင်း
from maythusharmusic.utils.database import get_clones, save_clone

BOT_TOKEN = getenv("BOT_TOKEN", "")
MONGO_DB_URI = getenv("MONGO_DB_URI", "")
STRING_SESSION = getenv("STRING_SESSION", "")

assistants = []
assistantids = []

class Userbot(Client):
    def __init__(self):
        # Assistant Account များအား Initialize လုပ်ခြင်း
        self.one = Client(
            name="maythusharmusic1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
            no_updates=True,
            ipv6=False,
        )
        self.two = Client(
            name="maythusharmusic2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
            no_updates=True,
            ipv6=False,
        )
        self.three = Client(
            name="maythusharmusic3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
            no_updates=True,
            ipv6=False,
        )
        self.four = Client(
            name="maythusharmusic4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
            no_updates=True,
            ipv6=False,
        )
        self.five = Client(
            name="maythusharmusic5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
            no_updates=True,
            ipv6=False,
        )

    async def start(self):
        LOGGER(__name__).info(f"Starting Assistants...")

        # --- (၁) Assistant 1 စတင်ခြင်း ---
        if config.STRING1:
            await self.one.start()
            try:
                await self.one.join_chat("sasukevipmusicbotsupport")
                await self.one.join_chat("sasukemusicsupportchat")
            except: pass
            assistants.append(1)
            try:
                await self.one.send_message(config.LOGGER_ID, "ᴀssɪsᴛᴀɴᴛ sᴛᴀʀᴛᴇᴅ !")
            except Exception as e: print(f"{e}")
            self.one.id = self.one.me.id
            self.one.name = self.one.me.mention
            self.one.username = self.one.me.username
            assistantids.append(self.one.id)
            LOGGER(__name__).info(f"Assistant Started as {self.one.name}")

        # --- (၂) Assistant 2 စတင်ခြင်း ---
        if config.STRING2:
            await self.two.start()
            try:
                await self.two.join_chat("sasukevipmusicbotsupport")
                await self.two.join_chat("sasukemusicsupportchat")
            except: pass
            assistants.append(2)
            self.two.id = self.two.me.id
            assistantids.append(self.two.id)
            LOGGER(__name__).info(f"Assistant Two Started as {self.two.me.mention}")

        # --- (၃) Assistant 3 စတင်ခြင်း ---
        if config.STRING3:
            await self.three.start()
            assistants.append(3)
            self.three.id = self.three.me.id
            assistantids.append(self.three.id)
            LOGGER(__name__).info(f"Assistant Three Started as {self.three.me.mention}")

        # --- (၄) Assistant 4 စတင်ခြင်း ---
        if config.STRING4:
            await self.four.start()
            assistants.append(4)
            self.four.id = self.four.me.id
            assistantids.append(self.four.id)
            LOGGER(__name__).info(f"Assistant Four Started as {self.four.me.mention}")

        # --- (၅) Assistant 5 စတင်ခြင်း ---
        if config.STRING5:
            await self.five.start()
            assistants.append(5)
            self.five.id = self.five.me.id
            assistantids.append(self.five.id)
            LOGGER(__name__).info(f"Assistant Five Started as {self.five.me.mention}")

        # --- (၆) CLONE BOTS STARTUP & ID STORAGE ---
        # Database ထဲမှ Clone များအားလုံးကို တစ်ပါတည်း စတင်ပြီး ID သိမ်းဆည်းခြင်း
        LOGGER(__name__).info(f"Starting Clone Bots and saving IDs to Database...")
        clones = await get_clones() 
        
        for clone in clones:
            bot_token = clone["bot_token"]
            try:
                clone_client = Client(
                    name=f"clone_{bot_token[:10]}",
                    api_id=config.API_ID,
                    api_hash=config.API_HASH,
                    bot_token=bot_token,
                    no_updates=False, # Auto-leave အလုပ်လုပ်ရန် Update များ လိုအပ်ပါသည်
                )
                
                await clone_client.start()
                details = await clone_client.get_me()
                
                # Bot ID နှင့် Username ကို Database တွင် အလိုအလျောက် သွားသိမ်းခြင်း
                await save_clone(bot_token, details.id, details.username)
                
                LOGGER(__name__).info(f"✅ Clone @{details.username} ({details.id}) Started and ID Saved.")
                
            except Exception as e:
                LOGGER(__name__).error(f"❌ Failed to start clone bot: {e}")

    async def stop(self):
        LOGGER(__name__).info(f"Stopping Assistants...")
        try:
            if config.STRING1: await self.one.stop()
            if config.STRING2: await self.two.stop()
            if config.STRING3: await self.three.stop()
            if config.STRING4: await self.four.stop()
            if config.STRING5: await self.five.stop()
        except Exception as e:
            LOGGER(__name__).error(f"Error stopping assistants: {e}")
