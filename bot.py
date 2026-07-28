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

BOT_TOKEN = "8665819961:AAGMdh4iPagsM60nSBpjqX2n-rauoKvz1Bo"


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



    # ================= RECEIPT =================

async def receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["step"] = "receipt"

await update.callback_query.edit_message_text(
    "📤 Mee receipt kaffaltii kee as ergi."
)


    user_id = update.message.chat_id


    keyboard = [
        [
            InlineKeyboardButton(
                "✅ Approve",
                callback_data=f"approve_{user_id}"
            ),
            InlineKeyboardButton(
                "❌ Reject",
                callback_data=f"reject_{user_id}"
            )
        ]
    ]


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
    )# ================= MAIN =================

def main():

    app = Application.builder().token(BOT_TOKEN).build()


    # Commands
    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("users", users)
    )

    app.add_handler(
        CommandHandler("stats", stats)
    )

    app.add_handler(
        CommandHandler("broadcast", broadcast)
    )


    # Buttons
    app.add_handler(
        CallbackQueryHandler(
            start_register,
            pattern="^register$"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            buttons
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            approve,
            pattern="^(approve_|reject_)"
        )
    )


   # Messages
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_handler
        )app.add_handler(
    MessageHandler(
        filters.PHOTO,
        receipt_handler
    )
)
    )

    # Buttons
    app.add_handler(
        CallbackQueryHandler(buttons)
    )

    # Admin approve/reject
    app.add_handler(
        CallbackQueryHandler(
            approve,
            pattern="^(approve_|reject_)"
        )
    )

    print("✅ ELBS Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()
