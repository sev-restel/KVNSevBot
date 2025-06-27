import aiosqlite
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
    
    async def select_name(self, id, table = "users"):
        async with aiosqlite.connect(self.db_file) as conn:
            sql = await conn.cursor()

            await sql.execute(f"SELECT name FROM {table} WHERE tg_id={id}")
            data = await sql.fetchall()
            return data[0][0]
    
    async def get_all_users(self):
        async with aiosqlite.connect(self.db_file) as conn:
            cursor = await conn.cursor()
            
            await cursor.execute("SELECT tg_id, name FROM users")
            users = await cursor.fetchall()
            
            return [user for user in users]


DB_Users = DataBaseUsers(config.path_users.get_secret_value())



        
    
        
    


        
    