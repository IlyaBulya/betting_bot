import os
from telegram import (
    Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    Updater, CommandHandler, CallbackQueryHandler, CallbackContext
)

# Настройки
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Render использует переменные окружения
CHANNEL_USERNAME = "@bettinghumour"        # 👈 замени на свой @канал
IMAGE_PATH = "Screenshot 2025-05-05 at 16.17.04.png"               # 👈 имя файла прогноза
FORECAST_TEXT = "🏒 Локо:CЮ ТМ 4.5\n🍁 Торонто Инд Тотал ТБ 2.5\n🇪🇸 Жирона:Мальорка ТМ 2.5\n💰 Коэф: 5.80"

# Команда /post публикует сообщение в канал с кнопкой
def post(update: Update, context: CallbackContext):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔓 Посмотреть прогноз", callback_data="show_forecast")]
    ])
    with open(IMAGE_PATH, 'rb') as photo:
        context.bot.send_photo(
            chat_id=CHANNEL_USERNAME,
            photo=photo,
            caption="🎯 Прогноз дня на 05.05.2025",
            reply_markup=keyboard
        )
    update.message.reply_text("✅ Пост опубликован в канал.")

# Обработка нажатия кнопки — alert
def on_button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "show_forecast":
        query.answer(FORECAST_TEXT, show_alert=True)

# Основной запуск
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("post", post))
    dp.add_handler(CallbackQueryHandler(on_button_click))

    print("✅ Бот запущен")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
