from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import os

TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_USERNAME = "@yourchannel"  # замените на ваш канал

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Посмотреть контент", callback_data="check")]
    ]
    update.message.reply_text("Нажмите, чтобы получить доступ:", reply_markup=InlineKeyboardMarkup(keyboard))

def check_subscription(update: Update, context: CallbackContext):
    user_id = update.callback_query.from_user.id
    chat_member = context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)

    if chat_member.status in ["member", "administrator", "creator"]:
        context.bot.send_message(chat_id=update.effective_chat.id, text="✅ Спасибо за подписку! Вот ваш контент: <секретный текст>")
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❌ Пожалуйста, подпишитесь на канал, чтобы продолжить.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Подписаться", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")]
            ])
        )

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(check_subscription, pattern="check"))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
