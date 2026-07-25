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
# ================= BUTTONS =================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "register":
        context.user_data["step"] = "name"

        await query.edit_message_text(
            "📝 Maqaa kee barreessi:"
        )

    elif query.data.startswith("approve_"):

        user_id = query.data.split("_")[1]

        if str(user_id) in members:
            members[str(user_id)]["approved"] = True
            save_members(members)

            await query.edit_message_text(
                "✅ Miseensummaan mirkanaa'e."
            )

            await context.bot.send_message(
                chat_id=int(user_id),
                text="🎉 Kaffaltiin kee mirkanaa'e. Baga miseensa taate!"
            )

    elif query.data.startswith("reject_"):

        user_id = query.data.split("_")[1]

        await query.edit_message_text(
            "❌ Kaffaltiin didame."
        )

        await context.bot.send_message(
            chat_id=int(user_id),
            text="❌ Ragaan kaffaltii kee hin fudhatamne."
        )


# ================= REGISTRATION =================

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    step = context.user_data.get("step")

    if step == "name":

        context.user_data["name"] = update.message.text
        context.user_data["step"] = "phone"

        await update.message.reply_text(
            "📱 Lakkoofsa bilbila kee barreessi:"
        )

    elif step == "phone":

        context.user_data["phone"] = update.message.text
        context.user_data["step"] = "payment"

        await update.message.reply_text(
            f"💳 Kaffaltii: {PAYMENT_AMOUNT} ETB\n\n"
            f"Telebirr: {TELEBIRR}\n"
            f"CBE: {CBE}\n\n"
            "Erga kaffalte booda screenshot receipt ergi."
        )


# ================= RECEIPT =================

async def receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if context.user_data.get("step") != "payment":
        return

    user_id = update.message.chat_id

    members[str(user_id)] = {
        "name": context.user_data.get("name"),
        "phone": context.user_data.get("phone"),
        "approved": False
    }

    save_members(members)

    keyboard = [[
        InlineKeyboardButton(
            "✅ Approve",
            callback_data=f"approve_{user_id}"
        ),
        InlineKeyboardButton(
            "❌ Reject",
            callback_data=f"reject_{user_id}"
        )
    ]]

    await update.message.reply_text(
        "✅ Receipt kee adminitti ergameera. Mee eegi."
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"💰 Kaffaltii Haaraa\n\n"
            f"🆔 ID: {user_id}\n"
            f"👤 Maqaa: {members[str(user_id)]['name']}\n"
            f"📱 Bilbila: {members[str(user_id)]['phone']}"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    await update.message.forward(ADMIN_ID)
