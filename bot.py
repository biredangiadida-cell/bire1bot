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
# ================= BUTTONS =================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "register":
        context.user_data["step"] = "name"
        await query.edit_message_text(
            "📝 Maqaa guutuu kee barreessi:"
        )

    elif query.data == "courses":
        await query.edit_message_text(
            "📚 Koorsoota ELBS\n\n"
            "📖 Jaalala Waaqayyoo\n"
            "✝️ Fayyina fi Ayyaana\n"
            "⚖️ Seeraa fi Firdii"
        )

    elif query.data == "payment":
        context.user_data["step"] = "payment"

        await query.edit_message_text(
            f"💳 Kaffaltii Galmee\n\n"
            f"💰 Qarshii: {PAYMENT_AMOUNT} ETB\n\n"
            f"📲 Telebirr: {TELEBIRR}\n"
            f"🏦 CBE: {CBE}\n\n"
            "Kaffaltii booda receipt ergi."
        )

    elif query.data == "website":
        await query.edit_message_text(
            "🌐 Website ELBS\n\n"
            "https://biredangiadida-cell.github.io/ELBS/"
        )

    elif query.data == "about":
        await query.edit_message_text(
            "🎓 Everlasting Love Bible School\n\n"
            "Founder: Brother Biratu Dangia\n"
            "📞 0982485937\n"
            "📧 biredangiadida@gmail.com"
        )# ================= REGISTRATION =================

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    step = context.user_data.get("step")

    if step == "name":

        context.user_data["name"] = update.message.text
        context.user_data["step"] = "phone"

        await update.message.reply_text(
            "📱 Lakkoofsa bilbilaa kee barreessi:"
        )

    elif step == "phone":

        user_id = str(update.message.chat_id)

        members[user_id] = {
            "name": context.user_data["name"],
            "phone": update.message.text,
            "approved": False
        }

        save_members(members)

        context.user_data["step"] = "payment"

        await update.message.reply_text(
            f"✅ Galmeen kee galmaa'eera.\n\n"
            f"💳 Kaffaltii: {PAYMENT_AMOUNT} ETB\n\n"
            f"📲 Telebirr: {TELEBIRR}\n"
            f"🏦 CBE: {CBE}\n\n"
            "📤 Amma receipt kee ergi."
        )
