import psycopg2
from psycopg2 import sql

class dataBase:
    def __init__(self, dbName):
        self.connection = psycopg2.connect(
            dbname=dbName,
            user="postgres",
            password="Tussa123!",
            host='localhost'
        )
        self.cursor = self.connection.cursor()

    def tableExists(self, tableName):
        """
        Checks if a table exists, and creates it if it does not.
        """
        # Use PostgreSQL's information_schema to check for table existence
        self.cursor.execute(
            """
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = %s
            );
            """,
            (tableName,)
        )
        if not self.cursor.fetchone()[0]:
            self.createTable(tableName)
        return True

    def executeQuery(self, query, params=None):
        """
        Executes a query with optional parameters.
        """
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
        """
        Creates a table with the given name, using PostgreSQL syntax.
        """
        # Use psycopg2's SQL module to safely format identifiers
        create_table_query = sql.SQL("""
            CREATE TABLE {} (
                shiftId SERIAL PRIMARY KEY,
                date DATE,
                dv NUMERIC(10 ,3),
                ev NUMERIC(10 ,3)
            );
        """).format(sql.Identifier(tableName))
        self.cursor.execute(create_table_query)
        print(f"Table '{tableName}' created.")
