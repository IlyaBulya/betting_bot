import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_USERNAME = "@bettinghumor"  # 👈 твой канал

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🔓 Посмотреть контент", callback_data="check")]
    ]
    update.message.reply_text("Привет! Нажми кнопку, чтобы получить доступ к контенту:", reply_markup=InlineKeyboardMarkup(keyboard))

def check_subscription(update: Update, context: CallbackContext):
    user_id = update.callback_query.from_user.id
    chat_id = update.effective_chat.id

    try:
        member = context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            context.bot.send_message(chat_id=chat_id, text="✅ Спасибо за подписку! Вот секретный контент:\n\n👉 [Скрытый текст или ссылка]", parse_mode="HTML")
        else:
            raise Exception("Not subscribed")
    except Exception as e:
        context.bot.send_message(
            chat_id=chat_id,
            text="❗ Чтобы получить доступ, подпишитесь на канал:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔗 Перейти к каналу", url="https://t.me/bettinghumor")]
            ])
        )

def main():
    print("Бот запущен.")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(check_subscription, pattern="check"))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
