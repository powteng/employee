from pymysql import connections
from pymysql.cursors import DictCursor
import os
import boto3
from botocore import UNSIGNED
from botocore.client import Config
from botocore.handlers import disable_signing
from config import *
from db_connection import db_conn, db_close
table = "employee"
bucket = custombucket
region = customregion

def add_employee(fn, ro, em, ge, ph, photo, ic):
    """
    Create new employee
    Args:
        fn (function): _description_
        ic (_type_): _description_
        ro (_type_): _description_
        em (_type_): _description_
        ph (_type_): _description_
        ge (_type_): _description_
        photo (_type_): _description_      
    Returns:
        _type_: _description_
    """
    emp_name = fn
    s3_photo_key = "emp-id-" + str(em) + "_image_file" + os.path.splitext(photo.filename)[1]
    s3 = boto3.resource('s3', config=Config(signature_version=UNSIGNED))
    s3.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)

    try:
        conn = db_conn()
        cursor = conn.cursor()
        insert_sql = "INSERT INTO " + table + " (full_name, ic, role, email, phone, gender, s3_photo_key) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_sql, (fn, ic, ro, em, ph, ge, s3_photo_key))
        conn.commit()
        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(custombucket).put_object(Key=s3_photo_key, Body=photo)
            #s3.Bucket(custombucket).put_object(Key=s3_ic_key, Body=ic)

        except Exception as e:
            print(str(e) + str('-S3'))
            return None

    except Exception as e:
        print(str(e))
        return None

    finally:
        cursor.close()

    return emp_name

def list_employee():
    """
    Retrieve employees
    Returns:
        _type_: _description_
    """
    conn = db_conn()
    cursor = conn.cursor(DictCursor)

    with cursor as cursor_:
        sql = "SELECT emp_id, full_name, email, role, phone, gender, s3_photo_key, is_delete FROM " + table + " WHERE is_delete = 0"    
        cursor_.execute(sql)
        employees = cursor.fetchall()
        cursor_.close()

    db_close(conn)

    return employees

def edit_employee(data):
    print(data)
    fn = data['full_name']
    em = data['email']
    ge = data['gender']
    ph = data['phone']
    emp_id = data['emp_id']

    conn = db_conn()
    cursor = conn.cursor()

    with cursor as cursor_:
        sql = "UPDATE "+ table +" SET \
        full_name = %s, \
        email = %s, \
        gender = %s, \
        phone = %s \
        WHERE emp_id = %s"

        cursor_.execute(sql, (fn, em, ge, ph, emp_id))
        conn.commit()
        cursor_.close()

    db_close(conn)    


def delete_employee(employee_id):

    conn = db_conn()
    cursor = conn.cursor()

    with cursor as cursor_:
        sql = "UPDATE " + table + " SET is_delete = 1 WHERE emp_id = " + str(employee_id) 

        cursor_.execute(sql)
        conn.commit()
        cursor_.close()

    db_close(conn)

def select_employee(employee_id):

    conn = db_conn()
    cursor = conn.cursor(DictCursor)

    with cursor as cursor_:
        sql = "SELECT * FROM " + table + " WHERE emp_id=" + employee_id
        cursor_.execute(sql)
        employee = cursor.fetchall()
        cursor_.close()

    db_close(conn)

    return employee[0]
