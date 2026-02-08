import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 6728678197
DOWNLOAD_PATH = "downloads"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)


def get_direct_link(tera_url):
    api = "https://terabox-dl-api.vercel.app/api?url=" + tera_url
    r = requests.get(api).json()
    if r.get("status") == "success":
        return r["download_url"]
    return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    await update.message.reply_text("Send Terabox link 🔗")


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    url = update.message.text
    msg = await update.message.reply_text("Getting file link...")

    direct = get_direct_link(url)
    if not direct:
        await msg.edit_text("Terabox server busy ❌ Try again later")
        return

    filename = os.path.join(DOWNLOAD_PATH, direct.split("/")[-1])

    await msg.edit_text("Downloading ⏬")

    with requests.get(direct, stream=True) as r:
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    await msg.edit_text("Uploading ⏫")

    await update.message.reply_document(document=open(filename, 'rb'))
    os.remove(filename)
    await msg.delete()


app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("Bot Running...")
app.run_polling()
