from telegram.ext import Updater

import config.secrets

updater = Updater(token=config.secrets.TELEGRAM_TOKEN)
dispatcher = updater.dispatcher