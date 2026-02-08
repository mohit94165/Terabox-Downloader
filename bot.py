import os
import re
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 6728678197
DOWNLOAD_PATH = "downloads"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)


# 🔎 Extract direct download link from Terabox page
def extract_direct_link(url):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.terabox.com/"
    }
    r = requests.get(url, headers=headers)
    match = re.search(r'"downloadUrl":"(.*?)"', r.text)
    if match:
        return match.group(1).replace("\\/", "/")
    return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    await update.message.reply_text("Send Terabox video/file link 🔗")


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    url = update.message.text
    msg = await update.message.reply_text("Getting file link...")

    direct = extract_direct_link(url)
    if not direct:
        await msg.edit_text("Failed to extract file ❌")
        return

    filename = os.path.join(DOWNLOAD_PATH, direct.split("/")[-1])

    await msg.edit_text("Downloading ⏬")

    with requests.get(direct, stream=True) as r:
        total = int(r.headers.get('content-length', 0))
        downloaded = 0
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)

    await msg.edit_text("Uploading ⏫")

    await update.message.reply_document(document=open(filename, 'rb'))
    os.remove(filename)
    await msg.delete()


app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("Bot Running...")
app.run_polling()
