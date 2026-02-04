from functools import wraps
from pyrogram.types import Message, CallbackQuery
from maythusharmusic.utils.database import is_active_bot_auto

def ActiveBotAuto(func):
    @wraps(func)
    async def wrapper(client, update, *args, **kwargs):
        # Message သို့မဟုတ် CallbackQuery ဖြစ်နေလား စစ်မယ်
        if isinstance(update, Message):
            chat_id = update.chat.id
        elif isinstance(update, CallbackQuery):
            chat_id = update.message.chat.id
        else:
            return await func(client, update, *args, **kwargs)

        bot_id = client.me.id
        
        # Database ကနေ ဒီ Bot က Active ဖြစ်-မဖြစ် စစ်မယ်
        if not await is_active_bot_auto(chat_id, bot_id):
            # Active မဟုတ်ရင် ဘာမှမလုပ်ဘဲ ပြန်ထွက်သွားမယ် (Silent Return)
            return 
            
        return await func(client, update, *args, **kwargs)
    return wrapper
