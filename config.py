from aiogram import Bot

from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode

from config_reader import config

bot = Bot(config.bot_token.get_secret_value() , default = DefaultBotProperties(parse_mode=ParseMode.HTML))