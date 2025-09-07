import os
from pyrogram import Client, filters
from pyrogram.types import Message
from keep_alive import keep_alive

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")
OWNER_ID = int(os.getenv("OWNER_ID"))

app = Client(session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

sources = set()
target_chat = None

@app.on_message(filters.user(OWNER_ID) & filters.command("settarget"))
async def set_target(_, message: Message):
    global target_chat
    if len(message.command) < 2:
        return await message.reply("Usage: /settarget <chat_id>")
    target_chat = int(message.command[1])
    await message.reply(f"✅ Target set to {target_chat}")

@app.on_message(filters.user(OWNER_ID) & filters.command("addsource"))
async def add_source(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: /addsource <chat_id>")
    chat_id = int(message.command[1])
    sources.add(chat_id)
    await message.reply(f"✅ Source added: {chat_id}")

@app.on_message(filters.user(OWNER_ID) & filters.command("status"))
async def status(_, message: Message):
    await message.reply(f"📌 Target: {target_chat}\n📌 Sources: {list(sources)}")

@app.on_message(filters.chat(list(sources)))
async def forward_messages(_, message: Message):
    if not target_chat:
        return
    try:
        if message.text:
            await app.send_message(target_chat, message.text)
        elif message.photo:
            await app.send_photo(target_chat, message.photo.file_id, caption=message.caption)
        elif message.video:
            await app.send_video(target_chat, message.video.file_id, caption=message.caption)
    except Exception as e:
        print(f"Forward failed: {e}")

@app.on_message(filters.user(OWNER_ID) & filters.command("help"))
async def help_cmd(_, message: Message):
    await message.reply(
        "**🤖 Auto Forward Bot Commands**\n\n"
        "/settarget <chat_id> – Set destination chat\n"
        "/addsource <chat_id> – Add source channel\n"
        "/status – Show sources and target\n"
        "/help – Show this help"
    )

if __name__ == "__main__":
    keep_alive()
    app.run()
