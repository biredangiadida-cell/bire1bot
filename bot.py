from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

TOKEN = "8665819961:AAH1RHRR-wY8i5k7EnVe62-cbmR5KqzCSyQ"
ADMIN_ID = 123456789  # Telegram ID kee as galchi

users = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("📝 Galmaa'i", callback_data="register")],
        [InlineKeyboardButton("💳 Kaffaltii", callback_data="payment")],
        [InlineKeyboardButton("👤 Account Koo", callback_data="account")],
        [InlineKeyboardButton("📞 Nu Qunnamaa", callback_data="contact")]
    ]

    await update.message.reply_text(
        "🎉 Baga Nagaan Gara *BIRE ONLINE IKUB* dhuftan!\n\n"
        "👇 Tajaajila barbaaddu filadhu.",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "register":
        context.user_data["step"] = "name"
        await query.edit_message_text(
            "📝 Maqaa kee barreessi."
        )

    elif query.data == "payment":
        await query.edit_message_text(
            "💳 Kaffaltii:\n\n"
            "Telebirr: 0982485937\n"
            "CBE: 1000291766734"
        )

    elif query.data == "account":
        await query.edit_message_text(
            "👤 Account kee yeroo dhihootti ni jiraata."
        )

    elif query.data == "contact":
        await query.edit_message_text(
            "📞 Telegram: @bireikub"
        )


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    step = context.user_data.get("step")

    if step == "name":

        context.user_data["name"] = update.message.text
        context.user_data["step"] = "phone"

        await update.message.reply_text(
            "📱 Lakkoofsa bilbila kee barreessi."
        )


    elif step == "phone":

        name = context.user_data["name"]
        phone = update.message.text

        users[update.message.chat_id] = {
            "name": name,
            "phone": phone
        }

        await update.message.reply_text(
            "✅ Galmeen kee milkaa'inaan xumurame!\n\n"
            f"👤 Maqaa: {name}\n"
            f"📱 Bilbila: {phone}"
        )

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                "🔔 Galmee Haaraa!\n\n"
                f"👤 Maqaa: {name}\n"
                f"📱 Bilbila: {phone}"
            )
        )

        context.user_data["step"] = None


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler)
)

print("🤖 BIRE ONLINE IKUB Bot Started...")

app.run_polling()
