from config import *
from pymysql import connections


def db_conn():
    return connections.Connection(
        host=customhost,
        port=3306,
        user=customuser,
        password=custompass,
        db=customdb,
        autocommit=True
    )

def db_close(conn):
    conn.close()
