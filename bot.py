import os
import requests
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 6728678197
DOWNLOAD_PATH = "downloads"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)


# 🔍 Extract Terabox direct link
def get_terabox_direct_link(url):
    api = "https://teraboxvideodownloader.nepcoderdevs.workers.dev/?url=" + url
    r = requests.get(api).json()
    if "download_url" in r:
        return r["download_url"]
    return None


# 📊 Progress bar
async def progress(current, total, msg, text):
    percent = current * 100 / total
    bar = "█" * int(percent/5) + "░" * (20-int(percent/5))
    try:
        await msg.edit_text(f"{text}\n[{bar}] {percent:.1f}%")
    except:
        pass


# 🚀 Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    await update.message.reply_text("Send Terabox video/file link 🔗")


# 📥 Handle link
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    url = update.message.text
    msg = await update.message.reply_text("Extracting Terabox link...")

    direct = get_terabox_direct_link(url)
    if not direct:
        await msg.edit_text("Failed to get file link ❌")
        return

    filename = os.path.join(DOWNLOAD_PATH, direct.split("/")[-1])

    await msg.edit_text("Downloading file ⏬")

    with requests.get(direct, stream=True) as r:
        total = int(r.headers.get('content-length', 0))
        downloaded = 0
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    await progress(downloaded, total, msg, "Downloading")

    await msg.edit_text("Uploading to Telegram ⏫")

    await update.message.reply_document(document=open(filename, 'rb'))

    os.remove(filename)
    await msg.delete()


# 🏁 Run
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("Bot Running...")
app.run_polling()
