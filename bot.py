#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
The project is based of https://habr.com/ru/post/341678/
This bot is based of https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/echobot.py (using python-telegram-bot)

my_homepc surveillance monitor telegram bot  

This bot is meant as a part of an exercise pet project that performs functions of a home monitor.
The project goal is to use an old notebook repurposed as an experimental debian bullseye server
to utilise https://motion-project.github.io/ to setup automatic webcam capture and motion detection
for no hassle "video monitoring" of some area e.g. my studio appartment.
python-telegram-bot.org is used to build telegram bot, that will be acting as a remote front end and
will run on an experimental debian bullseye server.

Known bugs:
ver 0.0
no authentication

Usage:
ver 0.0
/start - activate bot 
/snapshot - send last snapshot made by the debianpc webcam 
/help - send help message detailing available commands
"""

import logging

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import custom_config

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text("homewebcamssurveillance_9581_bot start()")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Usage:\n" \
                                    "/snapshot - send last snapshot made by the debianpc webcam\n" \
                                    "/help - send this message")

async def last_snapshot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_photo(open(custom_config.current_photo, 'rb'))

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5356737695:AAH6oul0w4An3wp-tyq9QQP2Qw1Tte-F89c").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("snapshot", last_snapshot))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
