import json
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from datetime import datetime
from database import Database
from config import DATABASE_URI, DATABASE_NAME, COLLECTION_NAME


class TelegramBot:

    def __init__(self, bot_token):
        self._bot = Bot(token=bot_token)
        self._dp = Dispatcher(self._bot)
        self._dp.middleware.setup(LoggingMiddleware())
        self._database = Database(DATABASE_NAME, DATABASE_URI, COLLECTION_NAME)

    async def on_start(self, message: types.Message):
        await message.answer("Hello! To get started, send parameters in JSON format.",
                                parse_mode="MarkdownV2")

    async def on_handle_aggregate(self, message: types.Message):
        input_text = message.text
        try:
            json_data = json.loads(input_text)
        except Exception as e:
            print(f"Error: {e}")
            await message.answer("Error in JSON format. Please use the correct JSON format.")
            return

        if "dt_from" not in json_data or "dt_upto" not in json_data or "group_type" not in json_data:
            await message.answer("Missing required parameters (dt_from, dt_upto, group_type) in JSON.")
            return

        dt_from = json_data["dt_from"]
        dt_upto = json_data["dt_upto"]
        group_type = json_data["group_type"]

        try:
            start_date = datetime.fromisoformat(dt_from)
            end_date = datetime.fromisoformat(dt_upto)
        except ValueError:
            await message.answer("Error in date format. Please use ISO format (e.g., 2022-09-01T00:00:00).")
            return

        result = json.dumps(
           self._database.aggregate_data(start_date, end_date, group_type), indent=2
        )

        await message.reply(
            result,
           
        )

    def run(self):
        self._dp.register_message_handler(self.on_start, commands=['start','help'])
        self._dp.register_message_handler(self.on_handle_aggregate, lambda message: message.text.startswith('{'))

        from aiogram import executor
        executor.start_polling(self._dp, skip_updates=True)
