from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext


def start_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Assalomu alaykum, ro‘yxatdan o‘ting",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("Ro‘yxatdan o‘tish")]],
            resize_keyboard=True,
        ),
    )