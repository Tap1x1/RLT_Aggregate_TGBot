import logging
from aiogram import executor
from config import BOT_TOKEN
from telegram_bot import TelegramBot

def main():
    try:
        tg_bot = TelegramBot(BOT_TOKEN)

        tg_bot.run()
    except Exception as ex:
        logging.exception(ex)


if __name__ == "__main__":
    main()
