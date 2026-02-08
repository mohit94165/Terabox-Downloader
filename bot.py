import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 6728678197

DOWNLOAD_PATH = "downloads"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)


# 🎯 Progress bar for Telegram message edit
async def progress_bar(current, total, message, start_time, action):
    percent = current * 100 / total
    bar = "█" * int(percent / 5) + "░" * (20 - int(percent / 5))
    try:
        await message.edit_text(f"{action}...\n[{bar}] {percent:.1f}%")
    except:
        pass


# 🎬 yt-dlp progress hook
def ytdlp_hook(d):
    if d['status'] == 'downloading':
        print("Downloading:", d['_percent_str'])
    elif d['status'] == 'finished':
        print("Download finished")


# 🔐 Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    await update.message.reply_text("Send Terabox video/file link 🔗")


# 📥 Handle links
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    url = update.message.text
    msg = await update.message.reply_text("Checking link...")

    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_PATH}/%(title)s.%(ext)s',
        'progress_hooks': [ytdlp_hook],
        'cookiefile': 'cookies.txt',   # optional if needed
        'nocheckcertificate': True,
        'quiet': True,
    }

    try:
        await msg.edit_text("Downloading from Terabox ⏬")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        await msg.edit_text("Uploading to Telegram ⏫")

        with open(file_path, 'rb') as f:
            await update.message.reply_document(
                document=f,
                filename=os.path.basename(file_path)
            )

        os.remove(file_path)
        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"Error: {e}")


# 🏁 Main
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

print("Bot Running...")
app.run_polling()
