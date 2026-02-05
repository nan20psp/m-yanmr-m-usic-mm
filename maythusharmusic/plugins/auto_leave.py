from pyrogram import filters, Client
from maythusharmusic.utils.database import is_clone_bot 

@Client.on_message(filters.new_chat_members & filters.group)
async def auto_leave_logic(client, message):
    for member in message.new_chat_members:
        if member.is_bot:
            # အခုထည့်လိုက်တဲ့ function နဲ့ စစ်မယ်
            if await is_clone_bot(member.id):
                
                # ဝင်လာတဲ့ကောင်က ကိုယ်မဟုတ်ဘဲ တခြား clone ဖြစ်နေရင်...
                if member.id != client.me.id:
                    await message.reply_text(f"❗ **Conflict detected!**\n@{member.username} ဝင်လာသောကြောင့် ကျွန်တော် @{client.me.username} ထွက်ခွာပါမည်။")
                    await client.leave_chat(message.chat.id)
