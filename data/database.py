import aiosqlite
import uuid
from config_reader import config


#юзерская бд
class DataBaseUsers:
    def __init__(self, db_file):
        self.db_file = db_file

    #создание листов бд - юзеров
    async def create_table_users(self):
        async with aiosqlite.connect(self.db_file) as conn:
            sql = await conn.cursor()

            #добавить значение дл использованных цитат
            await sql.executescript(f"""CREATE TABLE IF NOT EXISTS users (
                tg_id INT UNIQUE,
                name TEXT,
                us_name TEXT,                
                count INT)""")
            
            await sql.executescript(f"""CREATE TABLE IF NOT EXISTS admins (
                tg_id INT UNIQUE,
                tg_name TEXT,
                tg_user_name TEXT)""")

            await conn.commit()
    
    async def update_cell(self, tg_user_id: int, col: str, value: str, table: str = "users"):
        async with aiosqlite.connect(self.db_file) as conn:
            sql = await conn.cursor()

            await sql.execute(f"""UPDATE {table} 
                              SET {col} = ? 
                              WHERE tg_id = ?""", 
                              (value, tg_user_id))
            await conn.commit()
    
    async def select_cell(self, tg_user_id: int, col: str, table: str = "users"):
        async with aiosqlite.connect(self.db_file) as conn:
            sql = await conn.cursor()

            await sql.execute(f"""SELECT {col} 
                              FROM {table}
                              WHERE tg_id = ?""", 
                              (tg_user_id,))
            
            data = await sql.fetchone()
            return data[0]
    
    async def add_user(self, tg_user_id, name, us_name, count = 0):
        async with aiosqlite.connect(self.db_file) as conn:
            sql = await conn.cursor()

            await sql.execute("""INSERT OR REPLACE INTO users (
                    tg_id,
                    name,
                    us_name,
                    count) 
                    VALUES (?, ?, ?, ?)""",
                    (tg_user_id, name, us_name, count))
            await conn.commit()
    
    async def select_user(self, id, table = "users"):
        async with aiosqlite.connect(self.db_file) as conn:
            sql = await conn.cursor()

            await sql.execute(f"SELECT tg_id, name, us_name, count FROM {table} WHERE tg_id=?", 
                              (id,))

            data = await sql.fetchall()
            return data[0]
    
    async def get_all_users(self):
        async with aiosqlite.connect(self.db_file) as conn:
            cursor = await conn.cursor()
            
            await cursor.execute("SELECT tg_id, name FROM users")
            users = await cursor.fetchall()
            
            return users
            # return [user for user in users]
    
    
    #админские функции
    
    
    async def is_admin(self, tg_admin_id):
        async with aiosqlite.connect(self.db_file) as conn:
            sql = await conn.cursor()

            await sql.execute(f"SELECT tg_id FROM admins WHERE tg_id={tg_admin_id} ")
            zxc = await sql.fetchall()
            return (1 if len(zxc)==1 else 0)
     
    async def add_admin(self, tg_admin_id, name, user_name):
        async with aiosqlite.connect(self.db_file) as conn:
            sql = await conn.cursor()

            await sql.execute("""INSERT OR IGNORE INTO admins (
                    tg_id,
                    tg_name,
                    tg_user_name) 
                    VALUES (?, ?, ?)""",
                    (tg_admin_id, name, user_name))
            await conn.commit()
    
    async def select_admin(self, id, table = "admins"):
        async with aiosqlite.connect(self.db_file) as conn:
            sql = await conn.cursor()

            await sql.execute(f"SELECT tg_id, tg_name, tg_user_name FROM {table} WHERE tg_id=?", 
                              (id,))

            data = await sql.fetchall()
            return data[0]
    
    async def admins_list(self, table = "admins"):
        async with aiosqlite.connect(self.db_file) as conn:
            sql = await conn.cursor()

            await sql.execute(f"SELECT tg_id, tg_name, tg_user_name FROM {table} ")
            
            return await sql.fetchall()
    
    async def delete_admin(self, tg_admin_id):
        async with aiosqlite.connect(self.db_file) as conn:
            sql = await conn.cursor()

            await sql.execute(f"DELETE FROM admins WHERE tg_id=?", (tg_admin_id,))
            await conn.commit()


#новая бд для уведомлений и рассылки
class DataBaseNotification:
    def __init__(self, db_file):
        self.db_file = db_file
    
    #создание листа бд
    async def create_table_notification(self):
        async with aiosqlite.connect(self.db_file) as conn:
            sql = await conn.cursor()

            await sql.executescript(f"""CREATE TABLE IF NOT EXISTS notification (
                id_notif INT UNIQUE,
                text TEXT,
                date TEXT,
                period TEXT,                
                is_active BOOL,
                photo BLOB)""")

            await conn.commit()
    
    async def add_notification(self, id_notif: int, text: str, date: str, is_active: bool = True, photo: str = None, period: str = None):
        async with aiosqlite.connect(self.db_file) as conn:
            sql = await conn.cursor()

            await sql.execute("""INSERT OR REPLACE INTO notification (
                    id_notif,
                    text,
                    date,
                    is_active,
                    photo,
                    period) 
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (id_notif, text, date, is_active, photo, period))
            await conn.commit()
    
    async def is_id_exists(self, id_notif: int) -> bool:
        async with aiosqlite.connect(self.db_file) as conn:
            sql = await conn.cursor()
            
            await sql.execute("SELECT EXISTS(SELECT 1 FROM notification WHERE id_notif = ?)", (id_notif,))
            
            data = await sql.fetchone()
            #await sql.close()
            return data[0] == 1
    
    async def get_all_date(self, id_notif, table = "notification"):
        async with aiosqlite.connect(self.db_file) as conn:
            sql = await conn.cursor()

            await sql.execute(f"SELECT id_notif, text, date, period, is_active, photo FROM {table} WHERE id=?", (id_notif,))
            data = await sql.fetchone()
            
            return data
    
    async def get_all_notification(self):
        async with aiosqlite.connect(self.db_file) as conn:
            sql = await conn.cursor()
            
            #DESC -> ASC
            await sql.execute("SELECT id_notif, text, date, is_active, photo FROM notification WHERE is_active=1 ORDER BY date ASC")
            data = await sql.fetchall()
            await sql.execute("SELECT id_notif, text, date, is_active, photo FROM notification WHERE is_active=0 ORDER BY date ASC")
            data += await sql.fetchall()
            return data
    
    async def get_all_active_notification(self):
        async with aiosqlite.connect(self.db_file) as conn:
            sql = await conn.cursor()
            
            #DESC -> ASC
            await sql.execute("SELECT id_notif, text, date, is_active, photo FROM notification WHERE is_active=1 ORDER BY date ASC")
            data = await sql.fetchall()
            
            return data
    
    async def update_cell_notif(self, id_notif: int, col: str, value, table: str = "notification"):
        async with aiosqlite.connect(self.db_file) as conn:
            sql = await conn.cursor()

            await sql.execute(f"""UPDATE {table} 
                              SET {col} = ? 
                              WHERE id_notif = ?""", 
                              (value, id_notif))
            await conn.commit()



DB_Users = DataBaseUsers(config.path_users.get_secret_value())
DB_Notification = DataBaseNotification(config.path_notification.get_secret_value())
