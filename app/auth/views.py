# app/auth/views.py

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from .. import login_manager
from . import auth
from forms import LoginForm, RegistrationForm
from .. import db
from ..models import Employee
from token import generate_confirmation_token, confirm_token
import datetime
from email import send_email
# update this file to replace sql stuff with dynamodb stuff

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        employee = {"email":form.email.data,
                            "username":form.username.data,
                            "first_name":form.first_name.data,
                            "last_name":form.last_name.data,
                            "password":form.password.data,
                            "confirmed":False,
                            "confirmed_on":"?"}

        # add employee to the database
        db.createItem("Employee",employee)
        if db.getItem("Employee", {"username":form.username.data}):

            flash('You have successfully registered! You may now login.')

        # redirect to the login page
        token = generate_confirmation_token(form.email.data)
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        html = render_template('auth/activate.html', confirm_url=confirm_url)
        print html
        subject = "Please confirm your email"
        send_email(form.email.data, subject, html)
        flash('A confirmation email has been sent via email.', 'success')
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        employee = db.getItem("Employee", {"username":form.username.data})
        if employee is not None and employee['password']==form.password.data:
            # log employee in
            user_obj=Employee(employee['username'])
            login_user(user_obj)
            flash("Logged in successfully!", category='success')
            # redirect to the dashboard page after login
            return redirect(url_for('home.dashboard'))

        # when login details are incorrect
        else:
            flash('Invalid email or password.')
            # load login template
    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))

@login_manager.user_loader
def load_user(username):
    if "username" in db.getItem("Employee", {"username":username}):
        return Employee(username)
    else:
        return None

@auth.route('/confirm/<token>')
@login_required
def confirm_email(token):
    print "made it here"
    flash("confirming your email")
    try:
        print "trying to get email from confirm_token"
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = db.scanTable("Employee", "Attr('email').eq('"+ email +"')")[0]
    print user
    flash(user['email'])
    if user["confirmed"]:
        flash('Account already confirmed. Please login.', 'success')
    else:
        db.updateItem("Employee", key={"username":user["username"]}, updateExpression='SET confirmed = :val1, confirmed_on=:val2',expressionAttributeValues={
                        ':val1': True,
                        ':val2': str(datetime.datetime.now())
                    } )

        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('auth.login'))
