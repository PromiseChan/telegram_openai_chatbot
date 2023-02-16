#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import __version__ as TG_VER
import requests
import json
import ssl
import os

# DISABLE SSL CERTIFICATE VERIFICATION
ssl._create_default_https_context = ssl._create_unverified_context

# ### OPENAIL API INFO ####
OPENAI_DOMAIN = "https://api.openai.com"
OPENAI_CHAT_MODEL = "text-davinci-003"
CHAT_API_KEY = os.getenv("CHAT_API_KEY")

TEMPERATURE = 0.5
MAX_TOKENS = 1024
TOP_P = 1
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
STOP_WORDS = "None"
# ### OPENAIL API INFO ####


# ### TELEGRAM BOT INFO ####
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# ### TELEGRAM BOT INFO ####


try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

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
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def weekly_report_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """generate weekly report """
    user_msg = "请帮我把以下的工作内容填充为一篇完整的周报,用 markdown 格式以分点叙述的形式输出:"
    user_msg += update.message.text
    reply_meg = get_from_openai_chat(user_msg, CHAT_API_KEY)
    await update.message.reply_text(reply_meg)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    user_msg = update.message.text
    try:
        reply_msg = get_from_openai_chat(user_msg, CHAT_API_KEY)
    except Exception as e:
        reply_msg = "Sorry, I am not able to understand you. Please try again."
        logger.error(e)
    await update.message.reply_text(reply_msg)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder()\
        .token(token=TELEGRAM_BOT_TOKEN)\
        .build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    # add weekly-report command
    application.add_handler(CommandHandler("report", weekly_report_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


# chat from openai response
def get_from_openai_chat(prompt, api_key):
    url = OPENAI_DOMAIN + "/v1/completions"
    payload = json.dumps({
        "model": OPENAI_CHAT_MODEL,
        "prompt": prompt,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "top_p": TOP_P,
        "frequency_penalty": FREQUENCY_PENALTY,
        "presence_penalty": PRESENCE_PENALTY,
        "stop": STOP_WORDS
    })
    headers = {
        'Authorization': 'Bearer ' + api_key,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    content = json.loads(response.text)
    return content['choices'][0]['text']


if __name__ == "__main__":
    main()

