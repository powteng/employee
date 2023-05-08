from pymysql.cursors import DictCursor
import os
import boto3
from botocore import UNSIGNED
from botocore.client import Config
from botocore.handlers import disable_signing
from config import *
from db_connection import db_conn, db_close

table = "leave"
bucket = custombucket
region = customregion

def add_leave(data):
    emp_name = data['employee-name']
    _type = data['leave-type']
    start_date = data['start-date']
    end_date = data['end-date']
    reason = data['reason']
    
    #try:
    conn = db_conn()
    cursor = conn.cursor()
    insert_sql = "INSERT INTO `" + table + "` (emp_name, leave_type, date_from, date_to, reason) VALUES(%s, %s, %s, %s, %s)"
    print(insert_sql)
    cursor.execute(insert_sql, (emp_name, _type, start_date, end_date, reason))
    conn.commit()

#     except Exception as e:
#         return str(e)

#     finally:
    cursor.close()
    db_close(conn)
    return '''<script>alert('Leave submitted!');</script>'''

def list_list():
    conn = db_conn()
    cursor = conn.cursor(DictCursor)

    with cursor as cursor_:
        sql = "SELECT l.*, e.s3_photo_key FROM `" + table "` l JOIN employee e ON l.emp_name = e.full_name WHERE is_Deleted = 0"    
        cursor_.execute(sql)
        employees = cursor.fetchall()
        cursor_.close()

    db_close(conn)

    return leaves

def del_leave(id):
    conn = db_conn()
    cursor = conn.cursor()

    with cursor as cursor_:
        sql = "UPDATE `" + table + "` SET is_Deleted = 1 WHERE leave_id = " + str(id) 

        cursor_.execute(sql)
        conn.commit()
        cursor_.close()

    db_close(conn)
