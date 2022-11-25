import sqlite3

class Models:
    def __init__(self) -> None:
        self.db =  sqlite3.connect('database.db')
        self.cursor = self.db.cursor()
    
    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS servers (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            server_id TEXT, 
            server_owner TEXT,
            server_owner_id TEXT,
            server_name TEXT,
            member_count INTEGER,
            server_invited_date DATETIME DEFAULT CURRENT_TIMESTAMP)
        ''')
        self.db.commit()
    
    def add_server(self, server_id, server_owner,server_owner_id, server_name, member_count):
        self.create_table()
        self.cursor.execute('''
        INSERT INTO servers (server_id, server_owner, server_owner_id, server_name, member_count) VALUES (?, ?, ?, ?, ?)
        ''', (server_id, server_owner,server_owner_id, server_name, member_count))
        self.db.commit()

    def get_all_server(self):
        self.cursor.execute('''
        SELECT * FROM servers
        ''')
        return self.cursor.fetchall()
    
    def delete_server(self, server_id):
        self.cursor.execute('''
        DELETE FROM servers WHERE server_id = ?
        ''', (server_id,))
        self.db.commit()