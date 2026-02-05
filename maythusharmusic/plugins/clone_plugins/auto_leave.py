from pyrogram import filters, Client
from pyrogram.types import Message
from maythusharmusic import app
# သင့်ရဲ့ database file ထဲက clone ဟုတ်မဟုတ်စစ်တဲ့ function ကို import လုပ်ပါ
from maythusharmusic.utils.database import is_clone_bot 

@Client.on_message(filters.new_chat_members & filters.group)
async def auto_leave_redundant_clone(client: Client, message: Message):
    # ဝင်လာတဲ့ member တွေထဲမှာ bot ပါသလား စစ်မယ်
    for member in message.new_chat_members:
        if member.is_bot:
            # ဝင်လာတဲ့ bot က clone ဟုတ်မဟုတ် database မှာ စစ်မယ်
            if await is_clone_bot(member.id):
                
                # အကယ်၍ ဝင်လာတဲ့ bot က ကိုယ့် ID မဟုတ်ဘူးဆိုရင် (ဆိုလိုတာက နောက်တစ်ကောင် ဝင်လာတာ)
                if member.id != client.me.id:
                    try:
                        # User တွေသိအောင် message အရင်ပို့မယ်
                        await message.reply_text(
                            f"🤖 **New Clone Bot Detected:** @{member.username} ဝင်လာပါပြီ။\n"
                            f"တစ်ခုထက်ပိုမရှိစေရန် ကျွန်တော် @{client.me.username} က ဤ Group မှ ထွက်ခွာပါမည်။"
                        )
                        # Group ထဲက ထွက်မယ်
                        await client.leave_chat(message.chat.id)
                    except Exception as e:
                        print(f"Error while leaving chat: {e}")
