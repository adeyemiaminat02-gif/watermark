from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
import os
from utils.config import SUPPORTED_FORMATS, MAX_FILE_SIZE
from services.database import get_settings, log_history
from services.image_processor import add_text_watermark, add_image_watermark
from keyboards.inline import (
    get_watermark_type_keyboard, get_font_keyboard, get_color_keyboard,
    get_size_keyboard, get_opacity_keyboard, get_position_keyboard, get_preview_keyboard
)

(UPLOAD_BASE, SELECT_TYPE, INPUT_TEXT, SELECT_FONT, SELECT_COLOR, 
 SELECT_SIZE, SELECT_OPACITY, SELECT_POSITION, UPLOAD_LOGO, PREVIEW_DECISION) = range(10)

async def start_add_workflow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data.clear()
    await query.message.edit_text("📸 Please send/upload the high-res image source file asset node:")
    return UPLOAD_BASE

async def base_image_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    photo = msg.photo[-1] if msg.photo else msg.document
    
    if not photo:
        await msg.reply_text("❌ Input error. Please attach a valid image container file.")
        return UPLOAD_BASE
        
    if msg.document and msg.document.mime_type.split('/')[-1].upper() not in SUPPORTED_FORMATS:
        await msg.reply_text("❌ Format error. Supported matrix transformations: JPG, JPEG, PNG, WEBP.")
        return UPLOAD_BASE

    file_obj = await context.bot.get_file(photo.file_id)
    ext = msg.document.file_name.split('.')[-1] if msg.document else "jpg"
    dest_path = f"downloads/base_{msg.from_user.id}.{ext}"
    
    await file_obj.download_to_drive(dest_path)
    context.user_data["base_img"] = dest_path
    
    user_defaults = get_settings(msg.from_user.id)
    context.user_data["config"] = user_defaults
    
    await msg.reply_text("Select your desired overlay type layer structural processing module:", reply_markup=get_watermark_type_keyboard())
    return SELECT_TYPE

async def type_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "type_text":
        context.user_data["wm_type"] = "TEXT"
        await query.message.edit_text("📝 Enter custom overlay text sequence:")
        return INPUT_TEXT
    elif query.data == "type_image":
        context.user_data["wm_type"] = "IMAGE"
        await query.message.edit_text("🖼️ Please upload a transparent PNG image logo template:")
        return UPLOAD_LOGO

async def text_input_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["text_val"] = update.message.text
    await update.message.reply_text("Select font type matrix configuration:", reply_markup=get_font_keyboard())
    return SELECT_FONT

async def font_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["config"]["font"] = query.data.replace("font_", "")
    await query.message.edit_text("Select color visualization spectrum palette:", reply_markup=get_color_keyboard())
    return SELECT_COLOR

async def color_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data.replace("color_", "")
    
    if choice == "Custom HEX":
        await query.message.edit_text("Please enter your custom HEX text configuration sequence (e.g., `#FF5733`):")
        return SELECT_COLOR
        
    context.user_data["config"]["color"] = choice
    await query.message.edit_text("Select relative size presets:", reply_markup=get_size_keyboard())
    return SELECT_SIZE

async def custom_hex_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.strip()
    if not txt.startswith("#") or len(txt) != 7:
        await update.message.reply_text("❌ Input validation error. Expected strict `#FFFFFF` template standard. Re-enter:")
        return SELECT_COLOR
    context.user_data["config"]["color"] = txt
    await update.message.reply_text("Select scale dimensions configuration profile:", reply_markup=get_size_keyboard())
    return SELECT_SIZE

async def size_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["config"]["size"] = query.data.replace("size_", "")
    await query.message.edit_text("Select alpha-channel density opacity configuration layer matrix:", reply_markup=get_opacity_keyboard())
    return SELECT_OPACITY

async def opacity_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["config"]["opacity"] = query.data.replace("opacity_", "")
    await query.message.edit_text("Select dynamic grid spatial position anchor parameters:", reply_markup=get_position_keyboard())
    return SELECT_POSITION

async def logo_uploaded(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    doc = msg.document or (msg.photo[-1] if msg.photo else None)
    if not doc:
        await msg.reply_text("❌ Please submit a valid image file matrix.")
        return UPLOAD_LOGO
        
    file_obj = await context.bot.get_file(doc.file_id)
    logo_path = f"downloads/logo_{msg.from_user.id}.png"
    await file_obj.download_to_drive(logo_path)
    context.user_data["logo_path"] = logo_path
    
    await msg.reply_text("Select structural localization position placement configuration metrics:", reply_markup=get_position_keyboard())
    return SELECT_POSITION

async def position_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["config"]["position"] = query.data.replace("pos_", "")
    
    await query.message.edit_text("⏳ Compiling and pipeline processing preview matrix layers...")
    
    out_path = f"outputs/preview_{query.from_user.id}.png"
    base = context.user_data["base_img"]
    cfg = context.user_data["config"]
    
    try:
        if context.user_data["wm_type"] == "TEXT":
            add_text_watermark(base, context.user_data["text_val"], cfg, out_path)
        else:
            add_image_watermark(base, context.user_data["logo_path"], cfg, out_path)
            
        context.user_data["output_path"] = out_path
        await query.message.delete()
        await query.message.channel_post.reply_to_message  # safe fallback
    except Exception:
        pass

    await context.bot.send_photo(
        chat_id=query.message.chat_id,
        photo=open(out_path, 'rb'),
        caption="🎭 **Pipeline Processing Canvas Preview Canvas Generation:**\n\nApply configuration adjustments permanently?",
        parse_mode="Markdown",
        reply_markup=get_preview_keyboard()
    )
    return PREVIEW_DECISION

async def process_decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "action_apply":
        out_path = context.user_data.get("output_path")
        if out_path and os.path.exists(out_path):
            filename = os.path.basename(out_path)
            log_history(query.from_user.id, f"Added {context.user_data['wm_type']} Watermark", filename)
            
            await query.message.delete()
            await context.bot.send_document(
                chat_id=query.message.chat_id,
                document=open(out_path, 'rb'),
                caption="✅ Pipeline compilation complete. Document payload distributed successfully in master target resolutions."
            )
        else:
            await query.message.edit_text("❌ Operational compilation failure. Data structures expired.")
    else:
        await query.message.edit_text("❌ Action transaction sequence halted.")
        
    return ConversationHandler.END
