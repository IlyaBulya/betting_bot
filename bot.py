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
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    InlineQueryHandler,
)
from telegram.constants import ParseMode
from config import TELEGRAM_BOT_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔓 Посмотреть прогноз", callback_data='show_forecast')]
    ])


async def start_command_handler(update: Update, _: CallbackContext) -> None:
    await update.message.reply_text(
        'Привет! Используй меня через inline-режим в канале, чтобы публиковать прогнозы.'
    )


async def button_handler(update: Update, _: CallbackContext) -> None:
    query = update.callback_query

    forecast_text = (
        "📊 Прогноз:\n"
        "🏒 Локомотив ТМ 4.5 (1.85)\n"
        "🍁 Торонто ТБ 2.5 (1.90)\n"
        "🇪🇸 Жирона ТМ 2.5 (1.65)\n"
        "💰 Общий коэф: 5.80"
    )

    await query.answer(text=forecast_text, show_alert=True)


async def inline_query_handler(update: Update, _: CallbackContext) -> None:
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


def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command_handler))
    application.add_handler(InlineQueryHandler(inline_query_handler))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Бот запущен")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
