import aiosqlite
import logging
import asyncio

class Database:
    def __init__(self, db_name="db.db"):
        self.db_name = db_name
        self._lock = asyncio.Lock()

    async def connection_db(self):
        """Создает соединение с базой данных"""
        connection = await aiosqlite.connect(self.db_name)
        cursor = await connection.cursor()
        return connection, cursor
    
    async def create_users_table(self):
        """Создает таблицу пользователей - АСИНХРОННЫЙ метод"""
        conn, cursor = await self.connection_db()
        try:
            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER UNIQUE,
                    username TEXT,
                    first_name TEXT,
                    adminRightsLevel INTEGER DEFAULT 0,
                    balance INTEGER DEFAULT 0,
                    respect REAL DEFAULT 0.1,
                    role TEXT,
                    join_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_farm DATETIME CURRENT_TIMESTAMP
                )
            ''')
            await conn.commit()
            logging.info("Таблица users создана или уже существует")
            return "Таблица создана успешно"
        except Exception as e:
            logging.error(f"Ошибка при создании таблицы: {e}")
            raise
        finally:
            await conn.close()
    
    async def create_warns_table(self):
        conn,cursor = await self.connection_db()
        try:
            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS warns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    admin_id INTEGER,
                    reason TEXT,
                    created_at DATATIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            await conn.commit()
            logging.info("Table warns created or be created")
            return "Table warnd successfully created"
        except Exception as e:
            logging.error(f"Ошибка при создании таблицы: {e}")
            raise
        finally:
            await conn.close()



    async def add_user(self, user_id: int, username: str, first_name: str, admLevel: int, role: str):
        """Добавляет пользователя в базу - АСИНХРОННЫЙ метод"""
        conn, cursor = await self.connection_db()
        try:
            await cursor.execute(
                "INSERT OR IGNORE INTO users (user_id, username, first_name, adminRightsLevel,role) VALUES (?, ?, ?, ?,?)",
                (user_id, username, first_name, admLevel,role)
            )
            await conn.commit()
            logging.info(f"Пользователь {user_id} добавлен в базу")
            return "Пользователь добавлен успешно"
        except Exception as e:
            logging.error(f"Ошибка при добавлении пользователя: {e}")
            raise
        finally:
            await conn.close()
    
    async def user_exists(self, user_id: int) -> bool:
        """Проверяет существование пользователя - АСИНХРОННЫЙ метод"""
        conn, cursor = await self.connection_db()
        try:
            await cursor.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
            exists = await cursor.fetchone()
            return exists is not None
        finally:
            await conn.close()
    
    async def is_admin(self, user_id: int) -> bool:
        """Проверяет, является ли пользователь администратором - АСИНХРОННЫЙ метод"""
        conn, cursor = await self.connection_db()
        try:
            await cursor.execute(
                "SELECT 1 FROM users WHERE user_id = ? AND adminRightsLevel >= 1", 
                (user_id,)
            )
            exists = await cursor.fetchone()
            return exists is not None
        finally:
            await conn.close()

    

    async def get_user_info(self, user_id: int) -> dict:
        """Получает информацию о пользователе по ID"""
        conn, cursor = await self.connection_db()
        try:
            await cursor.execute(
                "SELECT user_id, username, first_name, adminRightsLevel, join_date,role,respect FROM users WHERE user_id = ?", 
                (user_id,)
            )
            user_data = await cursor.fetchone()
            
            if user_data:
                return {
                    'user_id': user_data[0],
                    'username': user_data[1],
                    'first_name': user_data[2],
                    'admin_level': user_data[3],
                    'join_date': user_data[4],
                    'role': user_data[5],
                    'respects': user_data[6]
                }
            else:
                return None
        finally:
            await conn.close()

    async def get_system_stats(self):
        conn, cursor = await self.connection_db()
        try:
            await cursor.execute('''
                SELECT 
                    (SELECT COUNT(*) FROM users) as total_users,
                    (SELECT COUNT(*) FROM warns) as total_warns,
                    (SELECT SUM(balance) FROM users) as total_balance
    
            ''')
            result = await cursor.fetchone()
            return {
                'total_users': result[0],
                'total_warns': result[1],
                'total_balance': result[2], 
            }
        finally:
            await conn.close()

    async def add_warn(self, user_id: int, admin_id: int, reason: str):
        conn,cursor = await self.connection_db()
        try:
            await cursor.execute(
                "INSERT INTO warns(user_id,admin_id,reason) VALUES (?, ?, ?)" ,
                (user_id,admin_id,reason)
            )
            await conn.commit()
            return "Варн добавлен в базу данных"
        except Exception as e:
            return (f"Ошибка при добавлении варна{e}")
            raise
        finally:
            await conn.close()
    
    async def get_user_warns(self,user_id: int):
        conn,cursor = await self.connection_db()
        try:
            await cursor.execute(
                "SELECT reason FROM warns WHERE user_id = ?",(user_id,)
            )
            reasons = await cursor.fetchall()
            warns_count = len(reasons)
            return reasons,warns_count
        finally:
            await conn.close()

    async def get_user_balance(self,user_id: int ):
        conn,cursor = await self.connection_db()
        try:
            await cursor.execute(
                "SELECT balance FROM users WHERE user_id = ?",(user_id,)
            )
            balance = await cursor.fetchone()
            if balance:
                return balance[0]
            else:
                return False
        finally:
            await conn.close()
    
    async def update_user_balance(self,user_id: int,balance: int):
        conn,cursor = await self.connection_db()
        try:
            await cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?",(balance,user_id))
            await conn.commit()
            return f"Сonsole: баланс пользователя: {user_id} обновлен"
        finally: 
            await conn.close()

    
            
    async def get_user_role(self,user_id:int) -> str:
        conn,cursor = await self.connection_db()
        try:
            await cursor.execute(
                "SELECT role FROM users WHERE user_id = ?",(user_id,)
            )
            role = await cursor.fetchone()
            if role:
                return role[0]
            else:
                return None
        finally:
            await conn.close()

    async def get_user_respects(self,user_id:int):
        conn,cursor = await self.connection_db()
        try:
            await cursor.execute(
                "SELECT respect FROM users WHERE user_id = ?",(user_id,)
            )
            respects = await cursor.fetchone()
            if respects is not None:
                print(respects[0])
                return respects[0]
            else:
                return False
        finally:
            await conn.close()

    async def get_top_respects(self, limit):
        conn, cursor = await self.connection_db()
        try:
            await cursor.execute('''
                SELECT user_id, username, respect 
                FROM users 
                ORDER BY respect DESC 
                LIMIT ?
            ''', (limit,))
            
            top_users = await cursor.fetchall()
            return top_users  # [(user_id, username, respect), ...]
        finally:
            await conn.close()

    async def set_user_role(self, user_id: int, role: str):
        async with self._lock:  # ⚠️ ГЛОБАЛЬНАЯ БЛОКИРОВКА
            await asyncio.sleep(0.1)
            conn, cursor = await self.connection_db()
            try:
                await cursor.execute(
                    "UPDATE users SET role = ? WHERE user_id = ?",
                    (role, user_id)
                )
                await conn.commit()
            finally:
                await conn.close()

    async def add_user_respect(self,user_id:int, rep_amount:float):
        conn,cursor = await self.connection_db()
        try:
            await cursor.execute(
                "UPDATE users SET respect = respect + ? WHERE user_id = ?",(rep_amount,user_id)
            )
            await conn.commit()
            return f"UserID: {user_id} получил {rep_amount} респктов!"
        except Exception as e:
            logging.error(f"Ошибка при добавлении респекта {e}")
        finally:
            await conn.close()

    async def update_admin_level(self,user_id: int,alevel : int ):
        conn,cursor = await self.connection_db()
        try:
            await cursor.execute("UPDATE users SET adminRightsLevel = ? WHERE user_id = ?",(alevel,user_id))
            await conn.commit()
            return f"[AdminSystem] Права админа {alevel} уровня, выданы пользователю: {user_id}"
        except Exception as e:
            print(e)
        finally:
            await conn.close()

    async def get_last_farm_time(self,user_id: int ):
        conn,cursor = await self.connection_db()
        try:
            last_time = await cursor.execute(
                "SELECT last_farm FROM users WHERE user_id = ?",(user_id,)
            )
            last_time = await cursor.fetchone()
            return last_time[0]
        finally:
            await conn.close()

    async def update_last_farm_time(self, user_id:int):
        conn, cursor = await self.connection_db()
        try:
            await cursor.execute(
                "UPDATE users SET last_farm = CURRENT_TIMESTAMP WHERE user_id = ?",
                (user_id,)
            )
            await conn.commit()
        finally:
            await conn.close()