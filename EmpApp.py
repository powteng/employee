from flask import Flask, render_template, request, redirect, url_for
from pymysql import connections
import os
import boto3
from config import *
from botocore import UNSIGNED
from botocore.client import Config
from botocore.handlers import disable_signing
from employee import add_employee, edit_employee, list_employee, delete_employee, select_employee
from leave import add_leave, list_leave, delete_leave
from payroll import add_payroll, list_payroll, delete_payroll

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
    name= add_employee(fn, role, email, gender, phone, photo, ic)
    return redirect('/view_emp')    

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

#fo to leave main page
@app.route("/leave", methods=['GET', 'POST'])
def leaveMain():
    return render_template('leaveMain/leavemain.html')

#go to add leave page
@app.route("/addLeave", methods=['GET', 'POST'])
def gotoAddLeave():
    return render_template('leaveMain/leave.html', employees=list_employee())

#add leave to db
@app.route("/apply_leave", methods=['POST'])
def addLeave():
    add_leave(request.form)
    return redirect('/listLeave')

#view leave
@app.route("/listLeave", methods=['GET'])
def viewLeave():
    return render_template('leaveMain/listLeave.html', leaves=list_leave())

#delete leave
@app.route("/delete_leave/<id>", methods=['GET'])
def delLeave(id):
    delete_leave(id)
    return redirect('/listLeave') 

#go to payroll main page
@app.route("/payrollMain", methods=['GET', 'POST'])
def payrollMain():
    return render_template('payroll/payrollmain.html')

#go to add payroll page
@app.route("/payroll", methods=['GET', 'POST'])
def gotoAddPayroll():
    return render_template('payroll/payroll.html', employees=list_employee())

#add payroll to database
@app.route("/addpayroll", methods=['POST'])
def addPayroll():
    add_payroll(request.form)
    return redirect('/listpayroll')

#list payroll
@app.route("/listpayroll", methods=['GET'])
def viewPayroll():
    return render_template('payroll/listpayroll.html', payroll=list_payroll())

#delete payroll
@app.route("/delete_payroll/<id>", methods=['GET'])
def delPayroll(id):
    delete_payroll(id)
    return redirect('/listpayroll') 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

