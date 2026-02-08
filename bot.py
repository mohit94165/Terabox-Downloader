import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 6728678197
WEBSITE_URL = "https://worker-production-43b5.up.railway.app"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    await update.message.reply_text("Send Terabox link")


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    link = update.message.text.strip()

    keyboard = [[
        InlineKeyboardButton(
            "📥 OPEN DOWNLOAD PAGE",
            url=f"{WEBSITE_URL}/?link={link}"
        )
    ]]

    await update.message.reply_text(
        "Open site → download file → upload back to Telegram",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("Bot Running...")
app.run_polling()
