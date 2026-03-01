from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext, ConversationHandler

from bot.config.constants import RegistrationStates
from bot.database import DB


def ask_name(update: Update, context: CallbackContext):
    update.message.reply_text("Ismingizni yozing...")
    return RegistrationStates.SET_NAME


def set_name(update: Update, context: CallbackContext):
    context.user_data["name"] = update.message.text

    update.message.reply_text(
        "Telefon raqamingizni yuboring",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("Telefon raqam", request_contact=True)]],
            resize_keyboard=True,
        ),
    )
    return RegistrationStates.SET_PHONE


def set_phone(update: Update, context: CallbackContext):
    context.user_data["phone"] = update.message.contact.phone_number

    update.message.reply_text(
        "Lokatsiya yuboring",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("Lokatsiya", request_location=True)]],
            resize_keyboard=True,
        ),
    )
    return RegistrationStates.SET_LOCATION


def set_location(update: Update, context: CallbackContext):
    context.user_data["location"] = update.message.location

    data = context.user_data
    update.message.reply_text(
        f"Ism: {data['name']}\nTelefon: {data['phone']}",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("Tasdiqlash"), KeyboardButton("Qayta boshlash")]],
            resize_keyboard=True,
        ),
    )
    return RegistrationStates.CONFIRM


def register(update: Update, context: CallbackContext):
    if update.message.text != "Tasdiqlash":
        context.user_data.clear()
        update.message.reply_text("Qayta boshlaymiz")
        return RegistrationStates.SET_NAME

    data = context.user_data

    db = DB()
    user_id = db.add_user(data["name"], data["phone"])
    db.add_location(
        user_id,
        data["location"].latitude,
        data["location"].longitude,
    )
    db.close()

    update.message.reply_text("Siz muvaffaqiyatli ro‘yxatdan o‘tdingiz ✅")
    return ConversationHandler.END