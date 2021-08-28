#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from textmodifier import TextModifier
from yttomp3 import YTToMP3

# Enable logging
logging.basicConfig(filename="awesome_bot.log", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    commands = '''
/ladder SOME MESSAGE (Shows the message in a "ladder" form)
/emojify SOME MESSAGE (Shows the message in emoji form)
/downloadmp3 YouTube URL or song name (Sends a YouTube video in mp3)
    '''
    update.message.reply_text('Hello! These are my commands:\n {}'.format(commands))

def downloadmp3(update, context):
    if(len(context.args) < 1):
        update.message.reply_text("You didn't send any URL or text o.O")
        return False

    query = " ".join(context.args)
    if(len(query) > 150):
        update.message.reply_text("WOW! That's a way too long text, mate :o. The max is 150 letters")
        return False

    yt = YTToMP3(5000000)

    try:
        update.message.reply_text("Sure! I'll try to download it")

        result = yt.downloadmp3(query)

        if(not result):
            update.message.reply_text("Oops! {}".format(yt.error_message))
        else:
            with open(yt.newfiles[0]+".mp3", 'rb') as file:
                update.message.reply_audio(file)
            os.remove(yt.newfiles[0]+".mp3")
    except Exception as e:
        logger.warning('Update "%s" caused error "%s" while downloading mp3', update, e)
        update.message.reply_text("Sorry! Some problem happened here :s")


def ladder(update, context):
    if(len(context.args) < 1):
        update.message.reply_text("You didn't send any text o.O")
        return False

    message = " ".join(context.args)
    if(len(message) > 100):
        update.message.reply_text("WOW! That's a way too long text, mate :o. The max is 100 letters")
    else:
        message = TextModifier.ladder(message)

    update.message.reply_text(message)


def emojify(update,context):
    if(len(context.args) < 1):
        update.message.reply_text("You didn't send any text o.O")
        return False

    message = " ".join(context.args)
    if(len(message) > 20):
        update.message.reply_text("WOW! That's a way too long text, mate :o. The max is 20 letters")
    else:
        message = TextModifier.emojify(message)
        update.message.reply_text(message)


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text("Sorry, I don't get that \""+update.message.text+"\" thing :/")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("HERE_GOES_YOUR_TOKEN", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ladder", ladder))
    dp.add_handler(CommandHandler("emojify", emojify))
    dp.add_handler(CommandHandler("downloadmp3", downloadmp3))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
