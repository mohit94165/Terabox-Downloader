import os
from flask import Flask, request, render_template
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 6728678197

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

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    with open(filename, 'rb') as f:
        requests.post(url, data={'chat_id': ADMIN_ID}, files={'document': f})

    os.remove(filename)
    return "Uploaded to Telegram ✅"
