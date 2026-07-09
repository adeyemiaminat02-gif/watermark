from telegram import Update
from telegram.ext import ContextTypes
from services.database import get_history

async def history_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    history_records = get_history(user_id, limit=10)
    
    if not history_records:
        await update.effective_message.reply_text("🗄️ Your transactional execution history log is currently empty.")
        return
        
    response = "🗄️ **Your Recent Processing Operations Logs (Last 10):**\n\n"
    for idx, item in enumerate(history_records, 1):
        response += f"{idx}. *{item['action_type']}* -> `{item['filename']}` \n   📅 _{item['timestamp']}_\n\n"
        
    await update.effective_message.reply_text(response, parse_mode="Markdown")
