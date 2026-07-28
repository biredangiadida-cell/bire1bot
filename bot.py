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

    await app.bot.set_my_commands(commands)*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

body{
    font-family:Arial,sans-serif;
    line-height:1.6;
}

.hero{
    background:url("church.jpg") center/cover no-repeat;
    color:white;
    padding:120px 20px;
    text-align:center;
}

.button{
    display:inline-block;
    margin-top:20px;
    background:#0b5ed7;
    color:white;
    padding:15px 30px;
    border-radius:30px;
    transition:.3s;
}

.button:hover{
    background:#084298;
    transform:scale(1.05);
}

.card{
    background:white;
    border-radius:12px;
    box-shadow:0 5px 15px rgba(0,0,0,.15);
    padding:25px;
    margin:20px auto;
}
