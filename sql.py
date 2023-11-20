import sqlite3 as sql

def add_user_to_group(chat_id, user_id, username, first_name, last_name):
    with sql.connect('bot_database.db') as db:
        c = db.cursor()

        table_name = str(chat_id)

        c.execute(f'''
            CREATE TABLE IF NOT EXISTS '{table_name}' (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                username TEXT,
                first_name TEXT,
                last_name TEXT
            )
        ''')

        db.commit()

        c.execute(f"SELECT * FROM '{table_name}'")
        everything = c.fetchall()
        if not any(uid == user_id for _, uid, _, _, _, in list(everything)):
            c.execute(f'''
                INSERT INTO '{table_name}' (user_id, username, first_name, last_name)
                VALUES (?, ?, ?, ?)
            ''', (user_id, username, first_name, last_name))
            db.commit()

            print(f'@{username} has been added to the {chat_id} database!')
        else:
            return

def add_user_to_level(chat_id, user_id, username, first_name, last_name):
    with sql.connect('bot_database.db') as db:
        c = db.cursor()

        c.execute('''
        CREATE TABLE IF NOT EXISTS level_table (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            level INTEGER
        )      
        ''')

        db.commit()

        c.execute(f"SELECT * FROM level_table")
        everything = c.fetchall()
        if not any(uid == user_id for _, uid, _ in list(everything)):
            c.execute(f'''
                INSERT INTO level_table (user_id, level)
                VALUES (?, ?)
            ''', (user_id, 0))
            db.commit()

            print(f'@{username} has been added to the level database!')

        else:
            return

def add_level(user_id):
    with sql.connect('bot_database.db') as db:
        c = db.cursor()
        c.execute('SELECT level FROM level_table WHERE user_id = ?', (user_id,))
        level = c.fetchone()[0]
        c.execute("UPDATE level_table SET level = ? WHERE user_id = ?", (level + 1, user_id))
        db.commit()

def get_chat_members(chat_id):
    with sql.connect('bot_database.db') as db:
        c = db.cursor()
        members = []

        c.execute(f'''
            SELECT user_id FROM '{chat_id}'
        ''')
        results = c.fetchall()
        for result in results:
            result, = result
            members.append(result)

        return members

def get_admin(user_id):
    with sql.connect('bot_database.db') as db:
        c = db.cursor()

        c.execute(f'''
            SELECT user_id FROM admins
        ''')
        admins = c.fetchall()
        admin_user_ids = [admin[0] for admin in admins]

        if user_id in admin_user_ids:
            return True
        else:
            return False

def add_admin(chat_id, user_id, username, first_name, last_name):
    with sql.connect('bot_database.db') as db:
        c = db.cursor()

        c.execute(f'''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                username TEXT,
                first_name TEXT,
                last_name TEXT
            )
        ''')

        db.commit()

        c.execute('''
        SELECT user_id FROM admins
        ''')

        if not get_admin(chat_id):

            c.execute(f'''
                INSERT INTO admins (user_id, username, first_name, last_name)
                VALUES (?, ?, ?, ?)
            ''', (user_id, username, first_name, last_name))

            print(f'@{username} has been added to the admins!')

            db.commit()

        else:
            return

def get_level(user_id):
    with sql.connect('bot_database.db') as db:
        c = db.cursor()
        c.execute('SELECT level FROM level_table WHERE user_id = ?', (user_id,))
        level = str(c.fetchone()[0])
        return level
