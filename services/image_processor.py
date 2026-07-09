import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

COLOR_MAP = {
    "White": (255, 255, 255),
    "Black": (0, 0, 0),
    "Gray": (128, 128, 128),
    "Red": (255, 0, 0),
    "Blue": (0, 0, 255),
    "Green": (0, 255, 0)
}

FONT_SIZE_MAP = {
    "Small": 0.03,
    "Medium": 0.05,
    "Large": 0.08,
    "Extra Large": 0.12
}

def get_hex_color(hex_str: str):
    try:
        hex_str = hex_str.lstrip('#')
        return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))
    except Exception:
        return (255, 255, 255)

def calculate_position(pos_str: str, base_w: int, base_h: int, comp_w: int, comp_h: int, margin=20):
    positions = {
        "Top Left": (margin, margin),
        "Top Center": ((base_w - comp_w) // 2, margin),
        "Top Right": (base_w - comp_w - margin, margin),
        "Center": ((base_w - comp_w) // 2, (base_h - comp_h) // 2),
        "Bottom Left": (margin, base_h - comp_h - margin),
        "Bottom Center": ((base_w - comp_w) // 2, base_h - comp_h - margin),
        "Bottom Right": (base_w - comp_w - margin, base_h - comp_h - margin)
    }
    return positions.get(pos_str, (margin, base_h - comp_h - margin))

def add_text_watermark(image_path: str, text: str, config: dict, output_path: str):
    with Image.open(image_path).convert("RGBA") as base_img:
        txt_layer = Image.new("RGBA", base_img.size, (255, 255, 255, 0))
        
        # Determine dynamic font size
        scale = FONT_SIZE_MAP.get(config.get("size", "Medium"), 0.05)
        font_size = max(15, int(base_img.size[0] * scale))
        
        try:
            font = ImageFont.truetype(f"utils/fonts/{config.get('font', 'Arial')}.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()
            
        draw = ImageDraw.Draw(txt_layer)
        bbox = draw.textbbox((0, 0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        
        x, y = calculate_position(config.get("position", "Bottom Right"), base_img.size[0], base_img.size[1], w, h)
        
        color_name = config.get("color", "White")
        rgb = get_hex_color(color_name) if color_name.startswith("#") else COLOR_MAP.get(color_name, (255, 255, 255))
        alpha = int(255 * (int(config.get("opacity", 50)) / 100))
        
        draw.text((x, y), text, fill=rgb + (alpha,), font=font)
        
        final_img = Image.alpha_composite(base_img, txt_layer)
        if base_img.mode in ("RGB", "JPEG"):
            final_img = final_img.convert("RGB")
        final_img.save(output_path)

def add_image_watermark(image_path: str, logo_path: str, config: dict, output_path: str):
    with Image.open(image_path).convert("RGBA") as base_img, Image.open(logo_path).convert("RGBA") as logo:
        base_w, base_h = base_img.size
        
        # Scale logo down to max 20% width/height of background image
        max_logo_w = int(base_w * 0.20)
        max_logo_h = int(base_h * 0.20)
        logo.thumbnail((max_logo_w, max_logo_h), Image.Resampling.LANCZOS)
        
        # Apply opacity adjustment
        alpha = int(255 * (int(config.get("opacity", 50)) / 100))
        logo_channels = logo.split()
        if len(logo_channels) == 4:
            r, g, b, a = logo_channels
            a = a.point(lambda p: min(p, alpha))
            logo = Image.merge("RGBA", (r, g, b, a))
            
        x, y = calculate_position(config.get("position", "Bottom Right"), base_w, base_h, logo.size[0], logo.size[1])
        
        logo_layer = Image.new("RGBA", base_img.size, (255, 255, 255, 0))
        logo_layer.paste(logo, (x, y))
        
        final_img = Image.alpha_composite(base_img, logo_layer)
        if base_img.mode in ("RGB", "JPEG"):
            final_img = final_img.convert("RGB")
        final_img.save(output_path)

def crop_image_region(image_path: str, box: tuple, output_path: str):
    with Image.open(image_path) as img:
        # Box order expected: (x1, y1, x2, y2)
        cropped = img.crop(box)
        cropped.save(output_path)

def inpaint_image_region(image_path: str, box: tuple, output_path: str):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read base image matrix.")
    
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    x1, y1, x2, y2 = box
    # Bound-checking box properties
    h, w = img.shape[:2]
    x1, x2 = max(0, min(x1, w)), max(0, min(x2, w))
    y1, y2 = max(0, min(y1, h)), max(0, min(y2, h))
    
    mask[y1:y2, x1:x2] = 255
    dst = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
    cv2.imwrite(output_path, dst)
