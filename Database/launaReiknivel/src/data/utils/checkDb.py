import psycopg2
from psycopg2 import sql, DatabaseError
from datetime import datetime, timedelta
import calendar 

def checkDb():
    config = {
        'dbname': 'postgres',  
        'user': 'postgres',
        'password': 'Tussa123!',
        'host': 'localhost',
        'port': 5432
    }

    db_name = dbname_()
    try:
        conn = psycopg2.connect(**config)
        conn.autocommit = True
        cursor = conn.cursor()
    
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,))
        if cursor.fetchone():
            print(f"Database '{db_name}' already exists.")
        else:
            print(f"Database '{db_name}' does not exist. Creating it now.")
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
        
        cursor.close()
        conn.close()
    except DatabaseError as e:
        print(e)

    return db_name


def dbname_():
    cur_month = datetime.now().month
    if cur_month == 12:
        return f"LAUN_{calendar.month_abbr[cur_month]}-{calendar.month_abbr[1]}"
    return f"LAUN_{calendar.month_abbr[cur_month]}-{calendar.month_abbr[cur_month + 1]}"



