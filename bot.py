import asyncio
from aiogram import Bot, Dispatcher

from handlers import (messages, start, send_photo)
from data.database import DB_Users

from config_reader import config
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode

bot = Bot(config.bot_token.get_secret_value() , default = DefaultBotProperties(parse_mode=ParseMode.HTML))

async def main(bot):
    dp = Dispatcher()

    await DB_Users.create_table_users()

    #добавляю себя в качестве перманентного админа и юзера
    await DB_Users.add_admin(config.admin_id.get_secret_value(), "главный админ", "главный админ")
    await DB_Users.add_user(config.admin_id.get_secret_value(), "Yarik")

    dp.include_routers(
        start.router,
        send_photo.router,
        messages.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    
if __name__ == "__main__":
    print("ready to work..")
    asyncio.run(main(bot))
