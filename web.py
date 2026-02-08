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
    filename = file.filename
    file.save(filename)

    bot.send_document(chat_id=ADMIN_ID, document=open(filename, 'rb'))
    os.remove(filename)

    return "Uploaded to Telegram ✅"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
