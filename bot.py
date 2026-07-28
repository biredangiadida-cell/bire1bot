# ================= KUTAA 1 =================

import os
import json

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    filters
)


# ================= TOKEN =================

BOT_TOKEN = "TOKEN_KEE_AS_GALCHI"


# ================= ADMIN =================

ADMIN_ID = 6836792869


# ================= PAYMENT =================

PAYMENT_AMOUNT = 200
TELEBIRR = "0982485937"
CBE = "1000291766734"


# ================= DATABASE =================

DATA_FILE = "members.json"


def load_members():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}


def save_members(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


members = load_members()
