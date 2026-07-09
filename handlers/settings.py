from telegram import Update
from telegram.ext import ContextTypes
from services.database import get_settings, update_setting
from keyboards.inline import get_font_keyboard, get_color_keyboard, get_opacity_keyboard, get_position_keyboard

async def settings_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    cfg = get_settings(user_id)
    
    msg = (
        "⚙️ **Your Global Profile Parameters Configuration:**\n\n"
         f"• 🔤 Font Engine Family: `{cfg['font']}`\n"
         f"• 🎨 Tone Canvas Tint: `{cfg['color']}`\n"
         f"• 🌓 Transparency Scale: `{cfg['opacity']}%`\n"
         f"• 📍 Grid Anchor Position: `{cfg['position']}`\n\n"
         "Select a parameter field node to adjust:"
    )
    
    kb = [
        [InlineKeyboardButton("Change Font", callback_data="cfg_font"), InlineKeyboardButton("Change Tint Color", callback_data="cfg_color")],
        [InlineKeyboardButton("Change Opacity", callback_data="cfg_opacity"), InlineKeyboardButton("Change Position Anchor", callback_data="cfg_pos")]
    ]
    
    await update.effective_message.reply_text(msg, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

async def settings_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data == "cfg_font":
        await query.message.edit_text("Select global default font style matrix:", reply_markup=get_font_keyboard())
    elif data == "cfg_color":
        await query.message.edit_text("Select default structural color variant:", reply_markup=get_color_keyboard())
    elif data == "cfg_opacity":
        await query.message.edit_text("Select density scalar parameters configuration:", reply_markup=get_opacity_keyboard())
    elif data == "cfg_pos":
        await query.message.edit_text("Select coordinate alignment layout configuration:", reply_markup=get_position_keyboard())
    elif data.startswith("font_"):
        val = data.replace("font_", "")
        update_setting(query.from_user.id, "font", val)
        await query.message.edit_text(f"✅ Default Font updated to: `{val}`", parse_mode="Markdown")
    elif data.startswith("color_"):
        val = data.replace("color_", "")
        if val == "Custom HEX":
            context.user_data["state"] = "SETTING_HEX"
            await query.message.edit_text("Please type your custom Hex Color Value below (e.g. `#FF5733`):")
        else:
            update_setting(query.from_user.id, "color", val)
            await query.message.edit_text(f"✅ Default Color Variant updated to: `{val}`", parse_mode="Markdown")
    elif data.startswith("opacity_"):
        val = data.replace("opacity_", "")
        update_setting(query.from_user.id, "opacity", int(val))
        await query.message.edit_text(f"✅ Default Opacity Level scalar updated to: `{val}%`", parse_mode="Markdown")
    elif data.startswith("pos_"):
        val = data.replace("pos_", "")
        update_setting(query.from_user.id, "position", val)
        await query.message.edit_text(f"✅ Default Positioning layout anchored at: `{val}`", parse_mode="Markdown")
