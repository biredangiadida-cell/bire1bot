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
        )# ================= RECEIPT =================

async def receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if context.user_data.get("step") != "payment":
        return

    user_id = update.message.chat_id

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
        "✅ Receipt kee fudhanneerra.\n"
        "Mee admin irraa mirkaneessa eegi."
    )

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=update.message.photo[-1].file_id,
        caption=(
            "💳 Kaffaltii Haaraa\n\n"
            f"👤 Maqaa: {members[str(user_id)]['name']}\n"
            f"📱 Bilbila: {members[str(user_id)]['phone']}\n"
            f"🆔 ID: {user_id}"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================= APPROVE / REJECT =================

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.data.split("_")[1]

    if query.data.startswith("approve_"):

        members[user_id]["approved"] = True
        save_members(members)

        await context.bot.send_message(
            chat_id=int(user_id),
            text="🎉 Baga gammaddan! Galmeen keessan mirkanaa'eera."
        )

        await query.edit_message_caption(
            caption="✅ Galmeen kun APPROVED ta'eera."
        )

    elif query.data.startswith("reject_"):

        await context.bot.send_message(
            chat_id=int(user_id),
            text="❌ Galmeen keessan hin mirkanoofne. Mee receipt sirrii ergaa."
        )

        await query.edit_message_caption(
            caption="❌ Galmeen kun REJECTED ta'eera."
        )# ================= ADMIN =================

async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text(
        f"👥 Members: {len(members)}"
    )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    approved = sum(
        1 for m in members.values()
        if m.get("approved")
    )

    await update.message.reply_text(
        f"📊 Statistics\n\n"
        f"👥 Total: {len(members)}\n"
        f"✅ Approved: {approved}"
    )


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text(
            "Fayyadami:\n/broadcast Ergaa kee"
        )
        return

    text = " ".join(context.args)

    sent = 0

    for uid in members:
        try:
            await context.bot.send_message(
                chat_id=int(uid),
                text=text
            )
            sent += 1
        except:
            pass

    await update.message.reply_text(
        f"✅ Ergaan namoota {sent} bira gahe."
    )


# ================= MAIN =================

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("users", users))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("broadcast", broadcast))

    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(CallbackQueryHandler(approve, pattern="^(approve_|reject_)"))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    app.add_handler(MessageHandler(filters.PHOTO, receipt))

    app.post_init = set_commands

    print("✅ ELBS Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()
