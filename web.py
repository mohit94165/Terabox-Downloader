import os
from flask import Flask, request, render_template
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 6728678197

bot = Bot(token=BOT_TOKEN)
app = Flask(__name__)

@app.route("/")
def index():
    link = request.args.get("link", "")
    return render_template("index.html", link=link)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['file']
    file.save(file.filename)
    bot.send_document(chat_id=ADMIN_ID, document=open(file.filename, 'rb'))
    os.remove(file.filename)
    return "Uploaded to Telegram ✅"

app.run(host="0.0.0.0", port=8080)
