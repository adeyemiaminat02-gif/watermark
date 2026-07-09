from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_start_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Watermark", callback_data="wm_add"),
         InlineKeyboardButton("❌ Remove Watermark", callback_data="wm_remove")],
        [InlineKeyboardButton("📖 Help", callback_data="wm_help"),
         InlineKeyboardButton("ℹ️ About", callback_data="wm_about")]
    ])

def get_watermark_type_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Text Watermark", callback_data="type_text")],
        [InlineKeyboardButton("🖼️ Image Logo Watermark", callback_data="type_image")]
    ])

def get_font_keyboard():
    fonts = ["Arial", "Roboto", "Open Sans", "Times New Roman", "Montserrat"]
    return InlineKeyboardMarkup([[InlineKeyboardButton(f, callback_data=f"font_{f}")] for f in fonts])

def get_color_keyboard():
    colors = ["White", "Black", "Gray", "Red", "Blue", "Green", "Custom HEX"]
    return InlineKeyboardMarkup([[InlineKeyboardButton(c, callback_data=f"color_{c}")] for c in colors])

def get_size_keyboard():
    sizes = ["Small", "Medium", "Large", "Extra Large"]
    return InlineKeyboardMarkup([[InlineKeyboardButton(s, callback_data=f"size_{s}")] for s in sizes])

def get_opacity_keyboard():
    opacities = ["10", "30", "50", "70", "90", "100"]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"{o}%", callback_data=f"opacity_{o}") for o in opacities[:3]],
        [InlineKeyboardButton(f"{o}%", callback_data=f"opacity_{o}") for o in opacities[3:]]
    ])

def get_position_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Top Left", callback_data="pos_Top Left"), InlineKeyboardButton("Top Center", callback_data="pos_Top Center"), InlineKeyboardButton("Top Right", callback_data="pos_Top Right")],
        [InlineKeyboardButton("- - - Center - - -", callback_data="pos_Center")],
        [InlineKeyboardButton("Bottom Left", callback_data="pos_Bottom Left"), InlineKeyboardButton("Bottom Center", callback_data="pos_Bottom Center"), InlineKeyboardButton("Bottom Right", callback_data="pos_Bottom Right")]
    ])

def get_preview_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Apply", callback_data="action_apply"),
         InlineKeyboardButton("❌ Cancel", callback_data="action_cancel")]
    ])

def get_removal_options_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✂️ Crop Margin Out", callback_data="remove_crop")],
        [InlineKeyboardButton("🪄 Structural Inpainting Area", callback_data="remove_inpaint")],
        [InlineKeyboardButton("❌ Cancel", callback_data="action_cancel")]
    ])
