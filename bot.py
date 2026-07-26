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
    )# ================= BUTTONS =================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    # ================= REGISTER =================

    if query.data == "register":

        context.user_data["step"] = "name"

        await query.edit_message_text(
            "📝 Maqaa guutuu kee barreessi:"
        )

    # ================= PAYMENT =================

    elif query.data == "payment":

        await query.edit_message_text(
            f"💳 Kaffaltii Miseensummaa\n\n"
            f"💰 Qarshii: {PAYMENT_AMOUNT} ETB\n\n"
            f"📲 Telebirr: {TELEBIRR}\n"
            f"🏦 CBE: {CBE}\n\n"
            "Erga kaffalte booda screenshot receipt ergi."
        )

    # ================= ACCOUNT =================

    elif query.data == "account":

        user_id = str(query.from_user.id)

        if user_id in members:

            data = members[user_id]

            status = (
                "✅ Approved"
                if data.get("approved")
                else "⏳ Pending"
            )

            await query.edit_message_text(
                f"👤 ACCOUNT KOO\n\n"
                f"📝 Maqaa: {data['name']}\n"
                f"📱 Bilbila: {data['phone']}\n"
                f"📊 Haala: {status}"
            )

        else:

            await query.edit_message_text(
                "❌ Ati amma hin galmoofne.\n\n"
                "Mee jalqaba Galmaa'i."
            )

    # ================= NEWS =================

    elif query.data == "news":

        await query.edit_message_text(
            "📢 BIRE ONLINE IKUB\n\n"
            "Beeksisni yeroo ammaa hin jiru.\n\n"
            "Beeksisni haaraan yeroo dhihoo keessatti ni maxxanfama."
        )

    # ================= CONTACT =================

    elif query.data == "contact":

        await query.edit_message_text(
            "📞 NU QUNNAMAA\n\n"
            "🤖 Telegram: @bire1bot"
        )

    # ================= HELP =================

    elif query.data == "help":

        await query.edit_message_text(
            "❓ GARGAARSA\n\n"
            "Rakkoo yoo qabaatte admin qunnami.\n\n"
            "Jalqabuuf /start fayyadami."
        )

    # ================= APPROVE =================

    elif query.data.startswith("approve_"):

        user_id = query.data.split("_")[1]

        if str(user_id) in members:

            members[str(user_id)]["approved"] = True
            save_members(members)

            await query.edit_message_text(
                "✅ Kaffaltiin miseensaa mirkanaa'e."
            )

            await context.bot.send_message(
                chat_id=int(user_id),
                text="🎉 Baga gammaddan! Kaffaltiin keessan mirkanaa'eera."
            )

    # ================= REJECT =================

    elif query.data.startswith("reject_"):

        user_id = query.data.split("_")[1]

        await query.edit_message_text(
            "❌ Kaffaltiin didame."
        )

        await context.bot.send_message(
            chat_id=int(user_id),
            text="❌ Receipt keessan hin fudhatamne. Mee irra deebi'aa ergaa."
        )
