import sqlite3

class Database:
    def __init__(self, db_name="db.db"):
        self.db_name = db_name

    def connection_db(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        return connection, cursor
    
    def create_users_table(self):
        conn, cursor = self.connection_db()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                username TEXT,
                first_name TEXT,
                adminRightsLevel INTEGER,
                join_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def create_sanctions_table(self):
        conn, cursor = self.connection_db()
        cursor.execute('''
            CREATE TABLE punishments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                chat_id INTEGER NOT NULL, 
                admin_id INTEGER NOT NULL,
                punishment_type TEXT NOT NULL,
                reason TEXT,
                duration INTEGER,  
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE  
            )
        '''
        )
        conn.commit()
        conn.close()

    def add_user(self, user_id, username, first_name,admLevel):
        conn, cursor = self.connection_db()
        cursor.execute(
            "INSERT OR IGNORE INTO users (user_id, username, first_name,adminRightsLevel) VALUES (?, ?, ?, ?)",
            (user_id, username, first_name,admLevel)
        )
        conn.commit()
        conn.close()
    
    def get_all_users(self):
        conn, cursor = self.connection_db()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()
        return users
    
    def get_admin_users(self):
        conn,cursor = self.connection_db()
        cursor.execute("SELECT * FROM users WHERE adminRightsLevel >= 1")
        admins = cursor.fetchall()
        conn.close()
        return admins

    def user_exists(self, user_id):
        conn, cursor = self.connection_db()
        cursor.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
        exists = cursor.fetchone() 
        conn.close()
        return exists
    
    def is_admin(self,user_id):
        conn,cursor = self.connection_db()
        cursor.execute("SELECT * FROM users WHERE user_id = ? AND adminRightsLevel >= 1",(user_id,))
        exists = cursor.fetchone()
        conn.close()
        if exists is None:
            return False
        else:
            return exists
        
    def get_admin_level(self,user_id):
        conn,cursor = self.connection_db()
        cursor.execute("SELECT adminRightsLevel FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            admin_level = result[0]  # result[0] потому что мы выбрали только один столбец
            return admin_level
        else:
            return 0  # или None если пользователя нет

    def add_punishment(self, user_id, chat_id, admin_id, punishment_type, reason, duration=None):
        conn, cursor = self.connection_db()
        cursor.execute(
            """INSERT INTO punishments 
            (user_id, chat_id, admin_id, punishment_type, reason, duration) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, chat_id, admin_id, punishment_type, reason, duration)
        )
        conn.commit()
        conn.close()

    def count_user_warns(self, user_id, chat_id):
        conn, cursor = self.connection_db()
        cursor.execute(
            """SELECT COUNT(*) FROM punishments 
            WHERE user_id = ? AND chat_id = ? AND punishment_type = 'warn' AND active = TRUE""",
            (user_id, chat_id)
        )
        count = cursor.fetchone()[0]
        conn.close()
        return count




