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


members = load_members()# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "📝 Galmaa'i",
                callback_data="register"
            ),
            InlineKeyboardButton(
                "📚 Koorsoota",
                callback_data="courses"
            )
        ],
        [
            InlineKeyboardButton(
                "💳 Kaffaltii",
                callback_data="payment"
            ),
            InlineKeyboardButton(
                "📤 Receipt",
                callback_data="receipt"
            )
        ],
        [
            InlineKeyboardButton(
                "👤 Account Koo",
                callback_data="account"
            ),
            InlineKeyboardButton(
                "🌐 Website",
                callback_data="website"
            )
        ],
        [
            InlineKeyboardButton(
                "📢 Beeksisa",
                callback_data="news"
            ),
            InlineKeyboardButton(
                "📞 Nu Qunnamaa",
                callback_data="contact"
            )
        ],
        [
            InlineKeyboardButton(
                "❓ Gargaarsa",
                callback_data="help"
            ),
            InlineKeyboardButton(
                "ℹ️ Waa'ee ELBS",
                callback_data="about"
            )
        ]
    ]


    await update.message.reply_text(
        "🎓 *ELBS*\n"
        "Everlasting Love Bible School\n\n"
        "Baga nagaan dhuftan!\n\n"
        "📖 Barnoota Macaafa Qulqulluu online.\n\n"
        "👇 Tajaajila barbaaddan keessaa tokko filadhaa.",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
