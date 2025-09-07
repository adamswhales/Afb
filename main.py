import os
from pyrogram import Client, filters
from keep_alive import keep_alive

# Load environment variables from Render
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")
SOURCE_CHAT = int(os.getenv("SOURCE_CHAT"))   # e.g. -100123456789
TARGET_CHAT = int(os.getenv("TARGET_CHAT"))   # e.g. -100987654321

# Initialize Pyrogram Client
app = Client(
    name="autoforward",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# Auto-forward handler (without "forwarded from" header)
@app.on_message(filters.chat(SOURCE_CHAT))
async def forward(client, message):
    try:
        await message.copy(TARGET_CHAT, reply_markup=None)   # copies cleanly, no buttons
    except Exception as e:
        print(f"❌ Error forwarding: {e}")

if __name__ == "__main__":
    keep_alive()  # start Flask keep-alive server
    print("🚀 Auto Forward Bot is running...")
    app.run()
