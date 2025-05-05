import logging
from uuid import uuid4
from typing import List

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Update,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    InlineQueryHandler,
    CommandHandler,
    CallbackContext,
)
from telegram.constants import ParseMode

from config import TELEGRAM_BOT_TOKEN, CHANNEL_USERNAME

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔓 Посмотреть прогноз", callback_data="show_forecast")]
    ])


async def start_command(update: Update, context: CallbackContext):
    await update.message.reply_text("Привет! Используй меня через inline-режим в канале.")


async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id

    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)

        if member.status in ["member", "administrator", "creator"]:
            forecast_text = (
                "📊 Прогноз:\n"
                "🏒 Локо ТМ 4.5 (1.85)\n"
                "🍁 Торонто ТБ 2.5 (1.90)\n"
                "🇪🇸 Жирона ТМ 2.5 (1.65)\n"
                "💰 Общий коэф: 5.80"
            )
            await query.answer(forecast_text, show_alert=True)
        else:
            await query.answer("❗ Чтобы получить прогноз, подпишитесь на канал", show_alert=True)

    except Exception as e:
        logger.error(f"Ошибка проверки подписки: {e}")
        await query.answer("⚠ Не удалось проверить подписку. Попробуйте позже.", show_alert=True)


async def inline_query_handler(update: Update, context: CallbackContext):
    if not update.inline_query.query:
        return

    results: List[InlineQueryResultArticle] = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="📈 Опубликовать прогноз",
            input_message_content=InputTextMessageContent(
                message_text="🎯 Нажмите кнопку ниже, чтобы узнать прогноз",
                parse_mode=ParseMode.HTML,
            ),
            reply_markup=get_keyboard(),
        ),
    ]

    await update.inline_query.answer(results)


def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(InlineQueryHandler(inline_query_handler))

    print("✅ Бот запущен")
    application.run_polling()


if __name__ == "__main__":
    main()
