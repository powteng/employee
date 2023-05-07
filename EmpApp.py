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
output = {}
table = 'employee'

#go to home page
@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

#go to about
@app.route("/about", methods=['GET'])
def about():
    return render_template('About.html')

#user management
@app.route("/userMain", methods=['GET', 'POST'])
def userMain():
    return render_template('employee/userMain.html')

#go to add new employee page
@app.route("/addNew", methods=['GET', 'POST'])
def addNew():
    return render_template('employee/AddEmp.html')

#fetch data and go to view all employee 
@app.route("/view_emp", methods=['GET'])
def viewEmp():
    return render_template('employee/GetEmp.html', employee=list_employee())

#add employee to database and show
@app.route("/addemp", methods=['POST'])
def AddEmp():
    fn = request.form['full_name']
    role = request.form['role']
    email = request.form['email']
    phone = request.form['phone']
    gender = request.form['gender']
    photo = request.files['photo']
    ic = request.form['ic']
    return render_template('employee/AddEmpOutput.html', name=add_employee(fn, role, email, gender, phone, photo, ic))    

#delete employee
@app.route("/delete_emp/<id>", methods=['GET'])
def delEmp(id):
    delete_employee(id)
    return redirect('/view_emp')   

#go to update employee
@app.route("/edit_emp/<id>", methods=['GET'])
def UpdateEmp(id):
    return render_template('employee/EditEmp.html', employee=select_employee(id))
    
# #update record for employee    
@app.route("/edit_emp", methods=['POST'])
def UpdateEmpRec():
    edit_employee(request.form)
    return redirect('/view_emp')  


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

