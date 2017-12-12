# app/home/views.py

from flask import render_template,redirect
# added these lines
from flask_login import login_required
from .. import db
from ..models import Employee
import datetime
# end of added lines
from . import home

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")

@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    # print username
    # employee = db.getItem("Employee", {"username":username})
    #
    # if "current_cust" in employee:
    #     current_cust=employee['cutomer_cust']
    # else:
    #     current_cust="?"
    #
    # email=employee["email"]
    # username=employee["username"]
    # password=employee["password"]
    # last_name=employee["last_name"]
    # first_name=employee["first_name"]
    # if "mobile" in employee:
    #     mobile=employee["mobile"]
    # else:
    #     mobile="000-000-0000"
    # if "company_name" in employee:
    #     company_name=employee["company_name"]
    # else:
    #     company_name="?"

    return render_template('home/dashboard.html', title="Dashboard")

@home.route('/edit')
@login_required
def edit():
    '''
        render the edit view so users can change their information on the dashboard /edit route

    '''

    pass
