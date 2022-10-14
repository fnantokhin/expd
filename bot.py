#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
bot ver 0.21

The project is based of https://habr.com/ru/post/341678/
This bot is based of https://github.com/python-telegram-bot/
python-telegram-bot/blob/master/examples/echobot.py
(using python-telegram-bot)

my_homepc surveillance monitor telegram bot

This bot is meant as a part of an exercise pet project that
performs functions of a home monitor. The project goal is to
use an old notebook repurposed as an experimental debian bullseye
server to utilise https://motion-project.github.io/ to setup
automatic webcam capture and motion detection for no hassle
"video monitoring" of some area e.g. my studio appartment.
python-telegram-bot.org is used to build telegram bot, that will
be acting as a remote front end and will run on an experimental
debian bullseye server.

Usage:
/start
/debug
/help
/update_photo x(int)

Config file:
custom_config.py
"""

import logging

from telegram import Update
from telegram.ext import ApplicationHandlerStop, Application
from telegram.ext import TypeHandler, CommandHandler, ContextTypes

import custom_config

# Enable logging
logging.basicConfig(
    format=(
        "%(asctime)s - %(name)s - %(levelname)s -"
        "%(message)s"), level=logging.INFO
)
logger = logging.getLogger(__name__)


async def auth_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Block every command handler for users that are not authorised"""
    logging.info("callback(), " + str(update.effective_user.id))
    if update.effective_user.id in custom_config.SPECIAL_USERS:
        pass
    else:
        # Print back user id
        await update.message.reply_text(update.effective_user.id)
        # Block further execution
        raise ApplicationHandlerStop


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a simple welcome message."""
    logging.info("start(), " + str(update.effective_message.chat_id))
    await update.message.reply_text("my_homepc surveillance monitor telegram bot")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a detailed information message."""
    logging.info("help_command(), " + str(update.effective_message.chat_id))
    # Display user id
    await update.message.reply_text(
        "USER: " + str(update.effective_message.chat_id))
    # Display active user settings
    update_photo_job_name = "update_photo_for_" + str(update.effective_message.chat_id)
    if job_if_exists(update_photo_job_name, context):
        await update.message.reply_text("auto-sending snapshots ENABLED")
    else:
        await update.message.reply_text("auto-sending snapshots DISABLED\n")
    # Display available commands
    await update.message.reply_text(
        "Usage:\n"
        "/debug - send last snapshot made by the motion "
        "& last motion capture video recorded\n"
        "/help - send this message\n"
        "/update_photo x(int) - every x seconds send"
        "last snapshot made by the motion\n")


async def debug_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send debug information: current snapshot and current
    movement-detection movie (as set in custom_config.py)"""
    logging.info("debug_command(), " + str(update.effective_message.chat_id))
    await update.message.reply_photo(open(custom_config.CURRENT_PHOTO, 'rb'))
    await update.message.reply_video(open(custom_config.CURRENT_VIDEO, 'rb'))


def job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE, remove_job: False) -> bool:
    """Check if job exists. If remove_job is passed as True then
    remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        logging.info("remove_job_if_exists(), " + job.name)
        if remove_job:
            job.schedule_removal()
    return True


async def update_photo(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send current snapshot."""
    logging.info("update_job(), " + str(context.job.chat_id))
    job = context.job
    await context.bot.send_photo(job.chat_id,
                                 photo=open(custom_config.CURRENT_PHOTO, 'rb'))


async def update_photo_set_job(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Enable and set interval to auto-send current snapshot made by
    motion program. No further real-time control is required from user.
    0 or negative will disable feature."""
    logging.info("update_photo_set_job(), " + str(update.effective_message.chat_id))
    chat_id = update.effective_message.chat_id
    new_job_name = "update_photo_for_" + str(chat_id)

    try:
        update_interval = int(context.args[0])
    except Exception:
        await update.message.reply_text("(ERROR) wrong arguments in /update_photo x(int)")
        return

    if update_interval < 1:
        await update.message.reply_text("auto-sending snapshots DISABLED.")
        job_if_exists(new_job_name, context, remove_job=True)
    else:
        await update.message.reply_text(
            "auto-sending snapshots ENABLED.\n"
            "sending snapshot every " +
            str(update_interval) + "s")

        job_if_exists(new_job_name, context, remove_job=True)

        context.job_queue.run_repeating(
            update_photo, update_interval, chat_id=chat_id,
            name=new_job_name, data=update_interval)


def main() -> None:
    """Start the bot."""
    logging.info("main(). starting surveillance bot.")
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(custom_config.BOT_TOKEN).build()

    # before anything else assess if the current user is authorised.
    application.add_handler(TypeHandler(Update, auth_callback), -1)
    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("debug", debug_command))
    application.add_handler(CommandHandler("update_photo", update_photo_set_job))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
