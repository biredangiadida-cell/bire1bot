import json

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    BotCommand
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

BOT_TOKEN = "8665819961:AAG8QHu3Wqkh5kq4-5Y-b3-lyYTv4BkbcQU"

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

# ================= MENU =================

async def set_commands(app):

    commands = [
        BotCommand("start", "Start ELBS"),
        BotCommand("users", "Members"),
        BotCommand("stats", "Statistics"),
        BotCommand("broadcast", "Broadcast")
    ]

    await app.bot.set_my_commands(commands)
