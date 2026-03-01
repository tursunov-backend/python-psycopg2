from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

from bot.config import settings
from bot.handlers.start import start_command
from bot.handlers.commands import (
    ask_name,
    set_name,
    set_phone,
    set_location,
    register,
)
from bot.config.constants import RegistrationStates


def main() -> None:
    updater = Updater(settings.BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    conv = ConversationHandler(
        entry_points=[MessageHandler(Filters.text("Ro‘yxatdan o‘tish"), ask_name)],
        states={
            RegistrationStates.SET_NAME: [
                MessageHandler(Filters.text & ~Filters.command, set_name)
            ],
            RegistrationStates.SET_PHONE: [
                MessageHandler(Filters.contact, set_phone)
            ],
            RegistrationStates.SET_LOCATION: [
                MessageHandler(Filters.location, set_location)
            ],
            RegistrationStates.CONFIRM: [
                MessageHandler(Filters.text, register)
            ],
        },
        fallbacks=[],
    )

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(conv)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()