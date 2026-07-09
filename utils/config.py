import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL", "data/bot.db")

# Ensure required directories exist
os.makedirs(os.path.dirname(DATABASE_URL) or "data", exist_ok=True)
os.makedirs("downloads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

SUPPORTED_FORMATS = ["JPG", "JPEG", "PNG", "WEBP"]
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
