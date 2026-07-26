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

BOT_TOKEN = "YOUR_NEW_BOT_TOKEN"

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


# ================= MENU COMMANDS =================

async def set_commands(app):

    commands = [
        BotCommand("start", "Jalqabi"),
        BotCommand("users", "Miseensota"),
        BotCommand("stats", "Statistics"),
        BotCommand("broadcast", "Ergaa hundaaf ergi")
    ]

    await app.bot.set_my_commands(commands)


# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("📝 Galmaa'i", callback_data="register"),
            InlineKeyboardButton("💳 Kaffaltii", callback_data="payment")
        ],
        [
            InlineKeyboardButton("👤 Account Koo", callback_data="account"),
            InlineKeyboardButton("📢 Beeksisa", callback_data="news")
        ],
        [
            InlineKeyboardButton("📞 Nu Qunnamaa", callback_data="contact"),
            InlineKeyboardButton("❓ Gargaarsa", callback_data="help")
        ]
    ]

    await update.message.reply_text(
        "🤖 BIRE ONLINE IKUB\n\n"
        "Baga nagaan dhuftan!\n\n"
        "Button keessaa tokko filadhaa.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
