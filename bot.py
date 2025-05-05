from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import config

def post(update: Update, context: CallbackContext):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔓 Посмотреть прогноз", callback_data="show_forecast")]
    ])

    with open(config.IMAGE_PATH, 'rb') as photo:
        context.bot.send_photo(
            chat_id=config.CHANNEL_USERNAME,
            photo=photo,
            caption="🎯 Прогноз дня на 05.05.2025",
            reply_markup=keyboard
        )

    update.message.reply_text("✅ Пост опубликован в канал.")

def on_button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "show_forecast":
        query.answer(text=config.FORECAST_TEXT, show_alert=True)

def main():
    updater = Updater(config.BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("post", post))
    dp.add_handler(CallbackQueryHandler(on_button_click))

    print("✅ Бот запущен.")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
