from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
import os
from utils.config import SUPPORTED_FORMATS
from services.database import log_history
from services.image_processor import crop_image_region, inpaint_image_region
from keyboards.inline import get_removal_options_keyboard

RM_UPLOAD, RM_METHOD, RM_EXECUTE = range(3)

async def start_remove_workflow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data.clear()
    
    notice = (
        "⚖️ **Legal Usage Policy Notice Verification Gateway:**\n\n"
        "Watermark removal architecture engine tools are structurally limited strictly to files "
        "you hold authenticated modification rights or authorial creation authorization to adapt.\n\n"
        "📸 Send the target media element document asset to process:"
    )
    await query.message.edit_text(notice, parse_mode="Markdown")
    return RM_UPLOAD

async def remove_image_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    photo = msg.photo[-1] if msg.photo else msg.document
    
    if not photo:
        await msg.reply_text("❌ File type error node. Upload a valid image.")
        return RM_UPLOAD
        
    file_obj = await context.bot.get_file(photo.file_id)
    ext = msg.document.file_name.split('.')[-1] if msg.document else "jpg"
    dest_path = f"downloads/rm_base_{msg.from_user.id}.{ext}"
    
    await file_obj.download_to_drive(dest_path)
    context.user_data["rm_base"] = dest_path
    
    await msg.reply_text(
        "Select programmatic matrix destruction/correction method pipeline configuration:", 
        reply_markup=get_removal_options_keyboard()
    )
    return RM_METHOD

async def method_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "remove_crop":
        context.user_data["rm_mode"] = "CROP"
        await query.message.edit_text(
            "✂️ **Crop Parameter Input Execution:**\n\n"
            "Please explicitly write out pixel dimensional crop configurations mapping parameters:\n"
            "`x1, y1, x2, y2`\n"
            "Example: `0, 0, 500, 450` to maintain upper top segment canvas space.",
            parse_mode="Markdown"
        )
        return RM_EXECUTE
    elif query.data == "remove_inpaint":
        context.user_data["rm_mode"] = "INPAINT"
        await query.message.edit_text(
            "🪄 **Inpaint Matrix Mask Coordinates Mapping Execution:**\n\n"
            "Provide bounding box coordinates enclosing target noise area to heal/inpaint:\n"
            "`x1, y1, x2, y2`\n"
            "Example: `100, 100, 200, 200`",
            parse_mode="Markdown"
        )
        return RM_EXECUTE
        
    return ConversationHandler.END

async def execution_parameters_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text
    try:
        coords = tuple(int(c.strip()) for c in txt.split(","))
        if len(coords) != 4:
            raise ValueError()
    except ValueError:
        await update.message.reply_text("❌ Formatting structure matrix mismatch. Please enter exactly 4 integer parameters numerical coordinates split by comma:")
        return RM_EXECUTE

    base = context.user_data["rm_base"]
    mode = context.user_data["rm_mode"]
    out_path = f"outputs/rm_final_{update.message.from_user.id}.png"
    
    await update.message.reply_text("⏳ Processing computational tensor transformation vectors...")
    
    try:
        if mode == "CROP":
            crop_image_region(base, coords, out_path)
        else:
            inpaint_image_region(base, coords, out_path)
            
        log_history(update.message.from_user.id, f"Removed Watermark via {mode}", os.path.basename(out_path))
        
        await update.message.reply_document(
            document=open(out_path, 'rb'),
            caption="✅ Programmatic repair operations matrix calculation sequence executed successfully."
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Structural engineering pipeline computation anomaly: {str(e)}")
        
    return ConversationHandler.END
