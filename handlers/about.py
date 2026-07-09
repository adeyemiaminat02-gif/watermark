from telegram import Update
from telegram.ext import ContextTypes

async def about_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = (
        "ℹ️ **About Systems Portal**\n\n"
        "• **Bot Name:** Watermark Management Assistant\n"
        "• **Version:** 1.0.0 (Production Core)\n"
        "• **Engine Core:** Powered by Python 3.12, Pillow, and OpenCV structural matrices.\n"
        "• **Framework:** `python-telegram-bot` asynchronous framework implementation Architecture.\n"
    )
    if update.message:
        await update.message.reply_text(about_text, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.message.edit_text(about_text, parse_mode="Markdown")
