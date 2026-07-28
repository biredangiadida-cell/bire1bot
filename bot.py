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
    )# ================= BUTTONS =================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()


    if query.data == "courses":

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
            "📤 Kaffaltii booda receipt kee ergi."
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
        )


    elif query.data == "contact":

        await query.edit_message_text(
            "📞 Nu Qunnamaa\n\n"
            "Bilbila: 0982485937"
        )


    elif query.data == "help":

        await query.edit_message_text(
            "❓ Gargaarsa\n\n"
            "Rakkoo yoo qabaatte nu qunnami."
        )


    elif query.data == "news":

        await query.edit_message_text(
            "📢 Beeksisa\n\n"
            "Beeksisni haaraan as irratti maxxanfama."
        )


    elif query.data == "account":

        user_id = str(query.from_user.id)

        if user_id in members:
            user = members[user_id]

            await query.edit_message_text(
                "👤 Account Koo\n\n"
                f"📝 Maqaa: {user['name']}\n"
                f"📱 Bilbila: {user['phone']}\n"
                f"✅ Haala: {'Mirkanaaʼeera' if user['approved'] else 'Hin mirkanoofne'}"
            )

        else:

            await query.edit_message_text(
                "👤 Account hin jiru.\n"
                "Mee dura galmaa'i."
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


# ================= START REGISTRATION =================

async def start_register(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["step"] = "name"

    await update.callback_query.edit_message_text(
        "📝 Maqaa guutuu kee barreessi:"
    )
