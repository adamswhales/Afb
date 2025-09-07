from flask import Flask
import threading, time, requests, os

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run():
    app.run(host="0.0.0.0", port=8080)

def ping_self():
    url = os.getenv("RENDER_URL")  # e.g. https://your-app.onrender.com
    while True:
        try:
            if url:
                requests.get(url, timeout=10)
                print("🔄 Self-ping sent")
        except Exception as e:
            print(f"Ping failed: {e}")
        time.sleep(300)  # every 5 minutes

def keep_alive():
    threading.Thread(target=run, daemon=True).start()
    threading.Thread(target=ping_self, daemon=True).start()
