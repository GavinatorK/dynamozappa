# app/models.py

from werkzeug.security import generate_password_hash, check_password_hash


from . import db
# update this to use dynamodb  methods

class Employee():

    """
    Create an Employee table
    """
    def __init__(self, username):

        self.username = username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username
# Set up user_loader


# class Department(db.Model):
#     """
#     Create a Department table
#     """
#
#     __tablename__ = 'departments'
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(60), unique=True)
#     description = db.Column(db.String(200))
#     employees = db.relationship('Employee', backref='department',
#                                 lazy='dynamic')
#
#     def __repr__(self):
#         return '<Department: {}>'.format(self.name)
#
# class Role(db.Model):
#     """
#     Create a Role table
#     """
#
#     __tablename__ = 'roles'
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(60), unique=True)
#     description = db.Column(db.String(200))
#     employees = db.relationship('Employee', backref='role',
#                                 lazy='dynamic')
#
#     def __repr__(self):
#         return '<Role: {}>'.format(self.name)
