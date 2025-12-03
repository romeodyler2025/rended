import os
import asyncio
import random
import logging
from telethon import TelegramClient
from telethon.sessions import StringSession

# Secrets များ
API_ID = int(os.environ['API_ID'])
API_HASH = os.environ['API_HASH']
SESSION_STRING = os.environ['SESSION_STRING']
SOURCE_CHANNEL = int(os.environ['SOURCE_CHANNEL'])
DEST_GROUP = int(os.environ['DEST_GROUP'])

# တစ်ခါ Run ရင် ၃ ပုဒ် တင်မယ်
POSTS_PER_RUN = 3

logging.basicConfig(level=logging.INFO)
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

async def main():
    await client.start()
    print("🔍 Channel ထဲက Video များကို ရှာဖွေနေပါသည်...")
    
    video_posts = []
    
    # နောက်ဆုံး Post ၃၀၀၀ ကို စစ်မယ်
    async for message in client.iter_messages(SOURCE_CHANNEL, limit=3000):
        is_video = False
        
        # ၁။ ရိုးရိုး Video ဖြစ်လျှင်
        if message.video:
            is_video = True
        
        # ၂။ File (Document) အနေနဲ့တင်ထားသော Video ဖြစ်လျှင် (mime_type စစ်မည်)
        elif message.document and hasattr(message.document, 'mime_type'):
            if message.document.mime_type.startswith('video/'):
                is_video = True
        
        # Video စစ်စစ်ဖြစ်မှ စာရင်းသွင်းမည် (ဓာတ်ပုံများ မပါတော့ပါ)
        if is_video:
            video_posts.append(message)
    
    if not video_posts:
        print("❌ Video များ မတွေ့ပါ။")
        return

    # ရှိတဲ့အထဲကနေ ၃ ပုဒ်ကို Random ရွေးမယ်
    count = min(len(video_posts), POSTS_PER_RUN)
    selected_posts = random.sample(video_posts, count)
    
    print(f"🎲 စုစုပေါင်း Video {len(video_posts)} ပုဒ်ထဲမှ {count} ပုဒ်ကို ရွေးလိုက်ပါပြီ...")

    for i, post in enumerate(selected_posts):
        try:
            # Forward လုပ်လိုက်တာနဲ့ Review စာ (Caption) ပါ အလိုလို ပါလာပါလိမ့်မယ်
            await client.forward_messages(DEST_GROUP, post)
            print(f"✅ [{i+1}/{count}] Video ID {post.id} ကို ပို့ပြီးပါပြီ!")
            
            # နောက်တစ်ပုဒ်မတင်ခင် ၁ မိနစ် နားမယ်
            if i < count - 1:
                print("⏳ နောက်တစ်ပုဒ်အတွက် ၁ မိနစ် စောင့်နေသည်...")
                await asyncio.sleep(60) 
                
        except Exception as e:
            print(f"❌ Error: {e}")

    await client.disconnect()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
