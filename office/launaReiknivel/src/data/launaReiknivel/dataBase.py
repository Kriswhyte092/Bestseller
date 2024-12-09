import sqlite3

class dataBase:
    def __init__(self, dbName):
        self.connection = sqlite3.connect(dbName)
        self.cursor = self.connection.cursor()

    def tableExists(self, tableName):
        """
        þetta func a bara við i þessu tiltekna scenario þar
        þar sem við viljum að það se alltaf created table
        """
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tableName}';")
        if self.cursor.fetchone() is None:
            self.createTable(tableName)
        return True


    def executeQuery(self, query, params):
        if params is None:
            params = ()
        self.cursor.execute(query, params)

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        self.connection.close()

    def createTable(self, tableName):
        self.cursor.execute(f"""
            CREATE TABLE {tableName} (
            shiftId INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            dv INTEGER,
            ev INTEGER
            );
        """)
        print(f"Table '{tableName}' created.")

