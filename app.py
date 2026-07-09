from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
from utils.config import BOT_TOKEN
from utils.logger import logger
from services.database import init_db
from handlers.start import start_handler
from handlers.help import help_handler
from handlers.about import about_handler
from handlers.history import history_handler
from handlers.settings import settings_handler, settings_callback
from handlers import add_watermark, remove_watermark

def main():
    logger.info("Initializing persistent system runtime databases...")
    init_db()
    
    logger.info("Building asynchronous telegram bot orchestration runtime cluster...")
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Conversations Workflows Definitions
    add_wm_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(add_watermark.start_add_workflow, pattern="^wm_add$")],
        states={
            add_watermark.UPLOAD_BASE: [MessageHandler(filters.PHOTO | filters.Document.IMAGE, add_watermark.base_image_received)],
            add_watermark.SELECT_TYPE: [CallbackQueryHandler(add_watermark.type_selected, pattern="^type_")],
            add_watermark.INPUT_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_watermark.text_input_received)],
            add_watermark.SELECT_FONT: [CallbackQueryHandler(add_watermark.font_selected, pattern="^font_")],
            add_watermark.SELECT_COLOR: [
                CallbackQueryHandler(add_watermark.color_selected, pattern="^color_"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, add_watermark.custom_hex_received)
            ],
            add_watermark.SELECT_SIZE: [CallbackQueryHandler(add_watermark.size_selected, pattern="^size_")],
            add_watermark.SELECT_OPACITY: [CallbackQueryHandler(add_watermark.opacity_selected, pattern="^opacity_")],
            add_watermark.SELECT_POSITION: [CallbackQueryHandler(add_watermark.position_selected, pattern="^pos_")],
            add_watermark.UPLOAD_LOGO: [MessageHandler(filters.PHOTO | filters.Document.IMAGE, add_watermark.logo_uploaded)],
            add_watermark.PREVIEW_DECISION: [CallbackQueryHandler(add_watermark.process_decision, pattern="^action_")]
        },
        fallbacks=[CommandHandler("start", start_handler)],
        per_message=False
    )
    
    remove_wm_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(remove_watermark.start_remove_workflow, pattern="^wm_remove$")],
        states={
            remove_watermark.RM_UPLOAD: [MessageHandler(filters.PHOTO | filters.Document.IMAGE, remove_watermark.remove_image_received)],
            remove_watermark.RM_METHOD: [CallbackQueryHandler(remove_watermark.method_selected, pattern="^remove_")],
            remove_watermark.RM_EXECUTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, remove_watermark.execution_parameters_received)]
        },
        fallbacks=[CommandHandler("start", start_handler)],
        per_message=False
    )
    
    # Commands Mapping Nodes
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("about", about_handler))
    app.add_handler(CommandHandler("history", history_handler))
    app.add_handler(CommandHandler("settings", settings_handler))
    
    # Callback fallbacks mapping layout routers
    app.add_handler(CallbackQueryHandler(help_handler, pattern="^wm_help$"))
    app.add_handler(CallbackQueryHandler(about_handler, pattern="^wm_about$"))
    app.add_handler(CallbackQueryHandler(settings_callback, pattern="^cfg_|^font_|^color_|^opacity_|^pos_"))
    
    app.add_handler(add_wm_conv)
    app.add_handler(remove_wm_conv)
    
    logger.info("Bot Engine online and listening for events...")
    app.run_polling()

if __name__ == "__main__":
    main()
