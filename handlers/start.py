from telegram import Update
from telegram.ext import ContextTypes
from services.database import add_user
from keyboards.inline import get_start_keyboard

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username)
    
    welcome_msg = (
        f"👋 Welcome *{user.first_name}* to the professional **Watermark Management Bot**!\n\n"
        "Safely configure and merge overlays using the tools below:\n"
        "➕ *Add Text Watermarks*\n"
        "🖼️ *Add Logo/Image Overlays*\n"
        "❌ *Remove Personal Watermarks*\n"
        "⚙️ *Customize Default Templates*\n\n"
        "Choose an action to proceed:"
    )
    
    if update.message:
        await update.message.reply_text(welcome_msg, parse_mode="Markdown", reply_markup=get_start_keyboard())
    elif update.callback_query:
        await update.callback_query.message.edit_text(welcome_msg, parse_mode="Markdown", reply_markup=get_start_keyboard())
