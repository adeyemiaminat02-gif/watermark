from telegram import Update
from telegram.ext import ContextTypes

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📖 **Watermark Bot Guide**\n\n"
        "📍 **Adding Overlays:**\n"
        "1. Click `➕ Add Watermark` or type /start.\n"
        "2. Upload your source asset image (`JPG`, `PNG`, `WEBP`).\n"
        "3. Follow the dynamic config menus to build or attach your logo.\n\n"
        "📍 **Removing Content:**\n"
        "• Intended specifically for elements you hold explicit modification authorization for.\n"
        "• Use `Crop` or target coordinates via structural `Inpainting` vectors.\n\n"
        "📂 **Limits:** Max file size supported is 10 Megabytes."
    )
    if update.message:
        await update.message.reply_text(help_text, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.message.edit_text(help_text, parse_mode="Markdown")
