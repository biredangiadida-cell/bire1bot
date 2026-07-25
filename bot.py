import json

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# ================= CONFIG =================

BOT_TOKEN = "8665819961:AAEGEgdg8XuvSSe1FyRxKgcn4FqgtPMwznY"

ADMIN_ID = 6836792869

PAYMENT_AMOUNT = 200
TELEBIRR = "0982485937"
CBE = "1000291766734"

DATA_FILE = "members.json"

# ================= DATABASE =================

def load_members():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_members(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

members = load_members()

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("📝 Galmaa'i", callback_data="register")]
    ]

    await update.message.reply_text(
        "👋 Baga nagaan dhuftan.\n\n"
        "Kaffaltiin miseensummaa: 200 ETB\n"
        "Galmaa'uuf button armaan gadii cuqaasi.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
