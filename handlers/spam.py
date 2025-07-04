from datetime import datetime, time
from data.database import DB_Users, DB_Notification
import asyncio

async def scheduled_mailing(bot):    
    while True:
        now = datetime.now()
        now = now.replace(second=0, microsecond=0)
        
        notif_time_list = await DB_Notification.get_all_active_notification()
        
        for notif_data in notif_time_list:
            target_time = datetime.strptime(notif_data[2], "%Y-%m-%d %H:%M")
            
            if now == target_time:
                await send_notif(bot, notif_data)
                await DB_Notification.update_cell_notif(notif_data[0], "is_active", 0)
                #await asyncio.sleep(60)  # avoid repeat
            
        await asyncio.sleep(10)


async def send_notif(bot, notif_data):
    users = await DB_Users.get_all_users()
    for user in users:
        try:
            if notif_data[4]:
                await bot.send_photo(
                    chat_id=user[0],
                    photo=notif_data[4],
                    caption=notif_data[1]
                )
            else:
                await bot.send_message(
                    chat_id=user[0],
                    text=notif_data[1]
                )
            await asyncio.sleep(0.1)
        except Exception as e:
            print(f"[send_wave] Ошибка при отправке пользователю {user[0]}: {e}")