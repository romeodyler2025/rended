import os
import asyncio
import random
import logging
from telethon import TelegramClient
from telethon.sessions import StringSession

# GitHub Secrets မှ Key များ
API_ID = int(os.environ['API_ID'])
API_HASH = os.environ['API_HASH']
SESSION_STRING = os.environ['SESSION_STRING']
SOURCE_CHANNEL = int(os.environ['SOURCE_CHANNEL'])
DEST_GROUP = int(os.environ['DEST_GROUP'])

# တစ်ခါ run ရင် ဘယ်နှပုဒ်တင်မလဲ?
POSTS_PER_RUN = 3 

logging.basicConfig(level=logging.INFO)
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

async def main():
    await client.start()
    print("🔍 Channel ထဲက Video များကို ရှာဖွေနေပါသည်...")
    
    # နောက်ဆုံး Post ၃၀၀၀ ထဲက Video/File ပါတာတွေကို စုမယ်
    video_posts = []
    async for message in client.iter_messages(SOURCE_CHANNEL, limit=3000):
        if message.video or message.file:
            video_posts.append(message)
    
    if not video_posts:
        print("❌ Video များ မတွေ့ပါ။")
        return

    # ရှိတဲ့အထဲကနေ ၃ ပုဒ် (သို့မဟုတ် ရှိသလောက်) ကို Random ရွေးမယ်
    count = min(len(video_posts), POSTS_PER_RUN)
    selected_posts = random.sample(video_posts, count)
    
    print(f"🎲 စုစုပေါင်း {len(video_posts)} ပုဒ်ထဲမှ {count} ပုဒ်ကို ရွေးလိုက်ပါပြီ...")

    # တစ်ပုဒ်ချင်းစီ Forward လုပ်မယ်
    for i, post in enumerate(selected_posts):
        try:
            await client.forward_messages(DEST_GROUP, post)
            print(f"✅ [{i+1}/{count}] Post ID {post.id} ကို ပို့ပြီးပါပြီ!")
            
            # နောက်တစ်ပုဒ်မတင်ခင် ၁ မိနစ် နားမယ် (Spam မဖြစ်အောင်)
            if i < count - 1:
                print("⏳ နောက်တစ်ပုဒ်အတွက် ၁ မိနစ် စောင့်နေသည်...")
                await asyncio.sleep(60) 
                
        except Exception as e:
            print(f"❌ Error: {e}")

    await client.disconnect()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
