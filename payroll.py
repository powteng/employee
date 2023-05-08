from pymysql.cursors import DictCursor
import os
import boto3
from botocore import UNSIGNED
from botocore.client import Config
from botocore.handlers import disable_signing
from config import *
from db_connection import db_conn, db_close

table = "payroll"
bucket = custombucket
region = customregion

def add_payroll(data):
  emp_id = data['emp-id']
  salary = data['salary']
  
  #tey
  conn = db_conn()
  cursor = conn.cursor()
  insert_sql = "INSERT INTO `" + table + "` (emp_id, salary) VALUES(%s, %s)"
  print(insert_sql)
  cursor.execute(insert_sql, (emp_id, salary))
  conn.commit()

#     except Exception as e:
#         return str(e)

#     finally:
  cursor.close()
  db_close(conn)
  return '''<script>alert('Leave submitted!');</script>'''

def list_payroll():
  conn = db_conn()
  cursor = conn.cursor(DictCursor)

  with cursor as cursor_:
      SELECT p.*, e.* FROM " + table +" p JOIN employee e ON p.emp_id = e.emp_id WHERE p.is_Deleted = 0;
   
      cursor_.execute(sql)
      payroll = cursor.fetchall()
      cursor_.close()

  db_close(conn)

  return payroll

def delete_payroll(id):
  conn = db_conn()
  cursor = conn.cursor()

  with cursor as cursor_:
      sql = "UPDATE `" + table + "` SET is_Deleted = 1 WHERE pay_id = " + str(id) 

      cursor_.execute(sql)
      conn.commit()
      cursor_.close()

  db_close(conn)
