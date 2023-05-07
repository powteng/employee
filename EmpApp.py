from flask import Flask, render_template, request, redirect
from pymysql import connections
import os
import boto3
from config import *
from botocore import UNSIGNED
from botocore.client import Config
from botocore.handlers import disable_signing
from employee import add_employee, edit_employee, list_employee, delete_employee, select_employee

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'employee'

#go to home page
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

#go to about
@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('About.html')

#user management
@app.route("/userMain", methods=['GET', 'POST'])
def userMain():
    #return render_template('AddEmp.html')
    return render_template('employee/userMain.html')

#go to add new employee page
@app.route("/addNew", methods=['GET', 'POST'])
def addNew():
    return render_template('employee/AddEmp.html')

#fetch data and go to view all employee 
@app.route("/view_emp", methods=['GET'])
def view_emp():
    return render_template('employee/GetEmp.html', employee=list_employee())

#add employee to database and show
@app.route("/addemp", methods=['POST'])
def AddEmp():
    fn = request.form['full_name']
    role = request.form['role']
    email = request.form['email']
    phone = request.form['phone']
    gender = request.form['gender']
    photo = request.form['photo']
    ic = request.files['ic']
    return render_template('employee/AddEmpFormOutput.html', name=add_employee(fn, role, email, phone, gender, photo, ic))    

#update employee
@app.route("/edit_emp/<id>", methods=['GET'])
def UpdateEmp(id):
    return render_template('employee/EditEmp.html', employee=select_employee(id))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

